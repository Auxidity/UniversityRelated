1. potential workaround for recv related issues on different platforms. Maybe something like :

```python
response = b''  # Initialize an empty byte string to store the response
while True:
    chunk = client_socket.recv(1024)  # Receive a chunk of data
    if not chunk:
        break  # If no more data is received, exit the loop
    response += chunk  # Append the received chunk to the response
response = response.decode()  # Decode the byte string to a Unicode string
print(response)
```

2. Fix led control

3. look into moving speech recognition away from server to client, and have api calls & tts be done on server.

172.27.227.235