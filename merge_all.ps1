# 🚀 HYPERFOCUS UNIFIED EMPIRE - MASS SUBTREE IMPORT SCRIPT (PowerShell)
# Imports all source repositories into the structured monorepo with full history.
# Re-run safe: skips already imported remotes.

Write-Host "🚀 Starting HYPERFOCUS UNIFIED EMPIRE mass import..." -ForegroundColor Cyan
Write-Host "This will import all source repositories with full git history preserved." -ForegroundColor Yellow

# Function to check if remote exists
function Test-RemoteExists {
    param($RemoteName)
    $remotes = git remote
    return $remotes -contains $RemoteName
}

# Function to safely add remote and subtree
function Import-Repository {
    param(
        [string]$RemoteName,
        [string]$RepoUrl,
        [string]$TargetPath,
        [string]$CommitMsg
    )
    
    Write-Host "📦 Processing: $RemoteName -> $TargetPath" -ForegroundColor Green
    
    if (Test-RemoteExists $RemoteName) {
        Write-Host "   ⚡ Remote '$RemoteName' already exists, skipping remote add" -ForegroundColor Yellow
        git fetch $RemoteName
    } else {
        Write-Host "   🔗 Adding remote: $RepoUrl" -ForegroundColor Blue
        git remote add $RemoteName $RepoUrl
        git fetch $RemoteName
    }
    
    if (Test-Path $TargetPath) {
        Write-Host "   ⚠️  Directory '$TargetPath' already exists, skipping subtree add" -ForegroundColor Yellow
    } else {
        Write-Host "   🌳 Creating subtree: $TargetPath" -ForegroundColor Blue
        git subtree add --prefix="$TargetPath" $RemoteName main --message="$CommitMsg"
    }
    
    Write-Host "   ✅ Completed: $RemoteName" -ForegroundColor Green
    Write-Host ""
}

# Create directory structure if not exists
Write-Host "🏗️  Ensuring directory structure..." -ForegroundColor Cyan
$directories = @(
    "🚀 CORE-SYSTEMS",
    "🤖 AI-AGENTS", 
    "🎮 APPLICATIONS",
    "🧠 NEURODIVERGENT-TOOLS",
    "📚 VERSION-ARCHIVE",
    "🛠️ DEVELOPMENT",
    "📖 DOCUMENTATION"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Import V8.5 (legacy)
Import-Repository -RemoteName "v85" `
    -RepoUrl "https://github.com/welshDog/HYPERfocusZone-V8.5.git" `
    -TargetPath "📚 VERSION-ARCHIVE/v8.5-legacy" `
    -CommitMsg "import: V8.5 legacy version"

# Import V9 (evolution scripts)
Import-Repository -RemoteName "v9" `
    -RepoUrl "https://github.com/welshDog/HYPERfocusZone-V9.git" `
    -TargetPath "📚 VERSION-ARCHIVE/v9-evolution" `
    -CommitMsg "import: V9 evolution version"

# Import ChaosGenius dashboard
Import-Repository -RemoteName "chaos" `
    -RepoUrl "https://github.com/welshDog/HYPERFOCUS-DREAM-ChaosGenius.git" `
    -TargetPath "🚀 CORE-SYSTEMS/chaos-genius-dashboard" `
    -CommitMsg "import: ChaosGenius dashboard system"

# Import BROski Tower
Import-Repository -RemoteName "tower" `
    -RepoUrl "https://github.com/HYPERFOCUSzone/HyperFocus-Zone-BROski-Tower.git" `
    -TargetPath "🚀 CORE-SYSTEMS/broski-tower" `
    -CommitMsg "import: BROski Tower core system"

# Import BROski Bot
Import-Repository -RemoteName "broskibot" `
    -RepoUrl "https://github.com/welshDog/BROski-BOT.git" `
    -TargetPath "🤖 AI-AGENTS/broski-bot" `
    -CommitMsg "import: BROski trading bot agent"

# Import Discord manager (clanverse)
Import-Repository -RemoteName "clanverse" `
    -RepoUrl "https://github.com/welshDog/broski-clanverse.git" `
    -TargetPath "🤖 AI-AGENTS/discord-manager" `
    -CommitMsg "import: Discord manager agent"

# Import hyperfocushub (TypeScript hub)
Import-Repository -RemoteName "hubts" `
    -RepoUrl "https://github.com/welshDog/hyperfocushub.git" `
    -TargetPath "🎮 APPLICATIONS/hyperfocus-hub-ts" `
    -CommitMsg "import: TypeScript hub application"

# Import HyperFocus-Hub (legacy neuro hub)
Import-Repository -RemoteName "neurohub" `
    -RepoUrl "https://github.com/welshDog/HyperFocus-Hub.git" `
    -TargetPath "🎮 APPLICATIONS/hyperfocus-hub" `
    -CommitMsg "import: original neuro hub application"

# Import filter_Zone
Import-Repository -RemoteName "filter" `
    -RepoUrl "https://github.com/welshDog/filter_Zone.git" `
    -TargetPath "🎮 APPLICATIONS/filter-zone" `
    -CommitMsg "import: filter zone application"

# Import NeighborWork
Import-Repository -RemoteName "neighbor" `
    -RepoUrl "https://github.com/welshDog/NeighborWork.git" `
    -TargetPath "🎮 APPLICATIONS/neighbor-work" `
    -CommitMsg "import: NeighborWork application"

Write-Host "🎉 LEGENDARY SUCCESS! All repositories imported with full history preserved." -ForegroundColor Green
Write-Host "🏰 Your HYPERFOCUS UNIFIED EMPIRE is now complete!" -ForegroundColor Magenta
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git commit -m `"chore: import source repositories (subtree history preserved)`"" -ForegroundColor White
Write-Host "  git push origin main" -ForegroundColor White
Write-Host ""
Write-Host "⚡ Ready for the next legendary enhancement! ❤️‍🔥" -ForegroundColor Red
