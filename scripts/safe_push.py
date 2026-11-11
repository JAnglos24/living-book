import os
import subprocess
import re

site_dir = r"D:\Proyectos personales\personal branding\living_book_astro"
env_path = os.path.join(site_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        m = re.match(r"^(?:GITHUB_TOKEN|GH_TOKEN|GIT_TOKEN)\s*=\s*[\"']?([^\"'\s\r\n]+)", line)
        if m:
            token = m.group(1).strip()
            break

if not token:
    print("Token not found in .env")
    exit(1)

# Git add
subprocess.run(["git", "add", "."], cwd=site_dir, check=True)

# Git commit
msg = "fix(ebook): synchronize curated color-compliant assets for chapter 10"
res = subprocess.run(["git", "commit", "-m", msg], cwd=site_dir, capture_output=True, text=True)
print(res.stdout)

# Git push using authenticated URL
auth_url = f"https://{token}@github.com/JAnglos24/living-book.git"
push_res = subprocess.run(["git", "push", auth_url, "master"], cwd=site_dir, capture_output=True, text=True)
if push_res.returncode == 0:
    print("Git push successful to master!")
else:
    err = push_res.stderr.replace(token, "***TOKEN***")
    print("Git push failed:", err)

