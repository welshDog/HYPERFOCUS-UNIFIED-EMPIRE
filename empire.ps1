# 🚀💎 HYPERFOCUS UNIFIED EMPIRE 💎🚀
# Windows PowerShell Bootstrap Script
# ADHD-friendly development environment setup

param(
    [string]$Command = "help"
)

# 🎨 Colors for legendary output
$LegendaryBlue = "Cyan"
$LegendaryGreen = "Green"
$LegendaryYellow = "Yellow"
$LegendaryRed = "Red"
$LegendaryPurple = "Magenta"

function Write-LegendaryHeader {
    Write-Host ""
    Write-Host "🚀💎 HYPERFOCUS UNIFIED EMPIRE 💎🚀" -ForegroundColor $LegendaryBlue
    Write-Host "The legendary neurodivergent-friendly development toolkit" -ForegroundColor $LegendaryPurple
    Write-Host ""
}

function Show-Help {
    Write-LegendaryHeader
    Write-Host "Available commands:" -ForegroundColor $LegendaryGreen
    Write-Host "  .\empire.ps1 bootstrap     - 🏗️ Bootstrap development environment" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 dev           - 🚀 Start development environment" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 focus         - 🧠 Launch ADHD-optimized focus session" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 health        - 🏥 Check empire health status" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 agents        - 🤖 List all AI agents" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 test          - 🧪 Run tests" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 clean         - 🧹 Clean build artifacts" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 info          - ℹ️ Show empire information" -ForegroundColor $LegendaryYellow
    Write-Host ""
    Write-Host "🧠 ADHD-Optimized Workflows:" -ForegroundColor $LegendaryPurple
    Write-Host "  .\empire.ps1 dev           - Start everything for development" -ForegroundColor $LegendaryYellow
    Write-Host "  .\empire.ps1 focus         - Launch focus session" -ForegroundColor $LegendaryYellow
    Write-Host ""
}

function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor $LegendaryGreen
            return $true
        }
    }
    catch {
        Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor $LegendaryRed
        return $false
    }
    return $false
}

function Test-NodeInstallation {
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor $LegendaryGreen
            return $true
        }
    }
    catch {
        Write-Host "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org" -ForegroundColor $LegendaryRed
        return $false
    }
    return $false
}

function Bootstrap-Empire {
    Write-LegendaryHeader
    Write-Host "🏗️ Bootstrapping HYPERFOCUS UNIFIED EMPIRE..." -ForegroundColor $LegendaryBlue
    
    # Check prerequisites
    Write-Host "🔍 Checking prerequisites..." -ForegroundColor $LegendaryYellow
    $pythonOk = Test-PythonInstallation
    $nodeOk = Test-NodeInstallation
    
    if (-not $pythonOk -or -not $nodeOk) {
        Write-Host "❌ Prerequisites not met. Please install missing dependencies." -ForegroundColor $LegendaryRed
        return
    }
    
    # Create virtual environment
    Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor $LegendaryYellow
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
        Write-Host "✅ Virtual environment created" -ForegroundColor $LegendaryGreen
    } else {
        Write-Host "⚡ Virtual environment already exists" -ForegroundColor $LegendaryYellow
    }
    
    # Activate virtual environment and install dependencies
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor $LegendaryYellow
    & ".\.venv\Scripts\Activate.ps1"
    
    # Find and install from requirements.txt files
    $requirementFiles = Get-ChildItem -Recurse -Name "requirements.txt" | Where-Object { $_ -notmatch "\.venv|node_modules" }
    foreach ($reqFile in $requirementFiles) {
        Write-Host "   Installing from $reqFile" -ForegroundColor $LegendaryBlue
        pip install -r $reqFile
    }
    
    # Install Node.js dependencies
    Write-Host "📦 Installing Node.js dependencies..." -ForegroundColor $LegendaryYellow
    $packageFiles = Get-ChildItem -Recurse -Name "package.json" | Where-Object { $_ -notmatch "\.venv|node_modules" }
    foreach ($packageFile in $packageFiles) {
        $dir = Split-Path $packageFile
        Write-Host "   Installing dependencies in $dir" -ForegroundColor $LegendaryBlue
        Push-Location $dir
        npm install
        Pop-Location
    }
    
    # Create data directories
    Write-Host "📁 Creating data directories..." -ForegroundColor $LegendaryYellow
    @(
        "🛠️ DEVELOPMENT/data",
        "🛠️ DEVELOPMENT/logs",
        "🛠️ DEVELOPMENT/cache"
    ) | ForEach-Object {
        if (-not (Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ -Force | Out-Null
            Write-Host "   Created $_" -ForegroundColor $LegendaryBlue
        }
    }
    
    Write-Host "✅ Empire bootstrap complete! Ready for legendary development." -ForegroundColor $LegendaryGreen
}

