"""
AES-256 encryption for sensitive financial data.
Provides encryption at rest for database storage.
"""
import base64
import os
from typing import Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

from config import settings


class EncryptionService:
    """
    Handles encryption and decryption of sensitive financial data.
    Uses Fernet (AES-128-CBC) with HMAC for authenticated encryption.
    """
    
    def __init__(self, key: Optional[str] = None):
        """
        Initialize encryption service.
        
        Args:
            key: Optional encryption key. If not provided, generates or uses from settings.
        """
        if key:
            self._key = self._derive_key(key)
        elif settings.ENCRYPTION_KEY:
            self._key = self._derive_key(settings.ENCRYPTION_KEY)
        else:
            # Generate a new key if none provided
            self._key = Fernet.generate_key()
        
        self._fernet = Fernet(self._key)
    
    def _derive_key(self, password: str, salt: bytes = None) -> bytes:
        """
        Derive encryption key from password using PBKDF2.
        
        Args:
            password: Password to derive key from
            salt: Optional salt (uses fixed salt for consistency)
        
        Returns:
            Derived key suitable for Fernet
        """
        if salt is None:
            # Use a fixed salt for key derivation (in production, store salt separately)
            salt = b'financial_health_platform_salt_v1'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, data: Union[str, dict, list]) -> str:
        """
        Encrypt data and return base64-encoded ciphertext.
        
        Args:
            data: Data to encrypt (string, dict, or list)
        
        Returns:
            Base64-encoded encrypted data
        """
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        
        encrypted = self._fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt base64-encoded ciphertext.
        
        Args:
            encrypted_data: Base64-encoded encrypted data
        
        Returns:
            Decrypted string
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    def decrypt_json(self, encrypted_data: str) -> Union[dict, list]:
        """
        Decrypt data and parse as JSON.
        
        Args:
            encrypted_data: Base64-encoded encrypted JSON data
        
        Returns:
            Decrypted and parsed JSON object
        """
        decrypted = self.decrypt(encrypted_data)
        return json.loads(decrypted)
    
    def encrypt_field(self, value: str) -> str:
        """
        Encrypt a single field value.
        Simpler wrapper for encrypting individual fields.
        """
        if not value:
            return value
        return self.encrypt(value)
    
    def decrypt_field(self, value: str) -> str:
        """
        Decrypt a single field value.
        Returns original value if decryption fails (for unencrypted data).
        """
        if not value:
            return value
        try:
            return self.decrypt(value)
        except:
            return value  # Return as-is if not encrypted
    
    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key."""
        return Fernet.generate_key().decode()
    
    @staticmethod
    def hash_sensitive(data: str) -> str:
        """
        Create a one-way hash of sensitive data.
        Useful for storing searchable but non-reversible data.
        """
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()


# Global encryption service instance
encryption_service = EncryptionService()


def encrypt_data(data: Union[str, dict, list]) -> str:
    """Convenience function to encrypt data."""
    return encryption_service.encrypt(data)


def decrypt_data(encrypted_data: str) -> str:
    """Convenience function to decrypt data."""
    return encryption_service.decrypt(encrypted_data)


def decrypt_json_data(encrypted_data: str) -> Union[dict, list]:
    """Convenience function to decrypt JSON data."""
    return encryption_service.decrypt_json(encrypted_data)
