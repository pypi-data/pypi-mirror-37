import hashlib

from .common import IANAList


class StrToPort:
    def __init__(self, s, use_iana=False):
        if use_iana:
            self.port_range = IANAList().available_ports
        else:
            self.port_range = range(1024, 65536)

        self.h = int(hashlib.md5(s.encode()).hexdigest(), 16)

        self.remaining = self.h

    def _next(self):
        self.remaining = self.remaining // len(self.port_range)
        if self.remaining > 0:
            return self.port_range[self.remaining % len(self.port_range) + 1]

    def all(self):
        ports = []

        while True:
            port = self._next()
            if port is None:
                break

            ports.append(port)

        self.remaining = self.h

        return ports
