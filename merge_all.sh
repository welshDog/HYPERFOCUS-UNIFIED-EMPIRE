#!/usr/bin/env bash
# 🚀 HYPERFOCUS UNIFIED EMPIRE - MASS SUBTREE IMPORT SCRIPT
# Imports all source repositories into the structured monorepo with full history.
# Re-run safe: skips already imported remotes.

set -euo pipefail

echo "🚀 Starting HYPERFOCUS UNIFIED EMPIRE mass import..."
echo "This will import all source repositories with full git history preserved."

# Function to check if remote exists
remote_exists() {
    git remote | grep -q "^$1$"
}

# Function to safely add remote and subtree
import_repo() {
    local remote_name="$1"
    local repo_url="$2"
    local target_path="$3"
    local commit_msg="$4"
    
    echo "📦 Processing: $remote_name -> $target_path"
    
    if remote_exists "$remote_name"; then
        echo "   ⚡ Remote '$remote_name' already exists, skipping remote add"
        git fetch "$remote_name"
    else
        echo "   🔗 Adding remote: $repo_url"
        git remote add "$remote_name" "$repo_url"
        git fetch "$remote_name"
    fi
    
    if [ -d "$target_path" ]; then
        echo "   ⚠️  Directory '$target_path' already exists, skipping subtree add"
    else
        echo "   🌳 Creating subtree: $target_path"
        git subtree add --prefix="$target_path" "$remote_name" main --message="$commit_msg"
    fi
    
    echo "   ✅ Completed: $remote_name"
    echo ""
}

# Create directory structure if not exists
echo "🏗️  Ensuring directory structure..."
mkdir -p "🚀 CORE-SYSTEMS" "🤖 AI-AGENTS" "🎮 APPLICATIONS" "🧠 NEURODIVERGENT-TOOLS" "📚 VERSION-ARCHIVE" "🛠️ DEVELOPMENT" "📖 DOCUMENTATION"

# Import V8.5 (legacy)
import_repo "v85" \
    "https://github.com/welshDog/HYPERfocusZone-V8.5.git" \
    "📚 VERSION-ARCHIVE/v8.5-legacy" \
    "import: V8.5 legacy version"

# Import V9 (evolution scripts)
import_repo "v9" \
    "https://github.com/welshDog/HYPERfocusZone-V9.git" \
    "📚 VERSION-ARCHIVE/v9-evolution" \
    "import: V9 evolution version"

# Import ChaosGenius dashboard
import_repo "chaos" \
    "https://github.com/welshDog/HYPERFOCUS-DREAM-ChaosGenius.git" \
    "🚀 CORE-SYSTEMS/chaos-genius-dashboard" \
    "import: ChaosGenius dashboard system"

# Import BROski Tower
import_repo "tower" \
    "https://github.com/HYPERFOCUSzone/HyperFocus-Zone-BROski-Tower.git" \
    "🚀 CORE-SYSTEMS/broski-tower" \
    "import: BROski Tower core system"

# Import BROski Bot
import_repo "broskibot" \
    "https://github.com/welshDog/BROski-BOT.git" \
    "🤖 AI-AGENTS/broski-bot" \
    "import: BROski trading bot agent"

# Import Discord manager (clanverse)
import_repo "clanverse" \
    "https://github.com/welshDog/broski-clanverse.git" \
    "🤖 AI-AGENTS/discord-manager" \
    "import: Discord manager agent"

# Import hyperfocushub (TypeScript hub)
import_repo "hubts" \
    "https://github.com/welshDog/hyperfocushub.git" \
    "🎮 APPLICATIONS/hyperfocus-hub-ts" \
    "import: TypeScript hub application"

# Import HyperFocus-Hub (legacy neuro hub)
import_repo "neurohub" \
    "https://github.com/welshDog/HyperFocus-Hub.git" \
    "🎮 APPLICATIONS/hyperfocus-hub" \
    "import: original neuro hub application"

# Import filter_Zone
import_repo "filter" \
    "https://github.com/welshDog/filter_Zone.git" \
    "🎮 APPLICATIONS/filter-zone" \
    "import: filter zone application"

# Import NeighborWork
import_repo "neighbor" \
    "https://github.com/welshDog/NeighborWork.git" \
    "🎮 APPLICATIONS/neighbor-work" \
    "import: NeighborWork application"

echo "🎉 LEGENDARY SUCCESS! All repositories imported with full history preserved."
echo "🏰 Your HYPERFOCUS UNIFIED EMPIRE is now complete!"
echo ""
echo "Next steps:"
echo "  git add ."
echo "  git commit -m \"chore: import source repositories (subtree history preserved)\""
echo "  git push origin main"
echo ""
echo "⚡ Ready for the next legendary enhancement! ❤️‍🔥"
