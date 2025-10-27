#!/usr/bin/env python3
"""
Environment setup script for Qwen Agent
"""

import os
import sys

def check_api_key():
    """Check if DASHSCOPE_API_KEY is set"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        print(f"✅ DASHSCOPE_API_KEY is set (length: {len(api_key)} characters)")
        return True
    else:
        print("❌ DASHSCOPE_API_KEY is not set")
        return False

def setup_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"📝 Creating {env_file} file...")
        with open(env_file, "w") as f:
            f.write("# Qwen Agent Environment Variables\n")
            f.write("# Get your API key from: https://dashscope.aliyun.com/\n")
            f.write("DASHSCOPE_API_KEY=your-api-key-here\n")
            f.write("\n# Optional: Enable debug mode\n")
            f.write("# DEBUG=1\n")
        print(f"✅ Created {env_file} file")
        print("💡 Edit the file and set your DASHSCOPE_API_KEY")
        return True
    else:
        print(f"📄 {env_file} file already exists")
        return False

def main():
    """Main setup function"""
    print("🔧 Qwen Agent Environment Setup")
    print("=" * 35)

    # Check current environment
    print("\n🔍 Checking current environment...")
    api_key_ok = check_api_key()

    # Setup .env file if needed
    print("\n📋 Setting up environment files...")
    env_created = setup_env_file()

    print("\n📚 How to use:")
    print("   1. Edit .env file and set your DASHSCOPE_API_KEY")
    print("   2. Load environment: source .env" if env_created else "   2. Load environment: source .env")
    print("   3. Test agent: python run_agent.py"
    print("\n🐳 Docker usage:")
    print("   docker run -e DASHSCOPE_API_KEY='your-key' qwen-agent")

    if not api_key_ok:
        print("\n⚠️  IMPORTANT: Set your DASHSCOPE_API_KEY before running the agent!")
        print("   Get it from: https://dashscope.aliyun.com/")

if __name__ == "__main__":
    main()
