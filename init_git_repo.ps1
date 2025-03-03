# PowerShell script to initialize Git repository and prepare for GitHub upload

Write-Host "Initializing BROski Bot Git Repository..." -ForegroundColor Cyan

# Step 1: Initialize the repository
Write-Host "Step 1: Initializing Git repository..." -ForegroundColor Green
git init

# Step 2: Create .gitignore file
Write-Host "Step 2: Creating .gitignore file..." -ForegroundColor Green
@"
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
"@ | Out-File -FilePath ".gitignore" -Encoding utf8

# Step 3: Create an example config file if needed
Write-Host "Step 3: Creating example configuration..." -ForegroundColor Green
if (Test-Path "config.json") {
    $config = Get-Content "config.json" -Raw | ConvertFrom-Json
    
    # Create a safe version by removing sensitive data
    if ($config.exchange) {
        $config.exchange.api_key = ""
        $config.exchange.api_secret = ""
    }
    
    $config | ConvertTo-Json -Depth 10 | Out-File -FilePath "config.example.json" -Encoding utf8
    Write-Host "Created config.example.json without API keys" -ForegroundColor Green
} else {
    Write-Host "Warning: config.json not found, skipping example creation" -ForegroundColor Yellow
}

# Step 4: Add all files
Write-Host "Step 4: Adding files to Git staging area..." -ForegroundColor Green
git add .

# Step 5: Commit the files
Write-Host "Step 5: Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit of BROski Bot"

# Instructions for GitHub
Write-Host "`nRepository initialized successfully!" -ForegroundColor Cyan
Write-Host "`nNext steps for GitHub:" -ForegroundColor Yellow
Write-Host "1. Create a new repository at https://github.com/new"
Write-Host "2. Name it 'BROski-Bot'"
Write-Host "3. DO NOT initialize with README, .gitignore, or license"
Write-Host "4. Run these commands after creating the repository:"
Write-Host "   git remote add origin https://github.com/YOUR-USERNAME/BROski-Bot.git"
Write-Host "   git push -u origin master"
Write-Host "`nReplace YOUR-USERNAME with your actual GitHub username"
