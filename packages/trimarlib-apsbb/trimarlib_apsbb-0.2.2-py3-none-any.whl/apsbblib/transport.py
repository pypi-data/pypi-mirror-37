from erpc import transport


class SerialTransport(transport.SerialTransport):
    def __init__(self, url, baudrate, **kwargs):
        super(SerialTransport, self).__init__(url, baudrate, **kwargs)

    def send(self, message):
        with self._sendLock:
            crc = self._Crc16.computeCRC16(message).to_bytes(2, 'little')
            dlen = len(message).to_bytes(2, 'little')
            xlen = (dlen[0] ^ dlen[1] ^ 0xAA).to_bytes(1, 'little')
            head = b''.join([b'\xA5\x5A', dlen, xlen])
            assert len(head) == 5
            self._base_send(b''.join([head, message, crc]))

    def receive(self):
        with self._receiveLock:
            # receive first pack of data and loop until synchronization sequence is found
            buf = bytearray(self._base_receive(5))
            if buf == b'':
                raise TimeoutError('timeout')
            while b'\xA5\x5A' not in buf:
                if buf[-1] == 0xA5:
                    buf = buf[-1:]
                else:
                    buf.clear()
                tmp = self._base_receive(5)
                if tmp == b'':
                    raise ValueError('synchronization sequence not found')
                buf += tmp
            # strip leading garbage, read following bytes if needed to extended the buffer
            idx = buf.index(b'\xA5\x5A')
            buf = buf[idx:]
            if len(buf) < 5:
                tmp = self._base_receive(5 - len(buf))
                if tmp == b'':
                    raise TimeoutError('incomplete frame: missing header data')
                buf += tmp
            # validate and decode message length
            if (buf[2] ^ buf[3] ^ buf[4] ^ 0xAA) != 0:
                raise ValueError('corrupted data: invalid XLEN value')
            dlen = int.from_bytes(buf[2:4], 'little')
            data = buf[5:]
            data += self._base_receive(dlen - len(data))
            if len(data) != dlen:
                raise TimeoutError('incomplete frame: missing message data')
            buf = self._base_receive(2)
            if len(buf) != 2:
                raise TimeoutError('incomplete frame: missing CRC')
            crc = int.from_bytes(buf, 'little')
            if crc != self._Crc16.computeCRC16(data):
                raise ValueError('corrupted data: CRC value mismatch')
            return data
