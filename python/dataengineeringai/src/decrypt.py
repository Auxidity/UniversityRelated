from Crypto.Cipher import AES

def read_encrypted_file():
    with open("message.txt", "rb") as file:
        return file.read()

def decrypt(encrypted_message):
    key = b'Sixteen byte keyyyyyyyyyyyyyyyy!'
    iv = encrypted_message[:12]
    tag = encrypted_message[-16:]
    ciphertext = encrypted_message[12:-16]

    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except ValueError:
        return "Decryption failed or message was tampered with"

def write_to_file(secret):
    with open("decrypted.txt", "w") as file:
        file.write(secret)

if __name__ == "__main__":
    message = decrypt(read_encrypted_file())
    print(f"{message}")
    //Optionally decrypt message to another file, uncomment the line below to do so
    //write_to_file(message)
