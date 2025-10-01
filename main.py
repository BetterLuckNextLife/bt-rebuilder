import pyshark
from collections import defaultdict
import sys

if len(sys.argv) != 3:
    print('Usage: ...')
    exit()

filename = sys.argv[1]
output_filename = sys.argv[2]

def find_pieces(cap):
    pieces = defaultdict(list)  # index: [begin, data]

    for pkt in cap:
        if not hasattr(pkt, "bittorrent"):
            continue
        bt = pkt.bittorrent
        required_fields = {"piece_index", "piece_begin", "piece_data"}
        if not required_fields.issubset(bt.field_names):
            continue
        try:
            index = int(str(bt.piece_index), 16)
            begin = int(str(bt.piece_begin), 16)
            data = bt.piece_data.replace(":", "")
            pieces[index].append((begin, data))
        except Exception:
            continue
    return pieces


def rebuild_file(pieces, output_filename):
    with open(output_filename, "wb") as out:
        for index in sorted(pieces.keys()):
            print(f"[+] Writing index {index}, {len(pieces[index])} pieces")
            for begin, hexdata in sorted(pieces[index], key=lambda x: x[0]):
                out.write(bytes.fromhex(hexdata))


if __name__ == "__main__":
    print("[+] Opening capture file...")
    cap = pyshark.FileCapture(filename, display_filter="bittorrent", keep_packets=False)
    pieces = find_pieces(cap)
    print(f"[+] Found {len(pieces)} pieces.") 
    rebuild_file(pieces, output_filename)
    print("[+] Rebuilt file successfully.")

