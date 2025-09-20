#!/bin/bash

# This script creates a 'frontend' folder in the current directory
# and populates it with the necessary project files.

echo "🚀 Creating the 'frontend' directory..."

# 1. Create the 'frontend' folder.
# The '-p' flag prevents an error if the folder already exists.
mkdir -p "frontend"

# 2. A list of all the files to be created.
files=(
    ".eslintrc.cjs"
    ".gitignore"
    "demo_example.py"
    "index.html"
    "package.json"
    "postcss.config.js"
    "README_FRONTEND.md"
    "start_frontend.py"
    "tailwind.config.js"
    "test_frontend.py"
    "vite.config.js"
)

# 3. Create each file inside the 'frontend' directory.
for file in "${files[@]}"; do
    touch "frontend/$file"
done

echo "✅ 'frontend' folder and all project files created successfully!"
echo "Navigate into your new project folder with: cd frontend"