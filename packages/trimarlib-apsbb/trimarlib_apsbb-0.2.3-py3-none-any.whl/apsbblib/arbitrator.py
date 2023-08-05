import erpc
from erpc.codec import MessageType


class SocketArbitrator(erpc.arbitrator.TransportArbitrator):
    """Shares a transport between a server and multiple clients."""
    def __init__(self, sharedTransport=None, codec=None):
        super(SocketArbitrator, self).__init__(sharedTransport, codec)

    def receive(self):
        assert self._transport is not None, "No shared transport was set"
        assert self._codec is not None, "No codec was set"

        # Repeatedly receive until we get an invocation request.
        while True:
            # Receive a message from the shared transport.
            msg = None
            try:
                msg = self._transport.receive()
            except erpc.transport.ConnectionClosed:
                # notify all pending clients
                with self._lock:
                    for seq, client in self._pending_clients.items():
                        client.msg = None
                        client.event.set()
                # re-raise exception
                raise

            # Parse the message header.
            self._codec.buffer = msg
            info = self._codec.start_read_message()

            # If it's an invocation or oneway, return it to the server.
            if info.type in (MessageType.kInvocationMessage, MessageType.kOnewayMessage):
                return msg
            # Ignore unexpected message types.
            elif info.type != MessageType.kReplyMessage:
                continue

            # Look up the client waiting for this reply.
            try:
                try:
                    self._lock.acquire()
                    client = self._pending_clients[info.sequence]
                finally:
                    self._lock.release()
                client.msg = msg
                client.event.set()
            except KeyError:
                # No client was found, unexpected sequence number!
                pass