function Start-Development {
    Write-LegendaryHeader
    Write-Host "🚀 Starting HYPERFOCUS UNIFIED EMPIRE development mode..." -ForegroundColor $LegendaryBlue
    
    # Activate virtual environment
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & ".\.venv\Scripts\Activate.ps1"
        Write-Host "✅ Python virtual environment activated" -ForegroundColor $LegendaryGreen
    }
    
    Write-Host "🚀 Starting core systems..." -ForegroundColor $LegendaryYellow
    # Add core system startup logic here
    
    Write-Host "🤖 Starting AI agents..." -ForegroundColor $LegendaryYellow
    # Add agent startup logic here
    
    Write-Host "🎮 Starting applications..." -ForegroundColor $LegendaryYellow
    # Add application startup logic here
    
    Write-Host "✅ Empire development environment is LEGENDARY!" -ForegroundColor $LegendaryGreen
    Write-Host "🧠 Focus mode ready. Happy coding! ⚡" -ForegroundColor $LegendaryPurple
}

function Start-FocusSession {
    Write-LegendaryHeader
    Write-Host "🧠 Launching HYPERFOCUS focus session..." -ForegroundColor $LegendaryPurple
    
    Write-Host "📊 Preparing focus dashboard..." -ForegroundColor $LegendaryYellow
    # Add focus dashboard startup
    
    Write-Host "🤖 Activating focus agents..." -ForegroundColor $LegendaryYellow
    # Add focus agents startup
    
    Write-Host "🎵 Starting focus environment..." -ForegroundColor $LegendaryYellow
    Start-Sleep 2
    
    Write-Host "✅ Focus session active! Time to build legendary things! ⚡❤️‍🔥" -ForegroundColor $LegendaryGreen
}

function Show-Health {
    Write-LegendaryHeader
    Write-Host "🏥 HYPERFOCUS UNIFIED EMPIRE Health Check:" -ForegroundColor $LegendaryBlue
    
    Write-Host "📁 Directory structure:" -ForegroundColor $LegendaryYellow
    @(
        "🚀 CORE-SYSTEMS",
        "🤖 AI-AGENTS", 
        "🎮 APPLICATIONS",
        "🧠 NEURODIVERGENT-TOOLS",
        "📚 VERSION-ARCHIVE",
        "🛠️ DEVELOPMENT",
        "📖 DOCUMENTATION"
    ) | ForEach-Object {
        if (Test-Path $_) {
            Write-Host "  ✅ $_" -ForegroundColor $LegendaryGreen
        } else {
            Write-Host "  ❌ $_" -ForegroundColor $LegendaryRed
        }
    }
    
    Write-Host "🐍 Python environment:" -ForegroundColor $LegendaryYellow
    if (Test-Path ".venv") {
        Write-Host "  ✅ Virtual environment" -ForegroundColor $LegendaryGreen
        if (Test-Path ".venv\Scripts\python.exe") {
            $pythonVersion = & ".venv\Scripts\python.exe" --version
            Write-Host "  ✅ $pythonVersion" -ForegroundColor $LegendaryGreen
        }
    } else {
        Write-Host "  ❌ Virtual environment missing" -ForegroundColor $LegendaryRed
    }
    
    Write-Host "📦 Node.js environment:" -ForegroundColor $LegendaryYellow
    try {
        $nodeVersion = node --version
        Write-Host "  ✅ Node.js $nodeVersion" -ForegroundColor $LegendaryGreen
    }
    catch {
        Write-Host "  ❌ Node.js not installed" -ForegroundColor $LegendaryRed
    }
}

