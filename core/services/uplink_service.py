"""
MacGyver Uplink Service
Secure, ephemeral P2P data transfer using standard libraries.
"""
import json
import urllib.request
import urllib.parse
import urllib.error
import secrets
import hashlib
import base64
import gzip
import hmac
from typing import Dict, Tuple, Optional, Union

class UplinkService:
    """
    Handles secure data transfer via ephemeral file host (file.io).
    Uses standard library crypto (PBKDF2 + XOR Stream) to avoid dependencies.
    """
    
    # Ephemeral host API (paste.rs)
    UPLOAD_URL = "https://paste.rs"
    
    def __init__(self):
        pass
        
    def generate_uplink_code(self, data: Dict, expiry: str = "1d") -> Tuple[bool, str]:
        """
        Encrypts data, uploads to relay (paste.rs), and returns a Magic Code.
        Code Format: MG-{FILE_KEY}-{ENCRYPTION_KEY}
        """
        try:
            # 1. Prepare Data
            json_bytes = json.dumps(data).encode('utf-8')
            compressed = gzip.compress(json_bytes)
            
            # 2. Encrypt
            key = secrets.token_bytes(32)  # 256-bit key
            encrypted_data = self._encrypt(compressed, key)
            
            # Base64 encode for text-based pastebin
            b64_content = base64.b64encode(encrypted_data).decode()
            
            # 3. Upload to paste.rs
            # Just POST the content
            req = urllib.request.Request(self.UPLOAD_URL, data=b64_content.encode())
            req.add_header('User-Agent', 'MacGyver-MultiTool/1.0')
            
            with urllib.request.urlopen(req) as response:
                paste_url = response.read().decode().strip()
                
            if not paste_url.startswith('http'):
                return False, f"Upload failed: {paste_url}"
                
            # Extract ID (last part of URL)
            file_key = paste_url.strip('/').split('/')[-1]
            
            # Encode encryption key to base64url for the code
            enc_key_b64 = base64.urlsafe_b64encode(key).decode().rstrip('=')
            
            magic_code = f"MG-{file_key}-{enc_key_b64}"
            return True, magic_code
            
        except Exception as e:
            return False, str(e)

    def receive_uplink_data(self, magic_code: str) -> Tuple[bool, Union[Dict, str]]:
        """
        Downloads, decrypts, and unpacks data from a Magic Code.
        """
        try:
            # 1. Parse Code
            parts = magic_code.strip().split('-')
            if len(parts) != 3 or parts[0] != "MG":
                return False, "Invalid Code Format"
            
            file_key = parts[1]
            enc_key_b64 = parts[2]
            
            # Restore padding if needed
            enc_key_b64 += '=' * (-len(enc_key_b64) % 4)
            key = base64.urlsafe_b64decode(enc_key_b64)
            
            # 2. Download Raw Content
            download_url = f"{self.UPLOAD_URL}/{file_key}"
            req = urllib.request.Request(download_url)
            req.add_header('User-Agent', 'MacGyver-MultiTool/1.0')
            
            try:
                with urllib.request.urlopen(req) as response:
                    content_b64 = response.read()
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return False, "Data not found or expired"
                return False, f"Download Error: {e.code}"
                
            # Decode Base64 wrapper
            try:
                encrypted_data = base64.b64decode(content_b64)
            except:
                return False, "Invalid data format (Not Base64)"
                
            # 3. Decrypt
            decrypted_compressed = self._decrypt(encrypted_data, key)
            if decrypted_compressed is None:
                return False, "Decryption Failed (Invalid Key or Corrupt Data)"
                
            # 4. Decompress & Parse
            json_bytes = gzip.decompress(decrypted_compressed)
            data = json.loads(json_bytes.decode('utf-8'))
            
            return True, data
            
        except Exception as e:
            return False, str(e)

    def _encrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Encrypts data using a custom stream cipher (HMAC-SHA256 based).
        Format: [Salt(16)][IV(16)][Ciphertext][HMAC(32)]
        """
        salt = secrets.token_bytes(16)
        iv = secrets.token_bytes(16)
        
        # Derive session key
        session_key = hashlib.pbkdf2_hmac('sha256', key, salt, 10000)
        
        # Generate keystream
        keystream = self._generate_keystream(session_key, iv, len(data))
        
        # XOR
        ciphertext = bytes(a ^ b for a, b in zip(data, keystream))
        
        # Calculate HMAC for integrity
        msg = salt + iv + ciphertext
        signature = hmac.new(key, msg, hashlib.sha256).digest()
        
        return msg + signature

    def _decrypt(self, blob: bytes, key: bytes) -> Optional[bytes]:
        """Decrypts data"""
        try:
            # Extract parts
            if len(blob) < 64: # Min size
                return None
                
            signature = blob[-32:]
            msg = blob[:-32]
            
            salt = msg[:16]
            iv = msg[16:32]
            ciphertext = msg[32:]
            
            # Verify HMAC
            expected_sig = hmac.new(key, msg, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected_sig):
                return None
            
            # Derive session key
            session_key = hashlib.pbkdf2_hmac('sha256', key, salt, 10000)
            
            # Generate keystream
            keystream = self._generate_keystream(session_key, iv, len(ciphertext))
            
            # XOR
            plaintext = bytes(a ^ b for a, b in zip(ciphertext, keystream))
            return plaintext
            
        except Exception:
            return None

    def _generate_keystream(self, key: bytes, iv: bytes, length: int) -> bytes:
        """
        Generates a pseudo-random keystream using HMAC-SHA256 counter mode.
        """
        keystream = bytearray()
        counter = 0
        while len(keystream) < length:
            # Hash(Key + IV + Counter)
            block_input = iv + counter.to_bytes(8, 'big')
            block = hmac.new(key, block_input, hashlib.sha256).digest()
            keystream.extend(block)
            counter += 1
        return bytes(keystream[:length])

# Global instance
_uplink_service = None

def get_uplink_service() -> UplinkService:
    global _uplink_service
    if _uplink_service is None:
        _uplink_service = UplinkService()
    return _uplink_service
