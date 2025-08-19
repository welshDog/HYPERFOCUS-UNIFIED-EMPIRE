# 🔄 MIGRATION GUIDE

This guide helps you transition from legacy HyperFocus versions to the Unified Empire.

## 📍 Path Mapping: Where Everything Moved

### From V8.5 Legacy
| Old Path  | New Path                                | Notes                        |
| --------- | --------------------------------------- | ---------------------------- |
| `src/`    | `📚 VERSION-ARCHIVE/v8.5-legacy/src/`    | Preserved for reference      |
| `config/` | `📚 VERSION-ARCHIVE/v8.5-legacy/config/` | Legacy config patterns       |
| `tools/`  | `🧠 NEURODIVERGENT-TOOLS/`               | Neurodivergent tools evolved |
| `docs/`   | `📖 DOCUMENTATION/legacy/v8.5/`          | Historical documentation     |

### From V9 Evolution  
| Old Path             | New Path                          | Notes                    |
| -------------------- | --------------------------------- | ------------------------ |
| `src/core/`          | `🚀 CORE-SYSTEMS/`                 | Core functionality moved |
| `src/agents/`        | `🤖 AI-AGENTS/`                    | AI components separated  |
| `src/apps/`          | `🎮 APPLICATIONS/`                 | Applications organized   |
| `evolution-scripts/` | `📚 VERSION-ARCHIVE/v9-evolution/` | Scripts preserved        |
| `documentation/`     | `📖 DOCUMENTATION/evolution/v9/`   | Evolution docs           |

### From V9.5 (Current Base)
| V9.5 Component | New Location                             | Status       |
| -------------- | ---------------------------------------- | ------------ |
| Main dashboard | `🚀 CORE-SYSTEMS/chaos-genius-dashboard/` | Enhanced     |
| User interface | `🎮 APPLICATIONS/hyperfocus-hub-ts/`      | Modernized   |
| Configuration  | `🛠️ DEVELOPMENT/config/`                  | Unified      |
| Testing        | `🛠️ DEVELOPMENT/testing/`                 | Standardized |

### Satellite Applications
| Repository         | New Location                        | Integration           |
| ------------------ | ----------------------------------- | --------------------- |
| `BROski-BOT`       | `🤖 AI-AGENTS/broski-bot/`           | Agent ecosystem       |
| `broski-clanverse` | `🤖 AI-AGENTS/discord-manager/`      | Community automation  |
| `filter_Zone`      | `🎮 APPLICATIONS/filter-zone/`       | Content processing    |
| `NeighborWork`     | `🎮 APPLICATIONS/neighbor-work/`     | Collaboration tools   |
| `HyperFocus-Hub`   | `🎮 APPLICATIONS/hyperfocus-hub/`    | Legacy hub preserved  |
| `hyperfocushub`    | `🎮 APPLICATIONS/hyperfocus-hub-ts/` | Modern TypeScript hub |

## 🔧 Configuration Migration

### Environment Variables
```bash
# Old V9.5 style
HYPERFOCUS_API_KEY=xxx
DISCORD_TOKEN=xxx
TRADING_API_KEY=xxx

# New unified style  
EMPIRE_API_KEY=xxx
EMPIRE_DISCORD_TOKEN=xxx
EMPIRE_TRADING_API_KEY=xxx
```

### Database Connections
```python
# Old scattered configs
DATABASE_URL = "sqlite:///app.db"
REDIS_URL = "redis://localhost:6379"

# New unified config
EMPIRE_DATABASE_URL = "sqlite:///🛠️ DEVELOPMENT/data/empire.db"
EMPIRE_REDIS_URL = "redis://localhost:6379/empire"
```

### API Endpoints
| Old Endpoint    | New Endpoint                    | Notes                 |
| --------------- | ------------------------------- | --------------------- |
| `/api/v1/focus` | `/api/empire/v1/focus`          | Versioned empire API  |
| `/api/trading`  | `/api/empire/v1/agents/trading` | Agent-specific routes |
| `/api/discord`  | `/api/empire/v1/agents/discord` | Unified agent API     |

## 🔄 Code Migration Examples

