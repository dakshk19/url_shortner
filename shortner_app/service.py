import base64
import hashlib


def create_short_link(original_url: str):
    
    to_encode = f"{original_url}"

    b64_encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(to_encode.encode()).digest()
    ).decode()
    return b64_encoded_str[:7]