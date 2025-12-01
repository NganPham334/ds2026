import sys
import os
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

def run_server(port):
    print(f"Starting RPC Server on port {port}...")
    server = SimpleXMLRPCServer(('0.0.0.0', port), allow_none=True)

    def upload_chunk(filename, binary_data):
        with open(f"recv_{filename}", 'ab') as f:
            f.write(binary_data.data)
        return True

    server.register_function(upload_chunk, "upload_chunk")

    try:
        print("Ready to receive files (Ctrl+C to stop).")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

def run_client(host, port, filepath):
    if not os.path.exists(filepath):
        print("Error: File not found.")
        return

    filename = os.path.basename(filepath)
    proxy = xmlrpc.client.ServerProxy(f'http://{host}:{port}')

    print(f"Sending {filename} to {host}:{port}...")

    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            wrapped_chunk = xmlrpc.client.Binary(chunk)
            try:
                proxy.upload_chunk(filename, wrapped_chunk)
            except Exception as e:
                print(f"RPC Error: {e}")
                sys.exit(1)

    print("Transfer complete.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python rpc_transfer.py server <port>")
        print("  Client: python rpc_transfer.py client <ip> <port> <file>")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == 'server':
        port = int(sys.argv[2])
        run_server(port)
    elif mode == 'client':
        ip = sys.argv[2]
        port = int(sys.argv[3])
        file = sys.argv[4]
        run_client(ip, port, file)