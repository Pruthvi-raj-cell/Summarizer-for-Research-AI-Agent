import os
from dotenv import load_dotenv

print("--- GOOGLE API DIAGNOSTIC START ---")

# 1. Check where we are
print(f"Current Folder: {os.getcwd()}")

# 2. Look for the file
if os.path.exists(".env"):
    print("✅ Found file: .env")
    # Check if it has content
    with open(".env", "r") as f:
        content = f.read()
        if "GOOGLE_API_KEY" in content:
            print("✅ File contains GOOGLE_API_KEY variable")
        elif "OPENAI_API_KEY" in content:
            print("⚠️ Found OPENAI_API_KEY, but we need GOOGLE_API_KEY now!")
        else:
            print("❌ File is missing GOOGLE_API_KEY")
else:
    print("❌ .env file NOT found in this folder!")
    print("Files found here:", os.listdir())

# 3. Try loading it
load_dotenv()
key = os.getenv("GOOGLE_API_KEY")

if key:
    print(f"✅ Success! Key loaded: {key[:10]}... (Hidden)")
else:
    print("❌ Load failed. Python cannot see 'GOOGLE_API_KEY'.")

print("--- GOOGLE API DIAGNOSTIC END ---")