import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pickle
import heapq
from collections import defaultdict
import ttkbootstrap as ttk
from tkinter import Tk, filedialog
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb


# Huffman Compression and Decompression Logic
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq_map = defaultdict(int)
    for char in text:
        freq_map[char] += 1

    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_codes(root, current_code="", codes={}):
    if root is None:
        return

    if root.char is not None:
        codes[root.char] = current_code

    build_codes(root.left, current_code + "0", codes)
    build_codes(root.right, current_code + "1", codes)

    return codes

def huffman_compress(text):
    root = build_huffman_tree(text)
    codes = build_codes(root)

    # Encode the text using the Huffman codes
    compressed_bits = ''.join(codes[char] for char in text)

    # Pad the compressed bits to make it a multiple of 8
    padding_length = 8 - len(compressed_bits) % 8
    compressed_bits += '0' * padding_length

    # Convert the bit string to bytes
    compressed_data = bytearray()
    for i in range(0, len(compressed_bits), 8):
        byte = int(compressed_bits[i:i+8], 2)
        compressed_data.append(byte)

    tree_and_data = {
        "tree": root,
        "data": compressed_data,
        "padding_length": padding_length
    }

    return pickle.dumps(tree_and_data) 

def huffman_decompress(serialized_data):
    # Convert bytes back to a bit string
    tree_and_data = pickle.loads(serialized_data)
    root = tree_and_data["tree"]
    compressed_data = tree_and_data["data"]
    padding_length = tree_and_data["padding_length"]
    compressed_bits = ''.join(f"{byte:08b}" for byte in compressed_data)

    # Remove the padding
    compressed_bits = compressed_bits[:-padding_length]

    # Decode the bit string using the Huffman tree
    result = []
    node = root
    for bit in compressed_bits:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            result.append(node.char)
            node = root

    return ''.join(result)

# RLE Compression and Decompression Logic
def rle_compress(data):
    encoding = ''
    i = 0

    while i < len(data):
        count = 1

        while i + 1 < len(data) and data[i] == data[i + 1]:
            count += 1
            i += 1

        encoding += str(count) + data[i]
        i += 1

    return encoding

def rle_decompress(data):
    decoding = ''
    i = 0

    while i < len(data):
        count_str = ''
        while i < len(data) and data[i].isdigit():
            count_str += data[i]
            i += 1
        count = int(count_str)
        decoding += data[i] * count
        i += 1

    return decoding

# LZW Compression and Decompression Logic
def lzw_compress(text):
    dictionary = {chr(i): i for i in range(256)}  # Initialize dictionary with single-character sequences
    dict_size = 256
    current_string = ""
    compressed = []

    for char in text:
        combined_string = current_string + char
        if combined_string in dictionary:
            current_string = combined_string
        else:
            # Output the code for the longest prefix in the dictionary
            compressed.append(dictionary[current_string])
            # Add new sequence to the dictionary
            dictionary[combined_string] = dict_size
            dict_size += 1
            current_string = char

    # Output the code for the last string if necessary
    if current_string:
        compressed.append(dictionary[current_string])

    return compressed

def lzw_decompress(compressed):
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256
    current_string = chr(compressed.pop(0))
    decompressed = [current_string]

    for code in compressed:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Bad compressed code")

        decompressed.append(entry)

        dictionary[dict_size] = current_string + entry[0]
        dict_size += 1

        current_string = entry

    return ''.join(decompressed)

def get_file_size(file_path):
    return os.path.getsize(file_path)


from tkinter import Tk, filedialog




# GUI Implementation
def compress_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    algorithm = algorithm_var.get()
    if algorithm not in ("RLE", "LZW", "Huffman"):
        messagebox.showerror("Error", "Please select a compression algorithm.")
        return

    # Allow the user to save output as either text or binary
    output_extension = ".bin" if file_type_var.get() == "Binary" else ".txt"
    file_types = [("Binary Files", "*.bin")] if file_type_var.get() == "Binary" else [("Text Files", "*.txt")]
    output_path = filedialog.asksaveasfilename(defaultextension=output_extension, filetypes=file_types)

    if not output_path:
        return

    with open(file_path, 'r') as file:
        text = file.read()

    if algorithm == "RLE":
        compressed_text = rle_compress(text)
        with open(output_path, 'w') as file:
            file.write(compressed_text)
        compressed_size = len(compressed_text) * 8
    elif algorithm == "LZW":
        compressed_text = lzw_compress(text)
        compressed_size = sum(len(bin(code)) - 2 for code in compressed_text)  # Calculate LZW compressed size
        compressed_text = ','.join(map(str, compressed_text))
        with open(output_path, 'w') as file:
            file.write(compressed_text)
    elif algorithm == "Huffman":
        compressed_data = huffman_compress(text)
        with open(output_path, 'wb' if file_type_var.get() == "Binary" else 'w') as file:
            if file_type_var.get() == "Binary":
                file.write(compressed_data)
            else:
                file.write(str(compressed_data))  # Save serialized data as a text representation
        tree_and_data = pickle.loads(compressed_data)
        compressedData = tree_and_data["data"]
        compressed_size = len(compressedData) * 8

    original_size = len(text) * 8  # Bits

    messagebox.showinfo("Compression Completed", f"Original size: {original_size} bits\nCompressed size: {compressed_size} bits")

