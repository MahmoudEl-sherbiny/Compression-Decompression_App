
# Compression and Decompression GUI Tool

This project provides a graphical user interface (GUI) tool for compressing and decompressing text files using popular algorithms such as **Huffman**, **Run-Length Encoding (RLE)**, and **Lempel-Ziv-Welch (LZW)**. The GUI is built using Python's Tkinter and ttkbootstrap libraries. The tool supports both **text** and **binary** file formats for compressed data.

---

## Features

- **Compression Algorithms**:
  - **RLE (Run-Length Encoding)**: Compresses data by replacing consecutive repeating characters with the character followed by the count of repetitions.
  - **LZW (Lempel-Ziv-Welch)**: A dictionary-based algorithm that replaces sequences of characters with dictionary indices.
  - **Huffman Coding**: A variable-length encoding algorithm that assigns shorter codes to more frequent characters.

- **Decompression**: Supports decompression of files compressed using the above algorithms.

- **GUI Interface**: Simple and intuitive interface for selecting files to compress/decompress and choosing the algorithm.

- **File Format**: Allows saving the output in **text** or **binary** formats.

---

## Requirements

- **Python 3.x**
- **Libraries**:
  - `tkinter` (for GUI)
  - `ttkbootstrap` (for enhanced styling)
  - `heapq` (for implementing Huffman coding)
  - `pickle` (for serializing and deserializing data)
  - `os`, `collections` (standard Python libraries)

---

## Installation

1. **Clone the repository** or download the script:
   ```bash
   git clone https://github.com/yourusername/compression-gui.git
   ```

2. **Install necessary dependencies** (make sure you have Python 3 installed):
   ```bash
   pip install ttkbootstrap
   ```

---

## How to Use

1. **Run the Application**:
   - Open a terminal and navigate to the project directory.
   - Run the Python script:
     ```bash
     python compression_gui.py
     ```

2. **Select a File**:
   - Click on the "Compress" tab to choose a file to compress, or the "Decompress" tab to choose a file to decompress.
   - Choose one of the supported algorithms (**RLE**, **LZW**, or **Huffman**).
   
3. **Compression**:
   - Choose the compression algorithm (RLE, LZW, or Huffman).
   - Select the file format (Text or Binary) for the output.
   - The tool will display the original file size and the compressed file size.

4. **Decompression**:
   - Select a compressed file and the appropriate decompression algorithm.
   - The tool will decompress the file and display the sizes of the compressed and decompressed files.

---

## Code Explanation

### Classes & Functions:

1. **HuffmanNode Class**: Represents each node in the Huffman tree used for encoding and decoding.
   
2. **Huffman Compression & Decompression**:
   - `huffman_compress(text)`: Compresses a given text using Huffman coding.
   - `huffman_decompress(serialized_data)`: Decompresses a Huffman-compressed file.

3. **RLE Compression & Decompression**:
   - `rle_compress(data)`: Compresses a string using Run-Length Encoding.
   - `rle_decompress(data)`: Decompresses data encoded using RLE.

4. **LZW Compression & Decompression**:
   - `lzw_compress(text)`: Compresses text using LZW compression.
   - `lzw_decompress(compressed)`: Decompresses data encoded using LZW.

5. **File Size Calculation**:
   - `get_file_size(file_path)`: Returns the size of a file in bytes.

6. **GUI Components**:
   - The GUI is built using Tkinter and ttkbootstrap. The user can choose a file, compression algorithm, and file type (binary or text).
   - The tool shows the original and compressed file sizes in the GUI.

---

## File Structure

- **compression_gui.py**: Main Python script containing the compression and decompression logic as well as the Tkinter GUI.
- **letter_templates/**: Folder containing any predefined letter templates used in the tool (optional).
- **birthdays.csv**: Sample CSV file containing birthday data (optional).

---

## Example

1. **Compressing a file**:
   - Open the "Compress" tab.
   - Select a `.txt` file.
   - Choose the compression algorithm (e.g., Huffman).
   - Save the compressed file in the desired format (text or binary).
   - View the original and compressed sizes.

2. **Decompressing a file**:
   - Open the "Decompress" tab.
   - Select the compressed file.
   - Choose the appropriate decompression algorithm (e.g., Huffman).
   - View the decompressed content.

---

## License

This project is open source and available under the MIT License.
