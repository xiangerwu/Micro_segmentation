# 安裝腳本 install_requirements_individually.py
import subprocess

failed = []

with open("requirements.txt") as f:
    for line in f:
        pkg = line.strip()
        if not pkg or pkg.startswith("#"):
            continue
        print(f"🚀 Installing: {pkg}")
        result = subprocess.run(["pip", "install", pkg])
        if result.returncode != 0:
            print(f"❌ Failed: {pkg}")
            failed.append(pkg)

print("\n=== Summary of Failed Packages ===")
for pkg in failed:
    print(pkg)
