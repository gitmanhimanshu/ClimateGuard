"""
Simple Hugging Face Login Script
"""

from huggingface_hub import login, whoami

print("\n🤗 Hugging Face Login")
print("=" * 50)
print("\nGet your token from: https://huggingface.co/settings/tokens")
print("(Create a token with 'write' access)")
print("\n" + "=" * 50 + "\n")

# Try to check if already logged in
try:
    user_info = whoami()
    print(f"✅ Already logged in as: {user_info['name']}")
    print(f"📧 Email: {user_info.get('email', 'N/A')}")
    print("\nYou're ready to deploy!")
except Exception:
    print("❌ Not logged in yet")
    print("\nPlease enter your Hugging Face token:")
    
    try:
        token = input("Token: ").strip()
        
        if token:
            login(token=token, add_to_git_credential=True)
            print("\n✅ Login successful!")
            
            # Verify
            user_info = whoami()
            print(f"👤 Logged in as: {user_info['name']}")
            print("\n🚀 Ready to deploy!")
        else:
            print("\n❌ No token provided")
    except KeyboardInterrupt:
        print("\n\n❌ Login cancelled")
    except Exception as e:
        print(f"\n❌ Login failed: {str(e)}")

print("\n" + "=" * 50)
print("\nNext step: python deploy.py YOUR_USERNAME/climateguard-ai")
print("=" * 50 + "\n")
