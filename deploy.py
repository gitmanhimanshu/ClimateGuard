"""
Deployment script for Hugging Face Spaces
"""

import os
import sys
import shutil
import tempfile
from huggingface_hub import HfApi, create_repo


def deploy_to_huggingface(repo_name: str, token: str = None):
    """
    Deploy ClimateGuard AI to Hugging Face Spaces
    
    Args:
        repo_name: Name for the HF repo (e.g., 'username/climateguard-ai')
        token: HF token (or set HF_TOKEN env variable)
    """
    
    # Try to get token from multiple sources
    if token is None:
        token = os.environ.get('HF_TOKEN')
    
    # Try to use saved credentials if no token
    api = HfApi(token=token) if token else HfApi()
    
    try:
        # Test if we can authenticate
        api.whoami(token=token)
        print("✅ Using Hugging Face credentials")
    except Exception:
        print("❌ Error: Not logged in to Hugging Face")
        print("\nPlease login first:")
        print("  python hf_login.py")
        print("\nOr set token:")
        print("  $env:HF_TOKEN='your_token_here'  # PowerShell")
        return
    
    try:
        # Create repository
        print(f"📦 Creating repository: {repo_name}")
        create_repo(
            repo_id=repo_name,
            token=token,
            repo_type="space",
            space_sdk="docker",
            exist_ok=True
        )
        print("✅ Repository created")
        
        # Create temporary directory for deployment
        print("\n📤 Preparing files for upload...")
        with tempfile.TemporaryDirectory() as temp_dir:
            # Files and folders to copy
            items_to_copy = [
                ('openenv.yaml', 'openenv.yaml'),
                ('models.py', 'models.py'),
                ('server', 'server'),
                ('static', 'static'),
                ('requirements.txt', 'requirements.txt'),
                ('Dockerfile', 'Dockerfile'),
                ('README.md', 'README.md'),
                ('.gitignore', '.gitignore')
            ]
            
            # Copy files to temp directory
            for src, dst in items_to_copy:
                src_path = os.path.join(os.getcwd(), src)
                dst_path = os.path.join(temp_dir, dst)
                
                if os.path.isfile(src_path):
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    print(f"  ✅ Prepared {src}")
                elif os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path)
                    print(f"  ✅ Prepared {src}/")
                else:
                    print(f"  ⚠️  Not found: {src}")
            
            # Upload entire folder
            print("\n📤 Uploading to Hugging Face...")
            import time
            commit_message = f"Update ClimateGuard AI - {int(time.time())}"
            
            api.upload_folder(
                folder_path=temp_dir,
                repo_id=repo_name,
                repo_type="space",
                token=token,
                commit_message=commit_message
            )
            print("  ✅ Upload complete!")
        
        print(f"\n🎉 Deployment successful!")
        print(f"🔗 View at: https://huggingface.co/spaces/{repo_name}")
        print(f"\n⏳ Note: It may take a few minutes for the Space to build and start.")
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <username/repo-name>")
        print("Example: python deploy.py myusername/climateguard-ai")
        print("\nMake sure you've logged in first:")
        print("  huggingface-cli login")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    deploy_to_huggingface(repo_name)
