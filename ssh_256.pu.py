
"""
aes_256_gcm.py

Implements AES-256 GCM (Galois/Counter Mode) encryption and decryption
using the PyCryptodome library. This mode provides both confidentiality 
(encryption) and authenticity (integrity check via the tag).
"""

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import binascii
import sys

# The size of the key for AES-256 must be 32 bytes (256 bits).
KEY_SIZE = 32

def aes_256_gcm_encrypt(plaintext: bytes, key: bytes):
    """
    Encrypts plaintext using AES-256 in GCM mode.

    :param plaintext: The data to encrypt (bytes).
    :param key: The 32-byte encryption key (bytes).
    :return: A tuple of (nonce, ciphertext, tag) in bytes.
    """
    if len(key) != KEY_SIZE:
        raise ValueError(f"Key size must be {KEY_SIZE} bytes for AES-256.")

    # Create a new AES cipher instance in GCM mode.
    # The nonce (IV) is generated automatically and must be unique for each encryption.
    cipher = AES.new(key, AES.MODE_GCM)
    
    # Encrypt the data and generate the authentication tag.
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # The nonce, ciphertext, and tag are all required for decryption.
    return cipher.nonce, ciphertext, tag

def aes_256_gcm_decrypt(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes):
    """
    Decrypts ciphertext using AES-256 in GCM mode and verifies the tag.

    :param nonce: The unique nonce used during encryption (bytes).
    :param ciphertext: The encrypted data (bytes).
    :param tag: The authentication tag (bytes).
    :param key: The 32-byte encryption key (bytes).
    :return: The decrypted plaintext (bytes) or raises an error on failure.
    """
    if len(key) != KEY_SIZE:
        raise ValueError(f"Key size must be {KEY_SIZE} bytes for AES-256.")
        
    # Create a new AES cipher instance using the key and the original nonce.
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Decrypt the data and verify the authentication tag.
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
    except ValueError as e:
        # If the key, nonce, or data/tag has been tampered with, the verification fails.
        # This is the security feature of GCM.
        raise ValueError(f"Decryption failed: Authentication tag verification failed. Data may be incorrect or tampered. Detail: {e}")

# --- Example Usage (When run directly) ---
if __name__ == "__main__":
    
    # Check if the necessary library is installed
    try:
        # Check if PyCryptodome is available
        from Cryptodome.Cipher import AES
    except ImportError:
        print("Error: PyCryptodome library is not installed.")
        print("Please install it using: pip install pycryptodome")
        sys.exit(1)

    print("## AES-256 GCM Encryption/Decryption Demonstration ##")
    print("-" * 50)
    
    try:
        # **1. Generate a secure, random 256-bit (32-byte) key**
        encryption_key = get_random_bytes(KEY_SIZE)
        print(f"🔑 Key (32 bytes): {binascii.hexlify(encryption_key).decode()}")

        # Data to be encrypted (must be in bytes)
        original_data = b"This is the secret message that needs AES-256 protection."
        print(f"\nOriginal Data: '{original_data.decode()}'")

        # **2. Encrypt the data**
        nonce, ciphertext, tag = aes_256_gcm_encrypt(original_data, encryption_key)

        print("\n--- Encryption Results ---")
        print(f"Nonce (IV): {binascii.hexlify(nonce).decode()}")
        print(f"Ciphertext: {binascii.hexlify(ciphertext).decode()}")
        print(f"Tag (Auth): {binascii.hexlify(tag).decode()}")
        print("--------------------------")

        # **3. Decrypt the data**
        decrypted_data = aes_256_gcm_decrypt(nonce, ciphertext, tag, encryption_key)
        
        print(f"\nDecrypted Data: '{decrypted_data.decode()}'")

        # **4. Tamper Example (Integrity Check)**
        print("\n--- Tamper Test (Simulating an attack) ---")
        try:
            # Change a single byte in the ciphertext
            tampered_ciphertext = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0x01])
            print(f"Attempting decryption with tampered ciphertext...")
            aes_256_gcm_decrypt(nonce, tampered_ciphertext, tag, encryption_key)
            print("ERROR: Tampered data was decrypted successfully (should not happen in GCM!)")
        except ValueError as e:
            print("SUCCESS: Decryption failed!")
            print(f"Reason: {e}")
            
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")