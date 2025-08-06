📦 Disk Cleaner with AI (GPT) Assistance
This Python script helps you analyze disk usage and optionally evaluate file/folder importance using OpenAI GPT-4.

It’s designed to help clean up disk space safely by showing you what's taking up space and letting GPT suggest if something is safe to delete.

🚀 Features

🔍 Scans directories and files, shows the heaviest items

🔄 Lets you drill into subdirectories interactively

🤖 Integrates with GPT-4 to analyze file/folder importance

🔒 OpenAI key is loaded securely from .env

🛠 Requirements

Python 3.8+

OpenAI API key (not necessery)

Packages: openai, python-dotenv

🧠 How It Works

You run the script.

It scans the top-level items in the path you provide (e.g. C:/ or /home/user).

It shows you the heaviest files and folders.

You can select a folder to dive into and analyze further.

If GPT is enabled (via .env), it will show AI feedback on whether items are safe to delete.

⚠️ Warnings

This script does not automatically delete anything.

GPT is used only as a recommendation tool — always double-check!


Example GPT Output

C:/Windows: 39.35 GB

[GPT]: No, this folder contains core Windows system files. Deleting it will break your operating system.

📄 License
MIT — do whatever you want, but don't sue the author.
