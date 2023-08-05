import json
import socket
import logging
from itertools import cycle
from twisted.internet import defer, reactor, protocol
from twisted.application.internet import ClientService, CancelledError
from twisted.internet.endpoints import clientFromString
from twisted.protocols.basic import LineOnlyReceiver

from torba import __version__
from torba.stream import StreamController

log = logging.getLogger(__name__)


class StratumClientProtocol(LineOnlyReceiver):
    delimiter = b'\n'
    MAX_LENGTH = 2000000

    def __init__(self):
        self.request_id = 0
        self.lookup_table = {}
        self.session = {}
        self.network = None

        self.on_disconnected_controller = StreamController()
        self.on_disconnected = self.on_disconnected_controller.stream

    def _get_id(self):
        self.request_id += 1
        return self.request_id

    @property
    def _ip(self):
        return self.transport.getPeer().host

    def get_session(self):
        return self.session

    def connectionMade(self):
        try:
            self.transport.setTcpNoDelay(True)
            self.transport.setTcpKeepAlive(True)
            if hasattr(socket, "TCP_KEEPIDLE"):
                self.transport.socket.setsockopt(
                    socket.SOL_TCP, socket.TCP_KEEPIDLE, 120
                    # Seconds before sending keepalive probes
                )
            else:
                log.debug("TCP_KEEPIDLE not available")
            if hasattr(socket, "TCP_KEEPINTVL"):
                self.transport.socket.setsockopt(
                    socket.SOL_TCP, socket.TCP_KEEPINTVL, 1
                    # Interval in seconds between keepalive probes
                )
            else:
                log.debug("TCP_KEEPINTVL not available")
            if hasattr(socket, "TCP_KEEPCNT"):
                self.transport.socket.setsockopt(
                    socket.SOL_TCP, socket.TCP_KEEPCNT, 5
                    # Failed keepalive probles before declaring other end dead
                )
            else:
                log.debug("TCP_KEEPCNT not available")

        except Exception as err: # pylint: disable=broad-except
            # Supported only by the socket transport,
            # but there's really no better place in code to trigger this.
            log.warning("Error setting up socket: %s", err)

    def connectionLost(self, reason=None):
        self.on_disconnected_controller.add(True)

    def lineReceived(self, line):
        log.debug('received: %s', line)

        try:
            message = json.loads(line)
        except (ValueError, TypeError):
            raise ValueError("Cannot decode message '{}'".format(line.strip()))

        if message.get('id'):
            try:
                d = self.lookup_table.pop(message['id'])
                if message.get('error'):
                    d.errback(RuntimeError(message['error']))
                else:
                    d.callback(message.get('result'))
            except KeyError:
                raise LookupError(
                    "Lookup for deferred object for message ID '{}' failed.".format(message['id']))
        elif message.get('method') in self.network.subscription_controllers:
            controller = self.network.subscription_controllers[message['method']]
            controller.add(message.get('params'))
        else:
            log.warning("Cannot handle message '%s'", line)

    def rpc(self, method, *args):
        message_id = self._get_id()
        message = json.dumps({
            'id': message_id,
            'method': method,
            'params': args
        })
        log.debug('sent: %s', message)
        self.sendLine(message.encode('latin-1'))
        d = self.lookup_table[message_id] = defer.Deferred()
        return d


class StratumClientFactory(protocol.ClientFactory):

    protocol = StratumClientProtocol

    def __init__(self, network):
        self.network = network
        self.client = None

    def buildProtocol(self, addr):
        client = self.protocol()
        client.factory = self
        client.network = self.network
        self.client = client
        return client


class BaseNetwork:

    def __init__(self, ledger):
        self.config = ledger.config
        self.client = None
        self.service = None
        self.running = False

        self._on_connected_controller = StreamController()
        self.on_connected = self._on_connected_controller.stream

        self._on_header_controller = StreamController()
        self.on_header = self._on_header_controller.stream

        self._on_status_controller = StreamController()
        self.on_status = self._on_status_controller.stream

        self.subscription_controllers = {
            'blockchain.headers.subscribe': self._on_header_controller,
            'blockchain.address.subscribe': self._on_status_controller,
        }

    @defer.inlineCallbacks
    def start(self):
        self.running = True
        for server in cycle(self.config['default_servers']):
            connection_string = 'tcp:{}:{}'.format(*server)
            endpoint = clientFromString(reactor, connection_string)
            log.debug("Attempting connection to SPV wallet server: %s", connection_string)
            self.service = ClientService(endpoint, StratumClientFactory(self))
            self.service.startService()
            try:
                self.client = yield self.service.whenConnected(failAfterFailures=2)
                yield self.ensure_server_version()
                log.info("Successfully connected to SPV wallet server: %s", connection_string)
                self._on_connected_controller.add(True)
                yield self.client.on_disconnected.first
            except CancelledError:
                return
            except Exception:  # pylint: disable=broad-except
                log.exception("Connecting to %s raised an exception:", connection_string)
            finally:
                self.client = None
                if self.service is not None:
                    self.service.stopService()
            if not self.running:
                return

    def stop(self):
        self.running = False
        if self.service is not None:
            self.service.stopService()
        if self.is_connected:
            return self.client.on_disconnected.first
        else:
            return defer.succeed(True)

    @property
    def is_connected(self):
        return self.client is not None and self.client.connected

    def rpc(self, list_or_method, *args):
        if self.is_connected:
            return self.client.rpc(list_or_method, *args)
        else:
            raise ConnectionError("Attempting to send rpc request when connection is not available.")

    def ensure_server_version(self, required='1.2'):
        return self.rpc('server.version', __version__, required)

    def broadcast(self, raw_transaction):
        return self.rpc('blockchain.transaction.broadcast', raw_transaction)

    def get_history(self, address):
        return self.rpc('blockchain.address.get_history', address)

    def get_transaction(self, tx_hash):
        return self.rpc('blockchain.transaction.get', tx_hash)

    def get_merkle(self, tx_hash, height):
        return self.rpc('blockchain.transaction.get_merkle', tx_hash, height)

    def get_headers(self, height, count=10000):
        return self.rpc('blockchain.block.headers', height, count)

    def subscribe_headers(self):
        return self.rpc('blockchain.headers.subscribe', True)

    def subscribe_address(self, address):
        return self.rpc('blockchain.address.subscribe', address)
