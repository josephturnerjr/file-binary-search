import struct
import ipaddress
import functools


class IPLookup:
    FORMAT = "!III"

    def __init__(self, filename):
        self.geofile = open(filename, "rb")
        self.geofile.seek(0, 2)
        self.file_length = self.geofile.tell()
        self.geofile.seek(0, 0)
        self.rowsize = struct.calcsize(self.FORMAT)
        self.rows = self.file_length // self.rowsize

    @functools.lru_cache()
    def find_ip(self, ip):
        ip_int = int(ipaddress.ip_address(ip))
        lo = 0
        hi  = self.rows - 1
        return self.binsearch(ip_int, lo, hi)

    def binsearch(self, ip, lo, hi):
        if lo > hi:
            return
        mid = int((lo + hi) // 2)
        self.geofile.seek(self.rowsize * mid)
        range_low, range_hi, rowid = struct.unpack(self.FORMAT, self.geofile.read(self.rowsize))
        if ip >= range_low and ip <= range_hi:
            return rowid
        elif ip < range_low:
            return self.binsearch(ip, lo, mid - 1)
        else:
            return self.binsearch(ip, mid + 1, hi)


if __name__ == "__main__":
    lookup = IPLookup("out.geo")
    print(lookup.find_ip(sys.argv[1]))
