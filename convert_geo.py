import ipaddress
import struct
import sys


with open('out.geo', 'wb') as outfile:
    with open('sample.geo') as infile:
        for line in infile:
            ranges, rowid = line.strip().split(",")
            low, high = ranges.split("-")
            rowid = int(rowid)
            low = int(ipaddress.ip_address(low))
            high = int(ipaddress.ip_address(high))
            print(low, high, rowid)
            outfile.write(struct.pack("!III", int(low), int(high), int(rowid)))
