import pyshark
from collections import defaultdict
import sys
from tqdm import tqdm

if len(sys.argv) != 3:
    print('Usage:\n    python main.py yourtraffic.pcap output.file')
    exit()

filename = sys.argv[1]
output_filename = sys.argv[2]

def count_packets(cap):
    print("[+] Counting packets...")
    cnt = 0
    for _ in tqdm(cap, desc="Counting packets", unit="pkt"):
        cnt += 1
    return cnt

def find_pieces(cap, total_packets):
    print("[+] Searching for data pieces...")
    pieces = defaultdict(list)  # index: [begin, data]

    for pkt in tqdm(cap, desc="Finding pieces", total=total_packets, unit="pkt"):
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
        for index in tqdm(sorted(pieces.keys()), desc="Writing pieces", unit="index"):
            piece_list = sorted(pieces[index], key=lambda x: x[0])
            for begin, hexdata in tqdm(piece_list, desc=f"Writing index {index}", leave=False, unit="chunk"):
                out.write(bytes.fromhex(hexdata))

if __name__ == "__main__":
    print("[+] Opening capture file...\nIt might take a while, because pyshark uses a ton of RAM.")
    cap = pyshark.FileCapture(filename, display_filter="bittorrent", keep_packets=False)

    dumplen = count_packets(cap)
    print(f"dump len is {dumplen}")

    pieces = find_pieces(cap, dumplen)
    print(f"[+] Found {len(pieces)} pieces.") 

    rebuild_file(pieces, output_filename)
    print("[+] Rebuilt file successfully.")

