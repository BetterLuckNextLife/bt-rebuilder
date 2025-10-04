**bt-rebuilder**

bt-rebuilder is a small utility for reconstructing files from BitTorrent network captures (`.pcap / .pcapng`).
It automatically extracts and reassembles data pieces from captured packets.

---

### ⚙️ Features:

* Automatically extracts BitTorrent pieces from `.pcap` files
* Rebuilds the original file from fragmented data
* Simple single-script usage

---

### 🔧 Installation:

1. Clone the repository:

```bash
git clone https://github.com/BetterLuckNextLife/bt-rebuilder
```

2. Install dependencies:

```bash
cd bt-rebuilder
pip install -r requirements.txt
```

3. Make sure **tshark** is installed on your system (required by pyshark):

4. Run the tool:

```bash
python main.py yourtraffic.pcap output.file
```

---

### 🧱 Example:

```bash
python main.py evidence.pcap recovered.pdf
```

The result will be the recovered file (`recovered.pdf`) rebuilt from BitTorrent pieces.


### 💡 Thoughts on development:

This little project was made after a CTF. Don't think it will be useful outside of solving similar tasks.
The script is slow as hell, because pyshark fully parses every packet, even if i don't need it. If you have any ideas on how to optimize it, feel free to fork the repo and open a pr.
