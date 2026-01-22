import socket
import struct

RTP_PORT = 5004  
RTP_HOST = "0.0.0.0"  

RTP_HEADER_SIZE = 12 

def parse_rtp_packet(data):
    """Parse the RTP packet header and print out the details"""
    if len(data) < RTP_HEADER_SIZE:
        print("Received a packet that's too small to be a valid RTP packet.")
        return

    rtp_header = struct.unpack("!BBHII", data[:RTP_HEADER_SIZE])

    version = (rtp_header[0] >> 6) & 0x03  
    padding = (rtp_header[0] >> 5) & 0x01 
    extension = (rtp_header[0] >> 4) & 0x01  
    csrc_count = rtp_header[0] & 0x0F  
    marker = (rtp_header[1] >> 7) & 0x
    payload_type = rtp_header[1] & 0x
    sequence_number = rtp_header[2] 
    timestamp = rtp_header[3]  
    ssrc = rtp_header[4]  

    print(f"Received RTP packet:")
    print(f"Version: {version}, Padding: {padding}, Extension: {extension}, CSRC Count: {csrc_count}")
    print(f"Marker: {marker}, Payload Type: {payload_type}")
    print(f"Sequence Number: {sequence_number}, Timestamp: {timestamp}, SSRC: {ssrc}")
    print(f"Payload data (length {len(data) - RTP_HEADER_SIZE}): {data[RTP_HEADER_SIZE:]}\n")

def start_rtp_receiver(host=RTP_HOST, port=RTP_PORT):
    """Start listening for RTP packets"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Listening for RTP packets on {host}:{port}")

    while True:
        data, addr = sock.recvfrom(2048)
        print(f"Received packet from {addr}")
        
        parse_rtp_packet(data)

if __name__ == "__main__":
    start_rtp_receiver()
