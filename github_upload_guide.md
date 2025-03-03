# How to Upload BROski Bot to GitHub

Follow these steps to create a GitHub repository for your BROski Bot project.

## Prerequisites
- [Git](https://git-scm.com/downloads) installed on your computer
- A [GitHub](https://github.com/) account

## Step 1: Create a .gitignore File

First, create a `.gitignore` file in your project directory to avoid uploading sensitive data:

```
# BROski Bot .gitignore file

# Config files with sensitive API keys
config.json

# Logs
logs/
*.log

# Cache files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
env/

# Data files
*.csv
*.pkl

# Other
.DS_Store
.env
```

## Step 2: Initialize Git Repository

Open a command prompt or terminal in your BROski Bot directory:

```bash
cd "C:\Users\Lyndz\OneDrive\Documents\BROski the Crypto Bot"
git init
```

## Step 3: Create GitHub Repository

1. Log in to your GitHub account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Enter "BROski-Bot" as the repository name
4. Add a description: "Automated cryptocurrency trading bot with multiple strategies"
5. Choose whether to make it Public or Private
6. Do NOT initialize with README, .gitignore, or license (we'll add these ourselves)
7. Click "Create repository"

## Step 4: Add Your Files to Git

Back in your command prompt:

```bash
# Add all files (except those in .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit of BROski Bot"
```

## Step 5: Connect to GitHub and Push

GitHub will show commands after creating your repository. Use these commands:

```bash
# Add the GitHub repository as a remote
git remote add origin https://github.com/YOUR-USERNAME/BROski-Bot.git

# Push your code to GitHub
git push -u origin master
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Step 6: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your BROski Bot files
3. Verify that sensitive files like config.json are not included

## Additional Recommendations

1. **Add a LICENSE file** if you want to control how others can use your code
2. **Update the README.md** with proper installation instructions
3. **Create example config file**: Add a `config.example.json` that shows the structure without your API keys
4. **Set up branch protection** for your main branch if collaborating with others
5. **Create a Wiki** with detailed documentation about using BROski Bot

Now your BROski Bot project is safely stored on GitHub!
