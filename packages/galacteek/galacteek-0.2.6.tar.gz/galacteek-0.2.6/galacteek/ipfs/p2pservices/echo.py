import asyncio

from galacteek import log
from galacteek.ipfs import tunnel
from galacteek.ipfs.ipfsops import *
from galacteek.ipfs.p2pservices import P2PService

from PyQt5.QtCore import QObject


class EchoProtocol(asyncio.Protocol):
    def __init__(self, exitF):
        super().__init__()
        self.exitF = exitF
        self.msgCount = 0

    def connection_made(self, transport):
        log.debug('HELLO', transport)
        self.transport = transport
        self.transport.write('Hello'.encode())

    def data_received(self, data):
        self.msgCount += 1
        if self.msgCount < 5:
            self.transport.write(data)
        else:
            self.transport.close()

    def eof_received(self):
        pass

    def connection_lost(self, exc):
        self.exitF.set_result(True)


class P2PEchoListener(tunnel.P2PListener):
    def __init__(self, client, protocol, address):
        self.exitF = asyncio.Future()
        self.proto = EchoProtocol(self.exitF)
        super().__init__(client, protocol, address,
                lambda: self.proto)


class EchoReceiver(QObject):
    def __init__(self, service):
        super().__init__(None)
        self.service = service


class P2PEchoService(P2PService):
    def __init__(self):
        receiver = EchoReceiver(self)
        super().__init__(
            'echo',
            'Echo service',
            'echo',
            ('127.0.0.1', range(12000, 12010)),
            receiver
        )

    async def createListener(self, client, **kw):
        self._listener = P2PEchoListener(
            client, self.protocolName,
            self.listenRange
        )
        addr = await self.listener.open()
        log.debug('P2PEchoService: created listener at address {0}'.format(
            addr))
        return True