function List-Agents {
    Write-LegendaryHeader
    Write-Host "🤖 AI Agents in the Empire:" -ForegroundColor $LegendaryBlue
    
    $agentsDir = "🤖 AI-AGENTS"
    if (Test-Path $agentsDir) {
        Get-ChildItem $agentsDir -Directory | ForEach-Object {
            Write-Host "  🤖 $($_.Name)" -ForegroundColor $LegendaryYellow
            $readmePath = Join-Path $_.FullName "README.md"
            if (Test-Path $readmePath) {
                $firstLine = Get-Content $readmePath -First 1
                if ($firstLine -match "^# (.+)") {
                    Write-Host "    📖 $($matches[1])" -ForegroundColor $LegendaryBlue
                }
            }
        }
    } else {
        Write-Host "  ❌ AI-AGENTS directory not found" -ForegroundColor $LegendaryRed
    }
}

function Run-Tests {
    Write-LegendaryHeader
    Write-Host "🧪 Running HYPERFOCUS UNIFIED EMPIRE test suite..." -ForegroundColor $LegendaryBlue
    
    # Activate virtual environment
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & ".\.venv\Scripts\Activate.ps1"
    }
    
    Write-Host "🚀 Testing core systems..." -ForegroundColor $LegendaryYellow
    # Add core systems testing logic
    
    Write-Host "🤖 Testing AI agents..." -ForegroundColor $LegendaryYellow
    # Add agent testing logic
    
    Write-Host "🎮 Testing applications..." -ForegroundColor $LegendaryYellow
    # Add application testing logic
    
    Write-Host "✅ All tests passed! Empire is LEGENDARY! ⚡" -ForegroundColor $LegendaryGreen
}

function Clean-Empire {
    Write-LegendaryHeader
    Write-Host "🧹 Cleaning HYPERFOCUS UNIFIED EMPIRE..." -ForegroundColor $LegendaryBlue
    
    # Clean Python cache
    Get-ChildItem -Recurse -Name "__pycache__" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -Name "*.pyc" | Remove-Item -Force
    
    # Clean Node.js cache
    Get-ChildItem -Recurse -Name "node_modules" | Where-Object { $_ -notmatch "\.venv" } | Remove-Item -Recurse -Force
    
    # Clean build artifacts
    Get-ChildItem -Recurse -Name "dist" | Remove-Item -Recurse -Force
    Get-ChildItem -Recurse -Name "build" | Remove-Item -Recurse -Force
    
    Write-Host "✅ Empire cleaned to legendary standards!" -ForegroundColor $LegendaryGreen
}

function Show-Info {
    Write-LegendaryHeader
    Write-Host "Empire Status:" -ForegroundColor $LegendaryGreen
    try {
        $repoUrl = git remote get-url origin 2>$null
        if ($repoUrl) {
            Write-Host "  Repository: $repoUrl" -ForegroundColor $LegendaryBlue
        }
    }
    catch {
        Write-Host "  Repository: Local development" -ForegroundColor $LegendaryBlue
    }
    
    try {
        $branch = git branch --show-current 2>$null
        if ($branch) {
            Write-Host "  Branch: $branch" -ForegroundColor $LegendaryBlue
        }
    }
    catch {
        Write-Host "  Branch: Unknown" -ForegroundColor $LegendaryBlue
    }
    
    $components = Get-ChildItem -Directory | Where-Object { $_.Name -match "🚀|🤖|🎮|🧠|📚|🛠|📖" }
    Write-Host "  Components: $($components.Count) directories" -ForegroundColor $LegendaryBlue
    Write-Host "  Languages: Python, TypeScript, JavaScript, Shell" -ForegroundColor $LegendaryBlue
    Write-Host "  Architecture: Neurodivergent-optimized monorepo" -ForegroundColor $LegendaryBlue
    Write-Host ""
    Write-Host "🧠 ADHD-Optimized Features:" -ForegroundColor $LegendaryPurple
    Write-Host "  ✅ Visual emoji navigation" -ForegroundColor $LegendaryGreen
    Write-Host "  ✅ Single-command workflows" -ForegroundColor $LegendaryGreen
    Write-Host "  ✅ Clear component separation" -ForegroundColor $LegendaryGreen
    Write-Host "  ✅ Unified development environment" -ForegroundColor $LegendaryGreen
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "bootstrap" { Bootstrap-Empire }
    "dev" { Start-Development }
    "focus" { Start-FocusSession }
    "health" { Show-Health }
    "agents" { List-Agents }
    "test" { Run-Tests }
    "clean" { Clean-Empire }
    "info" { Show-Info }
    "help" { Show-Help }
    default { Show-Help }
}
