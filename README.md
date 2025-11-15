# Memory Based Python File System

<h2>1. Introduction</h2>
- The purpose of this project is to offer a small-scale simulation of a real-life file system. Instead of creating and storing files on a computer hard drive, this system intends to maintain everything in memory (RAM) using Python objects and process to faciliate this.

- To acheive this objective, the following operations have been made possible: <strong>`open, read, write and close`.</strong>

- To fully simulate this memory file system, a simple command-line interface (CLI) has also been created.

<h2>2. The Main Parts of the System</h2>
- The system is composed of three different components that work together to facilitate its functioning for the purposes of this simulation. They are:
    + InMemoryFile: A class which represents a single file (its contents, cursor position, and closed/open state).

    + InMemoryFileSystem: The class that manages all the files and provides functions namely open(), read(), write() and close().

    + CLI interface: The visual interface that allows you to type commands like open, read, write, list, close, exit in this simulation.

- Each of this components will now be effectively broken down below.

<h2>3. The InMemoryFile Class</h2>
- This class functions as our primary container that handles three main things: file content, cursor position and file state.
    <code>
    class InMemoryFile:
        def __init__(self):
            self.content = bytearray()
            self.position = 0
            self.closed = False
    </code>

- The file content is initialised with a byteArray() function that holds the actual file data. The cursor position meanwhile is initialised with a zero value, indicating that the cursor - which is our pointer that'll facilitate reading and writing processes - is at the beginning of the file. Finally, the file state simply indicates whether the file is currently open or closed.

<h2>3. The InMemoryFileSystem Class</h2>
- This class acts as the brain of our simulation which mimics the behavior of real file operations. Essentially, it is the backbone of the system that is used to maintain files made using the previous class hence why it is initialised as:
    <code>
    class InMemoryFileSystem:
        def __init__(self):
            self.files = {}
    </code>

- Since this class is housing all our file operations, it is important to understand how each operation contributes to this filesystem we have created.

    <h3>open(path, mode)</h3>
    - This operation creates or retrieves a file based on mode. These modes include:
        + "r" → read existing file
        + "w" → create or overwrite a file
        + "a" → append to end of file (or create if missing)

    Each file has its cursor set appropriately:
        + “r” → the cursor is at beginning
        + “a” → the cursor is at end
        + “w” → new file therefore the cursor is at beginning

    <h3>read(file, size)</h3>
    - This operation reads from the file starting at its current cursor position and exploring its contents by moving the cursor forward like a real file would. If the size = -1 i.e. all, it reads everything to the end.

    <h3>write(file, data)</h3>
    - This operation writes data where the cursor is all while moving the cursor to the end of what it wrote. If writing extends past the end of the file, the file automatically grows.

    <h3>close(file)</h3>
    - This operation marks the file as closed thereby preventing further reading or writing until it is reopened.

<h2>4. The Command-Line Interface (CLI)</h2>
- To complete this simulation, a small interactive shell that functions in the command-line was created to faciliate the usage of the file system. This interface currently houses the following commands:
    + open → choose filename + mode
    + read → read bytes from open file
    + write → write to open file
    + close → close current file
    + list → show all stored files
    + exit → quit

- Below is a sample usage of the interface to carry out our core operations:
    <code>
    >>> open
    File path: notes.txt
    Mode (r/w/a): w
    Opened 'notes.txt' in mode 'w'.

    >>> write
    Write data: Hello User!
    Data written.

    >>> close
    Closed 'notes.txt'.

    >>> open
    File path: notes.txt
    Mode (r/w/a): r
    Opened 'notes.txt' in mode 'r'.

    >>> read
    Bytes to read (-1 for all): -1
    READ: 'Hello User!'
    </code>