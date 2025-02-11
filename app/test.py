import struct

binary_packet = b'\x02\x10\x00\x01m,\x00\x00\x9aY\xb6C78\xabg'

header = binary_packet[:8]  # First 8 bytes

ltp, ltt = struct.unpack('<fI', binary_packet[8:16])
 
print(ltp, ltt)