### Importing Modules
```python
# Old V9.5 imports
from hyperfocus.core import FocusEngine
from hyperfocus.agents import TradingBot

# New unified imports  
from empire.core_systems import FocusEngine
from empire.ai_agents.trading import TradingBot
```

### Configuration Loading
```python
# Old scattered config
import config.trading as trading_config
import config.discord as discord_config

# New unified config
from empire.development.config import EmpireConfig
config = EmpireConfig.load()
```

### Service Registration
```typescript
// Old individual services
const focusService = new FocusService(config.focus);
const tradingService = new TradingService(config.trading);

// New empire service mesh
import { EmpireServiceMesh } from '@empire/core-systems';
const services = new EmpireServiceMesh(config);
```

## 📚 Legacy Access Patterns

### Running Legacy Versions
```bash
# Access V8.5 legacy for reference
cd "📚 VERSION-ARCHIVE/v8.5-legacy"
python legacy_runner.py

# Access V9 evolution scripts
cd "📚 VERSION-ARCHIVE/v9-evolution"
./evolution_script.sh

# Run current unified empire
make dev  # From empire root
```

### Data Migration Tools
```bash
# Migrate V8.5 data to empire format
make migrate-v85-data

# Migrate V9 configurations  
make migrate-v9-config

# Import legacy user preferences
make import-legacy-preferences
```

## 🧠 Workflow Migration (ADHD-Optimized)

### Old Multi-Command Workflows
```bash
# V9.5 development workflow (many steps)
cd hyperfocus-v9.5
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Open new terminal
cd ../broski-bot
npm install
npm run dev
# Open another terminal
cd ../discord-manager  
python bot.py
```

### New Single-Command Workflows
```bash
# Empire unified workflow (one command)
make dev  # Starts everything with hot reloading
```

### Focus Session Migration
```bash
# Old: Multiple scattered commands
./start_focus_v9.sh
./start_trading_bot.sh  
./start_discord.sh

# New: Unified focus sessions
make focus-session  # Starts coordinated focus environment
```

## ⚠️ Breaking Changes

### Removed Features
- **V8.5 Legacy GUI**: Replaced with modern dashboard
- **Scattered Config Files**: Unified in development layer
- **Individual Service Scripts**: Replaced with make commands

### Changed Behavior  
- **API Authentication**: Now uses empire-wide tokens
- **Database Schema**: Unified across all components
- **Logging Format**: Standardized empire-wide logging

### Migration Required
- **Custom Plugins**: Need registration in empire service mesh
- **External Integrations**: Update endpoints to empire API
- **Backup Scripts**: Update paths to new structure

## 🛠️ Migration Tools

### Automated Migration
```bash
# Run the full migration assistant
make migrate-from-legacy

# Migrate specific components
make migrate-v85-config
make migrate-v9-data  
make migrate-satellite-apps
```

### Manual Migration Checklist
- [ ] Update environment variables to empire format
- [ ] Migrate custom configurations to unified config
- [ ] Update external service endpoints
- [ ] Test legacy data access patterns
- [ ] Verify agent orchestration works
- [ ] Update deployment scripts
- [ ] Migrate custom monitoring/alerting

## 🔍 Verification Steps

### Post-Migration Testing
```bash
# Verify all systems operational
make health-check

# Test legacy data access
make test-legacy-access

# Validate agent communication
make test-agent-mesh

# Check focus workflow integration
make test-focus-workflows
```

### Rollback Strategy
```bash
# If migration issues occur, rollback is available
make rollback-to-v95  # Emergency rollback to V9.5
```

## 📞 Migration Support

### Common Issues
- **Import Errors**: Check new module paths in migration guide
- **Config Errors**: Verify environment variable naming
- **Permission Errors**: Check unified authentication setup
- **Performance Issues**: Review resource allocation in empire

### Getting Help
- **Migration Logs**: Check `🛠️ DEVELOPMENT/logs/migration.log`
- **Documentation**: See `📖 DOCUMENTATION/` for detailed guides
- **Legacy Reference**: Access preserved versions in `📚 VERSION-ARCHIVE/`

---

*Migration is a journey, not a destination. Take it step by step, and your empire will be legendary.* ⚡
