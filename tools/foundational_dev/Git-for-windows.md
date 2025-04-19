# 🧰 Git Installation & Configuration Guide (Windows)

This guide walks you through installing and configuring Git on **Windows**, with recommended settings for use in professional or collaborative environments.

---

## 🔽 1. Download Git for Windows

👉 [https://git-scm.com/download/win](https://git-scm.com/download/win)

You can re-run the installer at any time to change settings. If you're reinstalling Git, **make sure all Git programs are closed first**, and consider **restarting your computer** before proceeding.

---

## ⚙️ 2. Installation Options

> When installing or reinstalling, **run the installer as Administrator**

### Set the following:

| Step | Recommended Option |
|------|--------------------|
| Destination | `C:\Program Files\Git` |
| Components | ✅ Select all (unless you know what you're doing) |
| Start Menu Folder | `Git` |
| Default Editor | `Notepad` (or something you know how to use — **avoid Vim**) |
| Initial Branch Name | `master` |
| PATH Environment | **Git from the command line and from 3rd-party tools** |
| SSH Executable | **Use bundled OpenSSH** |
| HTTPS Backend | **Use OpenSSL library** |
| Line Endings | **Checkout Windows-style, commit Unix-style** |
| Terminal Emulator | **Use MinTTY (default)** |
| `git pull` Behavior | **Default (fast-forward or merge)** |
| Credential Helper | **Git Credential Manager** |
| File System Caching | ✅ Enabled |
| Experimental Options | ❌ Leave unticked |

---

## 👤 3. Set Up Your User Info

Git tracks the author of every commit. You must set your name and email globally.

### Open PowerShell and run:

```powershell
$dom = $env:userdomain
$usr = $env:username
$fullname = ([adsi]"WinNT://$dom/$usr,user").fullname
$searcher = [adsisearcher]"(samaccountname=$env:USERNAME)"
$email = $searcher.FindOne().Properties.mail
git config --global user.name $fullname
git config --global user.email $email
```

To verify it worked, check your config:
```bash
git config --global --list
```

---

## 🛑 Optional: Global `.gitignore`

If you use a custom editor (not VS Code), you may want to create a global `.gitignore` to avoid clutter in project-specific files.

### Steps:

1. Create a `.gitignore` file:
   ```bash
   touch ~/.gitignore
   ```

2. Add your rules (example for Sublime Text):
   ```plaintext
   # Sublime Text
   *.sublime-project
   *.sublime-workspace
   ```

3. Tell Git to use it:
   ```bash
   git config --global core.excludesfile ~/.gitignore
   ```

📌 For most users in D+A using Windows and VS Code, this step is **not needed**.

---

## ✅ You're Ready!

You now have Git fully installed, configured, and ready to use with VS Code, Azure DevOps, or the terminal.

---
*Licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)*
*Visit [ProductFoundry.ai](https://productfoundry.ai)*
