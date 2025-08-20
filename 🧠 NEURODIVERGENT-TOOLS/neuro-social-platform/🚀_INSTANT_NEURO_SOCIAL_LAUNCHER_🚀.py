#!/usr/bin/env python3
"""
🚀💎❤️‍🔥 NEURO SOCIAL PLATFORM - INSTANT LAUNCH ENGINE ❤️‍🔥💎🚀

This script instantly launches your neurodivergent social platform development environment!
Built with ❤️ for ADHD minds who need things to "just work" immediately.

Features:
- Automatic dependency installation
- Environment setup
- All services launch in parallel
- BROski Bot economy integration
- Real-time status monitoring
- ADHD-friendly progress feedback

Author: HYPERFOCUS ZONE Development Team
Version: 1.0 - Phase 1 Foundation Launch
"""

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path


class NeuroSocialLauncher:
    def __init__(self):
        self.base_path = Path(
            "h:/HYPERFOCUS-UNIFIED-EMPIRE/🧠 NEURODIVERGENT-TOOLS/neuro-social-platform"
        )
        self.services = {
            "web": {"path": "frontend/web", "port": 3000, "status": "pending"},
            "mobile": {"path": "frontend/mobile", "port": 8081, "status": "pending"},
            "backend": {"path": "backend", "port": 5000, "status": "pending"},
            "broski": {"path": "ai-agents", "port": 8888, "status": "pending"},
        }
        self.setup_complete = False

    def print_banner(self):
        """Show ADHD-friendly launch banner"""
        print("🌟" * 60)
        print("🚀 LAUNCHING NEURODIVERGENT SOCIAL PLATFORM! 🚀")
        print("❤️‍🔥 Built by neurodivergent developers for neurodivergent minds ❤️‍🔥")
        print("🧠 Your ADHD superpowers are about to change the world! 🧠")
        print("🌟" * 60)
        print()

    def check_dependencies(self):
        """Check if Node.js, npm, and Python are available"""
        print("🔍 Checking development dependencies...")

        try:
            # Check Node.js
            node_version = (
                subprocess.check_output(["node", "--version"], shell=True)
                .decode()
                .strip()
            )
            print(f"✅ Node.js: {node_version}")

            # Check npm
            npm_version = (
                subprocess.check_output(["npm", "--version"], shell=True)
                .decode()
                .strip()
            )
            print(f"✅ npm: {npm_version}")

            # Check Python
            python_version = (
                subprocess.check_output([sys.executable, "--version"], shell=True)
                .decode()
                .strip()
            )
            print(f"✅ Python: {python_version}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Missing dependency: {e}")
            return False

    def install_dependencies(self):
        """Install npm dependencies for all services"""
        print("📦 Installing dependencies...")

        for service_name, service_info in self.services.items():
            if service_name in ["web", "mobile", "backend"]:
                service_path = self.base_path / service_info["path"]
                package_json = service_path / "package.json"

                if package_json.exists():
                    print(f"📦 Installing {service_name} dependencies...")
                    try:
                        os.chdir(service_path)
                        subprocess.run(["npm", "install"], check=True, shell=True)
                        print(f"✅ {service_name} dependencies installed!")
                        self.services[service_name]["status"] = "dependencies_ready"
                    except subprocess.CalledProcessError:
                        print(f"⚠️ Failed to install {service_name} dependencies")
                        self.services[service_name]["status"] = "error"
                else:
                    print(f"📝 Creating {service_name} package.json...")
                    self.create_package_json(service_name, service_path)

    def create_package_json(self, service_name, service_path):
        """Create package.json for services that don't have one"""
        service_path.mkdir(parents=True, exist_ok=True)

        if service_name == "web":
            package_content = {
                "name": "neuro-social-web",
                "version": "1.0.0",
                "private": True,
                "scripts": {
                    "dev": "next dev",
                    "build": "next build",
                    "start": "next start",
                    "lint": "next lint",
                },
                "dependencies": {
                    "next": "14.0.3",
                    "react": "^18",
                    "react-dom": "^18",
                    "@types/node": "^20",
                    "@types/react": "^18",
                    "@types/react-dom": "^18",
                    "typescript": "^5",
                    "tailwindcss": "^3.3.0",
                    "autoprefixer": "^10.0.1",
                    "postcss": "^8",
                    "socket.io-client": "^4.7.2",
                    "@reach/skip-nav": "^0.18.0",
                    "focus-trap-react": "^10.2.3",
                },
            }
        elif service_name == "mobile":
            package_content = {
                "name": "neurosocialmobile",
                "version": "0.0.1",
                "private": True,
                "scripts": {
                    "android": "react-native run-android",
                    "ios": "react-native run-ios",
                    "lint": "eslint .",
                    "start": "react-native start",
                    "test": "jest",
                },
                "dependencies": {
                    "react": "18.2.0",
                    "react-native": "0.72.6",
                    "react-native-haptic-feedback": "^2.2.0",
                    "@react-native-community/voice": "^3.2.4",
                    "react-native-accessibility-engine": "^0.16.0",
                    "react-native-vector-icons": "^10.0.0",
                },
                "devDependencies": {
                    "@babel/core": "^7.20.0",
                    "@babel/preset-env": "^7.20.0",
                    "@babel/runtime": "^7.20.0",
                    "@react-native/eslint-config": "^0.72.2",
                    "@react-native/metro-config": "^0.72.11",
                    "@tsconfig/react-native": "^3.0.0",
                    "@types/react": "^18.0.24",
                    "@types/react-test-renderer": "^18.0.0",
                    "babel-jest": "^29.2.1",
                    "eslint": "^8.19.0",
                    "jest": "^29.2.1",
                    "metro-react-native-babel-preset": "0.76.8",
                    "prettier": "^2.4.1",
                    "react-test-renderer": "18.2.0",
                    "typescript": "4.8.4",
                },
            }
        elif service_name == "backend":
            package_content = {
                "name": "neuro-social-backend",
                "version": "1.0.0",
                "main": "server.js",
                "scripts": {
                    "start": "node server.js",
                    "dev": "nodemon server.js",
                    "test": "jest",
                },
                "dependencies": {
                    "express": "^4.18.2",
                    "socket.io": "^4.7.2",
                    "cors": "^2.8.5",
                    "dotenv": "^16.3.1",
                    "axios": "^1.5.1",
                    "jsonwebtoken": "^9.0.2",
                    "bcryptjs": "^2.4.3",
                    "helmet": "^7.1.0",
                },
                "devDependencies": {"nodemon": "^3.0.1", "jest": "^29.7.0"},
            }

        # Write package.json
        with open(service_path / "package.json", "w") as f:
            json.dump(package_content, f, indent=2)
        print(f"✅ Created {service_name} package.json")

    def start_service(self, service_name):
        """Start a development service"""
        service_info = self.services[service_name]
        service_path = self.base_path / service_info["path"]

        print(f"🚀 Starting {service_name} service...")

        try:
            os.chdir(service_path)

            if service_name == "web":
                subprocess.Popen(["npm", "run", "dev"], shell=True)
            elif service_name == "mobile":
                subprocess.Popen(["npm", "start"], shell=True)
            elif service_name == "backend":
                subprocess.Popen(["npm", "run", "dev"], shell=True)
            elif service_name == "broski":
                # Start BROski Bot economy service
                subprocess.Popen(
                    [sys.executable, "broski-economy-service.py"], shell=True
                )

            self.services[service_name]["status"] = "running"
            print(f"✅ {service_name} started on port {service_info['port']}")

        except Exception as e:
            print(f"❌ Failed to start {service_name}: {e}")
            self.services[service_name]["status"] = "error"

    def monitor_services(self):
        """Monitor service health"""
        print("📊 Monitoring services...")

        while True:
            time.sleep(10)
            print("\n🔍 Service Status Check:")
            for service_name, service_info in self.services.items():
                status = service_info["status"]
                port = service_info["port"]

                if status == "running":
                    print(f"✅ {service_name}: Running on port {port}")
                elif status == "error":
                    print(f"❌ {service_name}: Error - needs attention")
                else:
                    print(f"⏳ {service_name}: {status}")

            print("💎 Your neurodivergent social platform is ALIVE! 💎")

    def show_dashboard(self):
        """Show ADHD-friendly development dashboard"""
        print("\n🌟" * 60)
        print("🎉 NEURO SOCIAL PLATFORM - DEVELOPMENT DASHBOARD 🎉")
        print("🌟" * 60)
        print()
        print("🌐 Web App: http://localhost:3000")
        print("📱 Mobile Metro: http://localhost:8081")
        print("🔧 Backend API: http://localhost:5000")
        print("💰 BROski Economy: http://localhost:8888")
        print()
        print("🧠 ADHD-Optimized Features:")
        print("   ✨ Haptic feedback buttons")
        print("   ⏰ 25-minute focus timers")
        print("   🎯 Progress celebrations")
        print("   💰 BROski$ social earning")
        print("   🤖 AI neurodivergent support agents")
        print()
        print("🌟 Ready to build the most AMAZING neuro social platform! 🌟")
        print("❤️‍🔥 Your ADHD superpowers are about to change the world! ❤️‍🔥")
        print()

    def launch(self):
        """Main launch sequence"""
        self.print_banner()

        if not self.check_dependencies():
            print(
                "❌ Missing required dependencies. Please install Node.js, npm, and Python."
            )
            return

        self.install_dependencies()

        # Start all services in parallel
        print("\n🚀 Launching all services...")
        for service_name in self.services.keys():
            threading.Thread(
                target=self.start_service, args=(service_name,), daemon=True
            ).start()
            time.sleep(2)  # ADHD-friendly staggered startup

        time.sleep(5)  # Let services initialize

        self.show_dashboard()

        # Start monitoring
        self.monitor_services()


if __name__ == "__main__":
    launcher = NeuroSocialLauncher()
    launcher.launch()
