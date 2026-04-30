import hashlib
import logging
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import os

logger = logging.getLogger("")

BS = 16


def pad_data(data):
    """PKCS7 padding for AES"""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data)
    padded_data += padder.finalize()
    return padded_data


def unpad_data(data):
    """Remove PKCS7 padding"""
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data)
    unpadded_data += unpadder.finalize()
    return unpadded_data


def generate_iv():
    """Generate a secure random IV"""
    return os.urandom(16)


class AESCipher(object):
    def __init__(self, key):
        if isinstance(key, str):
            key = key.encode()
        # Ensure key is 32 bytes for AES-256
        if len(key) < 32:
            key = key.ljust(32, b'\0')
        elif len(key) > 32:
            key = key[:32]
        self.key = key

    def encrypt(self, message):
        if isinstance(message, str):
            message = message.encode()

        # Use a fixed IV of zeros (as in original code)
        iv = b'\x00' * 16
        padded_data = pad_data(message)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, enc):
        enc_data = base64.b64decode(enc)
        iv = b'\x00' * 16

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(enc_data) + decryptor.finalize()

        unpadded_data = unpad_data(decrypted)
        return unpadded_data.decode('utf-8')


def aes_encrypt_data(data, key):
    if not key:
        key = Fernet.generate_key().decode()
    fernet = Fernet(key.encode() if isinstance(key, str) else key)
    return fernet.encrypt(data.encode()).decode()


def aes_decrypt_data(data, key=None):
    if not key:
        raise ValueError("Key is required for decryption")
    fernet = Fernet(key.encode() if isinstance(key, str) else key)
    if isinstance(data, bytes):
        return fernet.decrypt(data).decode()
    return fernet.decrypt(data.encode()).decode()


def hash_string_with_length(input_string, length=None):
    # Choose a hash function (SHA-256 in this case)
    hash_func = hashlib.sha256()

    # Update the hash object with the input string
    hash_func.update(input_string.encode())

    # Get the hexadecimal digest of the hash and truncate to the desired length
    if length:
        hashed_string = hash_func.hexdigest()[:length]
    else:
        hashed_string = hash_func.hexdigest()

    return hashed_string


def md5_hash(data):
    """Create MD5 hash using hashlib instead of pycrypto"""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


def encrypt_data(message, secret=''):
    if isinstance(message, str):
        message_bytes = message.encode()
    else:
        message_bytes = message

    if not secret:
        key = md5_hash(message_bytes)
    else:
        key = secret
    return AESCipher(key).encrypt(message_bytes)


def decrypt_data(message, code=''):
    try:
        if not code:
            key = md5_hash(message.encode())
        else:
            key = code
        result = AESCipher(key).decrypt(message)
        return result
    except Exception as e:
        logger.error(f"Error in decrypt_data: {str(e)}")
        raise


def padding_secret(x):
    x = str(x)
    if len(x) > 32:
        return x[:32]
    else:
        return x.zfill(32)
