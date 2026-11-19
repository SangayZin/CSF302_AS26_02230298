"""
Lab 7 Q2: Huffman Coding

Builds a Huffman tree from the character frequencies of a text file,
prints the code table, encodes the file to a bit string, decodes it again,
and reports the compression ratio against 8-bit fixed-length encoding.

Run:  python q2_huffman.py [file1 file2 ...]
With no arguments it uses the three sample files in data/.
"""

import heapq
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.char is not None


def build_tree(freq):
    # The middle number breaks ties between equal frequencies, so heapq never
    # has to compare two Node objects (and the tree is the same on every run).
    heap = [(f, i, Node(f, ch)) for i, (ch, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    counter = len(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, Node(f1 + f2, left=a, right=b)))
        counter += 1
    return heap[0][2]


def make_codes(root):
    codes = {}
    if root.is_leaf():
        codes[root.char] = "0"      # a file with one distinct character still needs one bit
        return codes

    def walk(node, path):
        if node.is_leaf():
            codes[node.char] = path
            return
        walk(node.left, path + "0")
        walk(node.right, path + "1")

    walk(root, "")
    return codes


def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, root):
    if root.is_leaf():
        return root.char * len(bits)
    out = []
    node = root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.is_leaf():
            out.append(node.char)
            node = root
    return "".join(out)


def show_char(ch):
    return {"\n": "\\n", " ": "space", "\t": "\\t"}.get(ch, ch)


def process(path, show_table=True):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    freq = Counter(text)
    root = build_tree(freq)
    codes = make_codes(root)
    bits = encode(text, codes)
    decoded = decode(bits, root)

    print("=" * 60)
    print(f"File: {os.path.basename(path)}")
    print("=" * 60)
    if show_table:
        print(f"{'char':>6} {'freq':>7}  code")
        for ch, f in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{show_char(ch):>6} {f:>7}  {codes[ch]}")
    fixed_bits = 8 * len(text)
    avg = len(bits) / len(text)
    print(f"\ncharacters            : {len(text):,}")
    print(f"distinct characters   : {len(freq)}")
    print(f"first 64 encoded bits : {bits[:64]}")
    print(f"8-bit fixed length    : {fixed_bits:,} bits")
    print(f"Huffman encoded       : {len(bits):,} bits ({avg:.3f} bits per character)")
    print(f"compression ratio     : {len(bits) / fixed_bits:.3f} "
          f"(saves {1 - len(bits) / fixed_bits:.1%})")
    print(f"decoded == original   : {decoded == text}")
    print()
    return os.path.basename(path), len(text), len(freq), fixed_bits, len(bits), decoded == text


if __name__ == "__main__":
    paths = sys.argv[1:] or [os.path.join(HERE, "data", name) for name in
                             ("english_text.txt", "python_code.txt", "dna_sequence.txt")]
    rows = [process(p) for p in paths]
    print("| file | characters | distinct | fixed 8-bit (bits) | Huffman (bits) | bits/char | ratio | decoded OK |")
    print("|---|---|---|---|---|---|---|---|")
    for name, n, d, fixed, huff, ok in rows:
        print(f"| {name} | {n:,} | {d} | {fixed:,} | {huff:,} | {huff / n:.3f} | {huff / fixed:.3f} | {'yes' if ok else 'no'} |")
