import secrets

def create_api_key() -> str:
    """Generates a secure, URL-safe, 32-byte (approx. 43 char) API key."""
    # 32 bytes gives a long random string, good enough for most apps
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    api_key = create_api_key()
    
    # Copy this key and set it as the API_SECRET_KEY environment variable 
    # on your deployment platform (Render, Hugging Face, etc.).
    print("---------------------------------------------------------")
    print("   🔑 YOUR NEW API KEY (USE THIS FOR PRODUCTION):")
    print(f"   {api_key}")
    print("---------------------------------------------------------")