from Crypto.Cipher import AES

def get_static_IV():
    return b'\x00' * 12

def write_to_file(secret):
    with open("message.txt", "wb") as file:
        file.write(secret)

def encrypt():
    key = b'Sixteen byte keyyyyyyyyyyyyyyyy!'
    secret = "A very secret message."
    cipher = AES.new(key, AES.MODE_GCM, nonce = get_static_IV())
    ciphertext, tag = cipher.encrypt_and_digest(secret.encode())
    encrypted_message = get_static_IV() + ciphertext + tag
    return encrypted_message

if __name__ == "__main__":
    write_to_file(encrypt())