def decompress_file():

    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if not file_path:
        return

    algorithm = algorithm_var.get()
    if algorithm not in ("RLE", "LZW", "Huffman"):
        messagebox.showerror("Error", "Please select a decompression algorithm.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if not output_path:
        return

    with open(file_path, 'rb' if file_path.endswith('.bin') else 'r') as file:
        compressed_text = file.read()

    if algorithm == "RLE":
        decompressed_text = rle_decompress(compressed_text if isinstance(compressed_text, str) else compressed_text.decode('utf-8'))
        compressed_size = len(compressed_text) * 8  # Bits
    elif algorithm == "LZW":
        if isinstance(compressed_text, str):
            # compressed_text is already a string
            pass
        else:
            # Decode the compressed_text if it's not a string
            compressed_text = compressed_text.decode('utf-8')

        compressed_numbers = list(map(int, compressed_text.split(',')))
        decompressed_text = lzw_decompress(compressed_numbers)
        compressed_text = lzw_compress(decompressed_text)
        compressed_size = sum(len(bin(code)) - 2 for code in compressed_text)
    elif algorithm == "Huffman":
        decompressed_text = huffman_decompress(compressed_text if isinstance(compressed_text, bytes) else bytes(eval(compressed_text)))
        compressed_data = huffman_compress(decompressed_text)
        tree_and_data = pickle.loads(compressed_data)
        compressedData = tree_and_data["data"]
        compressed_size = len(compressedData) * 8

    with open(output_path, 'w') as file:
        file.write(decompressed_text)

    decompressed_size = len(decompressed_text) * 8  # Bits

    messagebox.showinfo("Decompression Completed", f"Compressed size: {compressed_size} bits\nDecompressed size: {decompressed_size} bits")

# Main Application
def main():
    global algorithm_var
    global file_type_var

    root = tb.Window(themename="solar")
    root.title("Compression and Decompression GUI")
    root.geometry("900x700")

    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Times New Roman", 16, "bold"), padding=[8, 5])
    style.map("TNotebook.Tab",
              background=[('selected', '#2980b9')],
              foreground=[('selected', 'black')])

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    # Compression Tab
    compress_tab = ttk.Frame(notebook)
    notebook.add(compress_tab, text="Compress")

    compress_label = ttk.Label(compress_tab, text="Select a File to Compress and a Compression Algorithm:",
                               font=("Times New Roman", 14, "bold"))
    compress_label.pack(pady=10)

    algorithm_var = tk.StringVar(value="RLE")
    compression_frame = ttk.Labelframe(compress_tab, text="Algorithms")
    compression_frame.pack(fill='x', padx=20, pady=10)

    rle_button = ttk.Radiobutton(compression_frame, text="RLE", variable=algorithm_var, value="RLE")
    rle_button.pack(anchor="w", padx=10, pady=5)

    lzw_button = ttk.Radiobutton(compression_frame, text="LZW", variable=algorithm_var, value="LZW")
    lzw_button.pack(anchor="w", padx=10, pady=5)

    huffman_button = ttk.Radiobutton(compression_frame, text="Huffman", variable=algorithm_var, value="Huffman")
    huffman_button.pack(anchor="w", padx=10, pady=5)

    compress_button = ttk.Button(compress_tab, text="Compress File", command=compress_file)
    compress_button.pack(pady=20)

    file_type_var = tk.StringVar(value="Binary")
    file_type_label = ttk.Label(compress_tab, text="Choose a File Type for Saving:",
                                font=("Times New Roman", 14, "bold"))
    file_type_label.pack(pady=10)

    file_type_frame = ttk.Labelframe(compress_tab, text="File Types")
    file_type_frame.pack(fill='x', padx=20, pady=10)

    binary_button = ttk.Radiobutton(file_type_frame, text="Binary", variable=file_type_var, value="Binary")
    binary_button.pack(anchor="w", padx=10, pady=5)

    text_button = ttk.Radiobutton(file_type_frame, text="Text", variable=file_type_var, value="Text")
    text_button.pack(anchor="w", padx=10, pady=5)

    # Decompression Tab
    decompress_tab = ttk.Frame(notebook)
    notebook.add(decompress_tab, text="Decompress")

    decompress_label = ttk.Label(decompress_tab, text="Select a File to Decompress and a Decompression Algorithm:",
                                 font=("Times New Roman", 14, "bold"))
    decompress_label.pack(pady=10)

    rle_button = ttk.Radiobutton(decompress_tab, text="RLE", variable=algorithm_var, value="RLE")
    rle_button.pack(anchor="w", padx=10, pady=5)

    lzw_button = ttk.Radiobutton(decompress_tab, text="LZW", variable=algorithm_var, value="LZW")
    lzw_button.pack(anchor="w", padx=10, pady=5)

    huffman_button = ttk.Radiobutton(decompress_tab, text="Huffman", variable=algorithm_var, value="Huffman")
    huffman_button.pack(anchor="w", padx=10, pady=5)

    decompress_button = ttk.Button(decompress_tab, text="Decompress File", command=decompress_file)
    decompress_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()