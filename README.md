Python Reverse Shell Client
This is the client.py script that connects to a remote server and supports file uploads, downloads, and executing shell commands on the client machine.

Features
File Upload: The client can send a file to the server when requested.
File Download: The client can download a file from the server when requested.
Shell Execution: The client can execute shell commands sent by the server and return the output.
Requirements
Python 3.x
No external dependencies (only built-in modules)
Setup
Step 1: Edit client.py
Before running client.py, update the HOST variable to the IP address of the server you are connecting to.

python
Copy code
HOST = '<server_ip>'
The PORT should match the port the server is listening on:

python
Copy code
PORT = 2222  # Change if necessary
Step 2: Run client.py
Once the server IP and port are configured, you can run the client script as follows:

bash
Copy code
python3 client.py
The client will automatically connect to the server and wait for instructions (such as file uploads, downloads, or shell commands).

Features and Usage
1. File Upload
The client can receive a command from the server to upload a file. Once the command is received, the file is transferred from the client to the server.

2. File Download
When the server sends a download request, the client receives the file from the server and saves it to the specified path.

3. Shell Commands Execution
The client listens for shell commands from the server and executes them on the client machine, sending the output back to the server in real time.

Example Commands
Upload a File from the Client to the Server

The server sends the command upload, and the client starts the upload process by sending the specified file to the server.
Download a File from the Server to the Client

The server sends the command download, and the client receives and saves the file at the given path.
Execute a Shell Command

The server sends any shell command (e.g., ls, dir, etc.), and the client executes the command and returns the output to the server.
Error Handling
If there is an error in changing directories (cd), the client sends a failure message back to the server.
If the file doesn't exist or cannot be accessed, appropriate error handling is performed.
Legal Disclaimer
This script is intended for educational purposes only. Unauthorized use in systems you do not own or have explicit permission to control is illegal. The author is not responsible for any misuse or damage caused by this tool.

License
This project is licensed under the MIT License.
