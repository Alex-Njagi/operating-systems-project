class InMemoryFile:
    """
    This class represents a single openable file stored entirely in memory.
    Every file keeps track of:
      - its byte contents
      - the current read/write position (like a real file handle)
      - whether it's closed
    """
    def __init__(self):
        self.content = bytearray()     # raw bytes of the file
        self.position = 0              # current read/write cursor
        self.closed = False            # whether file is closed


class InMemoryFileSystem:
    """
    A tiny in-memory file system that mimics the behavior of real file operations:
       open(path, mode)  -> returns a file object
       read(file, size)  -> returns string
       write(file, data) -> writes string
       close(file)       -> closes the file

    Supported modes:
       'r'  - read existing file
       'w'  - create new file (overwrite if exists)
       'a'  - append to existing file (create if missing)
    """
    def __init__(self):
        # Maps file paths (strings) to InMemoryFile objects
        self.files = {}

    def open(self, path, mode = "r"):
        """
        Opens a file with the given mode.
        Behaves similarly to built-in Python file modes, but simplified.
        """
        if mode == "r":
            # The file must already exist for reading
            if path not in self.files:
                raise FileNotFoundError("File doesn't exist.")

            file = self.files[path]
            file.position = 0      # reset cursor to start
            file.closed = False
            return file

        elif mode == "w":
            # Create a new file OR overwrite an existing one
            self.files[path] = InMemoryFile()
            return self.files[path]

        elif mode == "a":
            # Append mode:
            #   - If file doesn't exist → create it
            #   - Move cursor to end for appending
            if path not in self.files:
                self.files[path] = InMemoryFile()

            file = self.files[path]
            file.position = len(file.content)  # jump to end for appending
            file.closed = False
            return file

        else:
            # Only 'r', 'w', and 'a' are supported in this simple system
            raise ValueError("Unsupported mode.")

    def read(self, file, size = -1):
        """
        Reads `size` characters from the file.
        If size is -1, read everything from the current position to the end.
        """
        if file.closed:
            raise ValueError("Cannot read a closed file.")

        # If size < 0 → read everything left
        if size < 0:
            size = len(file.content) - file.position

        # Determine read boundaries
        start = file.position
        end = min(start + size, len(file.content))

        # Extract bytes
        data = file.content[start:end]

        # Move cursor forward
        file.position = end

        # Convert bytes → string
        return data.decode("utf-8")

    # =========================== WRITE AND CLOSE OPERATIONS ===================================

    # def write(self, file, data):
    #     """
    #     Writes a string into the file at the current cursor position.
    #     Extends the file automatically if necessary.
    #     """
    #     if file.closed:
    #         raise ValueError("Cannot write to a closed file.")

    #     # Convert incoming string → bytes
    #     data_bytes = data.encode("utf-8")

    #     start = file.position
    #     end = start + len(data_bytes)

    #     # If writing past the current file length,
    #     # extend with zero bytes (like sparse files)
    #     if end > len(file.content):
    #         file.content.extend(b"\x00" * (end - len(file.content)))

    #     # Overwrite/insert bytes where the cursor currently is
    #     file.content[start:end] = data_bytes

    #     # Move pointer forward to end of written data
    #     file.position = end

    # def close(self, file):
    #     """
    #     Marks the file as closed. After this, read/write not allowed.
    #     """
    #     file.closed = True

# ---------------------------
# CLI Interface
# ---------------------------

def run_cli():
    fs = InMemoryFileSystem()
    open_file = None
    open_path = None

    print("=== In-Memory File System CLI ===")
    print("Commands: open, read, write, close, list, exit")
    print("Kindly choose a command to start with")
    print("---------------------------------")

    while True:
        cmd = input(">>> ").strip().lower()

        if cmd == "exit":
            print("Goodbye!")
            break

        elif cmd == "open":
            if open_file and not open_file.closed:
                print(f"A file is already open: '{open_path}'. Close it first.")
                continue

            path = input("File path: ")
            mode = input("Mode (r/w/a): ")

            try:
                open_file = fs.open(path, mode)
                open_path = path
                print(f"Opened '{path}' in mode '{mode}'.")
            except Exception as e:
                print("Error:", e)

        elif cmd == "read":
            if not open_file or open_file.closed:
                print("No open file to read from.")
                continue

            size = input("Bytes to read (-1 for all): ")
            size = int(size)

            try:
                data = fs.read(open_file, size)
                print("READ:", repr(data))
            except Exception as e:
                print("Error:", e)

        # elif cmd == "write":
        #     if not open_file or open_file.closed:
        #         print("No open file to write to.")
        #         continue

        #     data = input("Write data: ")

        #     try:
        #         fs.write(open_file, data)
        #         print("Data written.")
        #     except Exception as e:
        #         print("Error:", e)

        # elif cmd == "close":
        #     if not open_file:
        #         print("No open file to close.")
        #         continue

        #     fs.close(open_file)
        #     print(f"Closed '{open_path}'.")
        #     open_file = None
        #     open_path = None

        elif cmd == "list":
            if not fs.files:
                print("No files currently exist.")
            else:
                print("Files:")
                for name in fs.files:
                    print(" -", name)

        else:
            print("Unknown command. Try: open, read, write, close, list, exit")


# Run the CLI
if __name__ == "__main__":
    run_cli()