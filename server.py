# Server-side code (Run this on the machine with the camera, e.g., Raspberry Pi)
import cv2
import socket
import pickle
import struct
import platform # Added for checking OS specific IP access

# Initialize the camera
camera = cv2.VideoCapture(0) # 0 for the first camera, adjust if needed
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a socket for streaming
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Use '0.0.0.0' to listen on all available network interfaces
# NOTE: The client needs to connect to the actual IP address of this machine.
host_ip = '0.0.0.0'
port = 9999
socket_address = (host_ip, port)

server_socket.bind(socket_address)
server_socket.listen(5)

# Find the machine's actual local IP address for display
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
except Exception:
    local_ip = '127.0.0.1 (Check network settings)'

print(f"Server is ready.")
print(f"Client should connect to IP: **{local_ip}** on Port: **{port}**")

client_socket, addr = server_socket.accept()
print(f"Got connection from {addr}")

# Main streaming loop
try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to read frame from camera.")
            break

        # Serialize frame
        data = pickle.dumps(frame)

        # Send message size (using 'L' for unsigned long, which is 4 bytes on many systems)
        message_size = struct.pack("<L", len(data)) # Use little-endian for cross-platform compatibility

        # Send frame size and then the frame data
        client_socket.sendall(message_size + data)

        # Optional: Display frame on Server for testing
        # cv2.imshow('Server Stream', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Cleanup
    print("Cleaning up resources...")
    camera.release()
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()
