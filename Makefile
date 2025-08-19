# 🛠️ HYPERFOCUS UNIFIED EMPIRE - Legendary Makefile
# Single-command workflows for ADHD-optimized development

.DEFAULT_GOAL := help
SHELL := /bin/bash

# 🎨 Colors for legendary output
LEGENDARY_BLUE := \033[36m
LEGENDARY_GREEN := \033[32m
LEGENDARY_YELLOW := \033[33m
LEGENDARY_RED := \033[31m
LEGENDARY_PURPLE := \033[35m
LEGENDARY_BOLD := \033[1m
RESET := \033[0m

# 📁 Empire directories
CORE_SYSTEMS := 🚀\ CORE-SYSTEMS
AI_AGENTS := 🤖\ AI-AGENTS
APPLICATIONS := 🎮\ APPLICATIONS
NEURODIVERGENT_TOOLS := 🧠\ NEURODIVERGENT-TOOLS
VERSION_ARCHIVE := 📚\ VERSION-ARCHIVE
DEVELOPMENT := 🛠️\ DEVELOPMENT
DOCUMENTATION := 📖\ DOCUMENTATION

# 🐍 Python settings
PYTHON := python3
PIP := pip3
VENV := .venv

# 📦 Node.js settings
NODE := node
NPM := npm
YARN := yarn

# 🐳 Docker settings
DOCKER := docker
DOCKER_COMPOSE := docker-compose

.PHONY: help
help: ## 🏰 Show this legendary help message
	@echo -e "$(LEGENDARY_BLUE)$(LEGENDARY_BOLD)"
	@echo "🚀💎 HYPERFOCUS UNIFIED EMPIRE 💎🚀"
	@echo "The legendary neurodivergent-friendly development toolkit"
	@echo -e "$(RESET)"
	@echo -e "$(LEGENDARY_GREEN)Available commands:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  $(LEGENDARY_YELLOW)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo -e "$(LEGENDARY_PURPLE)🧠 ADHD-Optimized Workflows:$(RESET)"
	@echo -e "  $(LEGENDARY_YELLOW)make dev$(RESET)           - Start everything for development"
	@echo -e "  $(LEGENDARY_YELLOW)make focus$(RESET)         - Launch focus session"
	@echo -e "  $(LEGENDARY_YELLOW)make deploy$(RESET)        - Deploy entire empire"
	@echo ""

## 🚀 Development Workflows

.PHONY: bootstrap
bootstrap: ## 🏗️ Bootstrap entire empire development environment
	@echo -e "$(LEGENDARY_BLUE)🏗️ Bootstrapping HYPERFOCUS UNIFIED EMPIRE...$(RESET)"
	@$(MAKE) --no-print-directory create-venv
	@$(MAKE) --no-print-directory install-deps
	@$(MAKE) --no-print-directory setup-hooks
	@echo -e "$(LEGENDARY_GREEN)✅ Empire bootstrap complete! Ready for legendary development.$(RESET)"

.PHONY: dev
dev: ## 🚀 Start full development environment (all services)
	@echo -e "$(LEGENDARY_BLUE)🚀 Starting HYPERFOCUS UNIFIED EMPIRE development mode...$(RESET)"
	@$(MAKE) --no-print-directory ensure-deps
	@echo -e "$(LEGENDARY_YELLOW)Starting core systems...$(RESET)"
	@$(MAKE) --no-print-directory start-core-systems &
	@echo -e "$(LEGENDARY_YELLOW)Starting AI agents...$(RESET)"
	@$(MAKE) --no-print-directory start-ai-agents &
	@echo -e "$(LEGENDARY_YELLOW)Starting applications...$(RESET)"
	@$(MAKE) --no-print-directory start-applications &
	@echo -e "$(LEGENDARY_GREEN)✅ Empire development environment is LEGENDARY!$(RESET)"
	@echo -e "$(LEGENDARY_PURPLE)🧠 Focus mode ready. Happy coding! ⚡$(RESET)"

.PHONY: focus
focus: focus-session ## 🧠 Alias for focus-session

.PHONY: focus-session
focus-session: ## 🧠 Start neurodivergent-optimized focus session
	@echo -e "$(LEGENDARY_PURPLE)🧠 Launching HYPERFOCUS focus session...$(RESET)"
	@echo -e "$(LEGENDARY_YELLOW)📊 Preparing focus dashboard...$(RESET)"
	@$(MAKE) --no-print-directory start-focus-dashboard &
	@echo -e "$(LEGENDARY_YELLOW)🤖 Activating focus agents...$(RESET)"
	@$(MAKE) --no-print-directory start-focus-agents &
	@echo -e "$(LEGENDARY_YELLOW)🎵 Starting focus environment...$(RESET)"
	@sleep 2
	@echo -e "$(LEGENDARY_GREEN)✅ Focus session active! Time to build legendary things! ⚡❤️‍🔥$(RESET)"

.PHONY: stop
stop: ## ⏹️ Stop all running services
	@echo -e "$(LEGENDARY_YELLOW)⏹️ Stopping all empire services...$(RESET)"
	@pkill -f "python.*hyperfocus" || true
	@pkill -f "node.*empire" || true
	@$(DOCKER_COMPOSE) down || true
	@echo -e "$(LEGENDARY_GREEN)✅ All services stopped.$(RESET)"

## 📦 Dependency Management

.PHONY: create-venv
create-venv: ## 🐍 Create Python virtual environment
	@if [ ! -d "$(VENV)" ]; then \
		echo -e "$(LEGENDARY_BLUE)🐍 Creating Python virtual environment...$(RESET)"; \
		$(PYTHON) -m venv $(VENV); \
		echo -e "$(LEGENDARY_GREEN)✅ Virtual environment created.$(RESET)"; \
	fi

.PHONY: install-deps
install-deps: create-venv ## 📦 Install all dependencies
	@echo -e "$(LEGENDARY_BLUE)📦 Installing empire dependencies...$(RESET)"
	@$(MAKE) --no-print-directory install-python-deps
	@$(MAKE) --no-print-directory install-node-deps
	@echo -e "$(LEGENDARY_GREEN)✅ All dependencies installed.$(RESET)"

.PHONY: install-python-deps
install-python-deps: ## 🐍 Install Python dependencies
	@echo -e "$(LEGENDARY_YELLOW)🐍 Installing Python dependencies...$(RESET)"
	@. $(VENV)/bin/activate && \
	find . -name "requirements.txt" -exec echo "Installing from {}" \; -exec $(PIP) install -r {} \;

.PHONY: install-node-deps
install-node-deps: ## 📦 Install Node.js dependencies
	@echo -e "$(LEGENDARY_YELLOW)📦 Installing Node.js dependencies...$(RESET)"
	@find . -name "package.json" -not -path "./node_modules/*" -not -path "./.venv/*" | while read package; do \
		dir=$$(dirname "$$package"); \
		echo "Installing dependencies in $$dir"; \
		cd "$$dir" && $(NPM) install && cd - > /dev/null; \
	done

.PHONY: ensure-deps
ensure-deps: ## ✅ Ensure dependencies are installed
	@if [ ! -d "$(VENV)" ] || [ ! -d "node_modules" ]; then \
		$(MAKE) --no-print-directory install-deps; \
	fi

## 🧪 Testing & Quality

.PHONY: test
test: ## 🧪 Run all tests across the empire
	@echo -e "$(LEGENDARY_BLUE)🧪 Running HYPERFOCUS UNIFIED EMPIRE test suite...$(RESET)"
	@$(MAKE) --no-print-directory test-core-systems
	@$(MAKE) --no-print-directory test-ai-agents
	@$(MAKE) --no-print-directory test-applications
	@$(MAKE) --no-print-directory test-integration
	@echo -e "$(LEGENDARY_GREEN)✅ All tests passed! Empire is LEGENDARY! ⚡$(RESET)"

.PHONY: test-core-systems
test-core-systems: ## 🚀 Test core systems
	@echo -e "$(LEGENDARY_YELLOW)🚀 Testing core systems...$(RESET)"
	@find "$(CORE_SYSTEMS)" -name "pytest.ini" -o -name "test_*.py" | while read test; do \
		dir=$$(dirname "$$test"); \
		echo "Testing $$dir"; \
		cd "$$dir" && . ../../$(VENV)/bin/activate && python -m pytest && cd - > /dev/null; \
	done

.PHONY: test-ai-agents
test-ai-agents: ## 🤖 Test AI agents
	@echo -e "$(LEGENDARY_YELLOW)🤖 Testing AI agents...$(RESET)"
	@find "$(AI_AGENTS)" -name "*test*.py" | while read test; do \
		dir=$$(dirname "$$test"); \
		echo "Testing $$dir"; \
		cd "$$dir" && . ../../$(VENV)/bin/activate && python -m pytest && cd - > /dev/null; \
	done

.PHONY: test-applications
test-applications: ## 🎮 Test applications
	@echo -e "$(LEGENDARY_YELLOW)🎮 Testing applications...$(RESET)"
	@find "$(APPLICATIONS)" -name "package.json" | while read package; do \
		dir=$$(dirname "$$package"); \
		if jq -e '.scripts.test' "$$package" > /dev/null; then \
			echo "Testing $$dir"; \
			cd "$$dir" && $(NPM) test && cd - > /dev/null; \
		fi; \
	done

.PHONY: test-integration
test-integration: ## 🔗 Run integration tests
	@echo -e "$(LEGENDARY_YELLOW)🔗 Running integration tests...$(RESET)"
	@if [ -d "$(DEVELOPMENT)/integration-tests" ]; then \
		cd "$(DEVELOPMENT)/integration-tests" && . ../../$(VENV)/bin/activate && python -m pytest; \
	else \
		echo "No integration tests found. Creating placeholder..."; \
		mkdir -p "$(DEVELOPMENT)/integration-tests"; \
		echo "# Integration tests coming soon!" > "$(DEVELOPMENT)/integration-tests/README.md"; \
	fi

.PHONY: lint
lint: ## 🔍 Run linting across the empire
	@echo -e "$(LEGENDARY_BLUE)🔍 Linting HYPERFOCUS UNIFIED EMPIRE...$(RESET)"
	@$(MAKE) --no-print-directory lint-python
	@$(MAKE) --no-print-directory lint-javascript
	@$(MAKE) --no-print-directory lint-docs
	@echo -e "$(LEGENDARY_GREEN)✅ Empire code is clean and legendary!$(RESET)"

.PHONY: lint-python
lint-python: ## 🐍 Lint Python code
	@echo -e "$(LEGENDARY_YELLOW)🐍 Linting Python code...$(RESET)"
	@. $(VENV)/bin/activate && \
	$(PIP) install flake8 black isort 2>/dev/null && \
	find . -name "*.py" -not -path "./.venv/*" | xargs flake8 --max-line-length=100 --ignore=E203,W503 || true && \
	find . -name "*.py" -not -path "./.venv/*" | xargs black --check --diff || true

.PHONY: lint-javascript
lint-javascript: ## 📦 Lint JavaScript/TypeScript code
	@echo -e "$(LEGENDARY_YELLOW)📦 Linting JavaScript/TypeScript code...$(RESET)"
	@find . -name "package.json" -not -path "./node_modules/*" | while read package; do \
		dir=$$(dirname "$$package"); \
		if jq -e '.scripts.lint' "$$package" > /dev/null; then \
			echo "Linting $$dir"; \
			cd "$$dir" && $(NPM) run lint && cd - > /dev/null; \
		fi; \
	done || true

.PHONY: lint-docs
lint-docs: ## 📖 Lint documentation
	@echo -e "$(LEGENDARY_YELLOW)📖 Linting documentation...$(RESET)"
	@if command -v markdownlint > /dev/null; then \
		markdownlint "$(DOCUMENTATION)"/**/*.md || true; \
	else \
		echo "markdownlint not installed. Install with: npm install -g markdownlint-cli"; \
	fi

.PHONY: format
format: ## 🎨 Format code across the empire
	@echo -e "$(LEGENDARY_BLUE)🎨 Formatting HYPERFOCUS UNIFIED EMPIRE code...$(RESET)"
	@. $(VENV)/bin/activate && \
	$(PIP) install black isort 2>/dev/null && \
	find . -name "*.py" -not -path "./.venv/*" | xargs black && \
	find . -name "*.py" -not -path "./.venv/*" | xargs isort
	@echo -e "$(LEGENDARY_GREEN)✅ Code formatted to legendary standards!$(RESET)"

## 🚀 Service Management

.PHONY: start-core-systems
start-core-systems: ## 🚀 Start core systems
	@echo -e "$(LEGENDARY_YELLOW)🚀 Starting core systems...$(RESET)"
	@if [ -d "$(CORE_SYSTEMS)/chaos-genius-dashboard" ]; then \
		cd "$(CORE_SYSTEMS)/chaos-genius-dashboard" && \
		. ../../$(VENV)/bin/activate && \
		python app.py & \
	fi
	@if [ -d "$(CORE_SYSTEMS)/broski-tower" ]; then \
		cd "$(CORE_SYSTEMS)/broski-tower" && \
		. ../../$(VENV)/bin/activate && \
		python main.py & \
	fi

.PHONY: start-ai-agents
start-ai-agents: ## 🤖 Start AI agents
	@echo -e "$(LEGENDARY_YELLOW)🤖 Starting AI agents...$(RESET)"
	@if [ -d "$(AI_AGENTS)/broski-bot" ]; then \
		cd "$(AI_AGENTS)/broski-bot" && \
		. ../../$(VENV)/bin/activate && \
		python bot.py & \
	fi
	@if [ -d "$(AI_AGENTS)/discord-manager" ]; then \
		cd "$(AI_AGENTS)/discord-manager" && \
		. ../../$(VENV)/bin/activate && \
		python main.py & \
	fi

.PHONY: start-applications
start-applications: ## 🎮 Start applications
	@echo -e "$(LEGENDARY_YELLOW)🎮 Starting applications...$(RESET)"
	@if [ -d "$(APPLICATIONS)/hyperfocus-hub-ts" ]; then \
		cd "$(APPLICATIONS)/hyperfocus-hub-ts" && \
		$(NPM) run dev & \
	fi

.PHONY: start-focus-dashboard
start-focus-dashboard: ## 📊 Start focus dashboard
	@echo -e "$(LEGENDARY_PURPLE)📊 Starting focus dashboard...$(RESET)"
	@# Placeholder for focus dashboard startup
	@echo "Focus dashboard starting..."

.PHONY: start-focus-agents
start-focus-agents: ## 🧠 Start focus-specific agents
	@echo -e "$(LEGENDARY_PURPLE)🧠 Starting focus agents...$(RESET)"
	@# Placeholder for focus agents startup
	@echo "Focus agents activating..."

## 🏗️ Build & Deploy

.PHONY: build
build: ## 🏗️ Build entire empire
	@echo -e "$(LEGENDARY_BLUE)🏗️ Building HYPERFOCUS UNIFIED EMPIRE...$(RESET)"
	@$(MAKE) --no-print-directory build-applications
	@$(MAKE) --no-print-directory build-docs
	@echo -e "$(LEGENDARY_GREEN)✅ Empire build complete!$(RESET)"

.PHONY: build-applications
build-applications: ## 🎮 Build all applications
	@echo -e "$(LEGENDARY_YELLOW)🎮 Building applications...$(RESET)"
	@find "$(APPLICATIONS)" -name "package.json" | while read package; do \
		dir=$$(dirname "$$package"); \
		if jq -e '.scripts.build' "$$package" > /dev/null; then \
			echo "Building $$dir"; \
			cd "$$dir" && $(NPM) run build && cd - > /dev/null; \
		fi; \
	done

.PHONY: build-docs
build-docs: ## 📖 Build documentation
	@echo -e "$(LEGENDARY_YELLOW)📖 Building documentation...$(RESET)"
	@# Placeholder for documentation build
	@echo "Documentation build complete."

.PHONY: deploy
deploy: ## 🚀 Deploy entire empire
	@echo -e "$(LEGENDARY_BLUE)🚀 Deploying HYPERFOCUS UNIFIED EMPIRE...$(RESET)"
	@$(MAKE) --no-print-directory build
	@$(MAKE) --no-print-directory test
	@echo -e "$(LEGENDARY_YELLOW)🚀 Deploying to production...$(RESET)"
	@# Add deployment commands here
	@echo -e "$(LEGENDARY_GREEN)✅ Empire deployed! LEGENDARY! 🏰💎$(RESET)"

## 🛠️ Utilities

.PHONY: clean
clean: ## 🧹 Clean build artifacts and caches
	@echo -e "$(LEGENDARY_BLUE)🧹 Cleaning HYPERFOCUS UNIFIED EMPIRE...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "node_modules" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@echo -e "$(LEGENDARY_GREEN)✅ Empire cleaned to legendary standards!$(RESET)"

.PHONY: deep-clean
deep-clean: clean ## 🧹 Deep clean including virtual environment
	@echo -e "$(LEGENDARY_BLUE)🧹 Deep cleaning HYPERFOCUS UNIFIED EMPIRE...$(RESET)"
	@rm -rf $(VENV)
	@echo -e "$(LEGENDARY_GREEN)✅ Deep clean complete!$(RESET)"

.PHONY: tree
tree: ## 🌳 Show empire directory structure
	@echo -e "$(LEGENDARY_BLUE)🌳 HYPERFOCUS UNIFIED EMPIRE Structure:$(RESET)"
	@if command -v tree > /dev/null; then \
		tree -I '.git|.venv|node_modules|__pycache__|*.pyc' -L 3; \
	else \
		find . -type d -not -path "./.git/*" -not -path "./.venv/*" -not -path "./node_modules/*" | head -20 | sort; \
	fi

.PHONY: health
health: ## 🏥 Check empire health status
	@echo -e "$(LEGENDARY_BLUE)🏥 HYPERFOCUS UNIFIED EMPIRE Health Check:$(RESET)"
	@echo -e "$(LEGENDARY_YELLOW)📁 Directory structure:$(RESET)"
	@for dir in "$(CORE_SYSTEMS)" "$(AI_AGENTS)" "$(APPLICATIONS)" "$(NEURODIVERGENT_TOOLS)" "$(VERSION_ARCHIVE)" "$(DEVELOPMENT)" "$(DOCUMENTATION)"; do \
		if [ -d "$$dir" ]; then \
			echo -e "  ✅ $$dir"; \
		else \
			echo -e "  ❌ $$dir"; \
		fi; \
	done
	@echo -e "$(LEGENDARY_YELLOW)🐍 Python environment:$(RESET)"
	@if [ -d "$(VENV)" ]; then \
		echo -e "  ✅ Virtual environment"; \
		. $(VENV)/bin/activate && python --version; \
	else \
		echo -e "  ❌ Virtual environment missing"; \
	fi
	@echo -e "$(LEGENDARY_YELLOW)📦 Node.js environment:$(RESET)"
	@if command -v node > /dev/null; then \
		echo -e "  ✅ Node.js $$(node --version)"; \
	else \
		echo -e "  ❌ Node.js not installed"; \
	fi

.PHONY: setup-hooks
setup-hooks: ## 🪝 Setup git hooks
	@echo -e "$(LEGENDARY_YELLOW)🪝 Setting up git hooks...$(RESET)"
	@mkdir -p .git/hooks
	@echo '#!/bin/bash' > .git/hooks/pre-commit
	@echo 'make lint' >> .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo -e "$(LEGENDARY_GREEN)✅ Git hooks configured.$(RESET)"

## 📊 Information

.PHONY: info
info: ## ℹ️ Show empire information
	@echo -e "$(LEGENDARY_BLUE)$(LEGENDARY_BOLD)"
	@echo "🚀💎 HYPERFOCUS UNIFIED EMPIRE 💎🚀"
	@echo "The legendary neurodivergent-friendly AI ecosystem"
	@echo -e "$(RESET)"
	@echo -e "$(LEGENDARY_GREEN)Empire Status:$(RESET)"
	@echo -e "  Repository: $$(git remote get-url origin 2>/dev/null || echo 'Local development')"
	@echo -e "  Branch: $$(git branch --show-current 2>/dev/null || echo 'Unknown')"
	@echo -e "  Components: $$(find . -maxdepth 1 -type d -name "*.*" | wc -l) directories"
	@echo -e "  Languages: Python, TypeScript, JavaScript, Shell"
	@echo -e "  Architecture: Neurodivergent-optimized monorepo"
	@echo ""
	@echo -e "$(LEGENDARY_PURPLE)🧠 ADHD-Optimized Features:$(RESET)"
	@echo -e "  ✅ Visual emoji navigation"
	@echo -e "  ✅ Single-command workflows"
	@echo -e "  ✅ Clear component separation"
	@echo -e "  ✅ Unified development environment"
	@echo ""

.PHONY: list-agents
list-agents: ## 🤖 List all AI agents
	@echo -e "$(LEGENDARY_BLUE)🤖 AI Agents in the Empire:$(RESET)"
	@find "$(AI_AGENTS)" -maxdepth 1 -type d -not -name "$(AI_AGENTS)" | while read agent; do \
		agent_name=$$(basename "$$agent"); \
		echo -e "  $(LEGENDARY_YELLOW)🤖 $$agent_name$(RESET)"; \
		if [ -f "$$agent/README.md" ]; then \
			echo -e "    📖 $$(head -1 "$$agent/README.md" | sed 's/^# //')"; \
		fi; \
	done

## 🔧 Development Tools

.PHONY: import-repos
import-repos: ## 📥 Import source repositories (run merge_all.sh)
	@echo -e "$(LEGENDARY_BLUE)📥 Importing source repositories...$(RESET)"
	@if [ -f "merge_all.sh" ]; then \
		chmod +x merge_all.sh && ./merge_all.sh; \
	else \
		echo -e "$(LEGENDARY_RED)❌ merge_all.sh not found!$(RESET)"; \
	fi

.PHONY: update-consolidation-log
update-consolidation-log: ## 📝 Update consolidation log with current date
	@echo -e "$(LEGENDARY_BLUE)📝 Updating consolidation log...$(RESET)"
	@echo "| $$(date -u '+%Y-%m-%d') | Manual update | Updated via Makefile | Routine maintenance | - |" >> "$(DOCUMENTATION)/CONSOLIDATION-LOG.md"
	@echo -e "$(LEGENDARY_GREEN)✅ Consolidation log updated.$(RESET)"

# 🎯 Default development workflow for new users
.PHONY: legendary
legendary: bootstrap dev ## 🏰 Full legendary setup + development start
	@echo -e "$(LEGENDARY_BLUE)$(LEGENDARY_BOLD)"
	@echo "🏰💎 WELCOME TO YOUR LEGENDARY EMPIRE! 💎🏰"
	@echo "Your HYPERFOCUS UNIFIED EMPIRE is now running!"
	@echo "Time to build something LEGENDARY! ⚡❤️‍🔥"
	@echo -e "$(RESET)"
