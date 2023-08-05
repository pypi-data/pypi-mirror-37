import csv
try:
    import importlib.resources
except ImportError:
    pass


class IANAList:
    def __init__(self):
        self.used_ports = set()
        raw = importlib.resources.read_text('str2port', 'iana.csv').strip().split('\n')
        records = csv.DictReader(raw)
        for record in records:
            port = record['Port Number'].strip()
            if port:
                try:
                    self.used_ports.add(int(port))
                except ValueError:
                    port_from, port_to = port.split('-')
                    self.used_ports.update(range(int(port_from), int(port_to) + 1))

        self.available_ports = sorted(set(range(1024, 65536)) - self.used_ports)

    def __len__(self):
        return len(self.available_ports)

    def is_free(self, i):
        return i not in self.used_ports
