#!/usr/bin/env python3
"""
💰🤖 BROski Economy Service for Neuro Social Platform 🤖💰

This service provides BROski$ cryptocurrency integration for the neurodivergent social platform.
Handles social earning, rewards, and the revolutionary social crypto economy.

Features:
- Social earning tracking
- BROski$ wallet integration
- ADHD dopamine reward system
- Achievement celebrations
- Real-time balance updates
- Community trading pools

Author: HYPERFOCUS ZONE Development Team
Version: 1.0 - Social Economy Integration
"""

import datetime
import threading
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class BroskiEconomyService:
    def __init__(self):
        self.users = {}
        self.social_earnings = []
        self.trading_pools = []
        self.earning_opportunities = [
            {
                "id": "focus_session",
                "name": "Complete Focus Session",
                "description": "25-minute hyperfocus session",
                "reward_min": 10,
                "reward_max": 12,
                "category": "productivity",
            },
            {
                "id": "help_community",
                "name": "Help Community Member",
                "description": "Answer question or provide support",
                "reward_min": 5,
                "reward_max": 15,
                "category": "social",
            },
            {
                "id": "share_knowledge",
                "name": "Share ADHD Strategy",
                "description": "Share helpful ADHD coping strategy",
                "reward_min": 15,
                "reward_max": 25,
                "category": "knowledge",
            },
            {
                "id": "mentor_session",
                "name": "Mentor Another User",
                "description": "Provide 1-on-1 guidance session",
                "reward_min": 25,
                "reward_max": 50,
                "category": "mentoring",
            },
            {
                "id": "create_content",
                "name": "Create Helpful Content",
                "description": "Blog post, video, or resource",
                "reward_min": 20,
                "reward_max": 100,
                "category": "content",
            },
        ]

    def get_user_wallet(self, user_id):
        """Get or create user wallet"""
        if user_id not in self.users:
            self.users[user_id] = {
                "user_id": user_id,
                "balance": 100,  # Welcome bonus
                "total_earned": 100,
                "earnings_history": [],
                "achievements": [],
                "created_at": datetime.datetime.now().isoformat(),
            }
        return self.users[user_id]

    def record_social_earning(self, user_id, earning_type, amount, description=""):
        """Record a social earning transaction"""
        user = self.get_user_wallet(user_id)

        earning = {
            "earning_id": f"earn_{len(self.social_earnings) + 1}",
            "user_id": user_id,
            "type": earning_type,
            "amount": amount,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat(),
            "celebration": self.generate_celebration_message(earning_type, amount),
        }

        # Update user balance
        user["balance"] += amount
        user["total_earned"] += amount
        user["earnings_history"].append(earning)

        # Add to global earnings
        self.social_earnings.append(earning)

        # Check for achievements
        self.check_achievements(user_id)

        return earning

    def generate_celebration_message(self, earning_type, amount):
        """Generate ADHD-friendly celebration messages"""
        celebrations = {
            "focus_session": [
                f"🎯 FOCUS CHAMPION! +{amount} BROski$ for that amazing session!",
                f"⚡ HYPERFOCUS POWER! You earned {amount} BROski$ like a legend!",
                f"🧠 BRAIN SUPERPOWER! +{amount} BROski$ for crushing that session!",
            ],
            "help_community": [
                f"❤️ COMMUNITY HERO! +{amount} BROski$ for helping a fellow neurodivergent!",
                f"🤝 KINDNESS PAYS! You earned {amount} BROski$ for being awesome!",
                f"🌟 HELPER LEGEND! +{amount} BROski$ for spreading the love!",
            ],
            "share_knowledge": [
                f"🧠 KNOWLEDGE WIZARD! +{amount} BROski$ for sharing your wisdom!",
                f"📚 STRATEGY MASTER! You earned {amount} BROski$ for teaching others!",
                f"💡 INSIGHT CHAMPION! +{amount} BROski$ for your brilliant advice!",
            ],
        }

        import random

        return random.choice(
            celebrations.get(earning_type, [f"🎉 AMAZING! +{amount} BROski$!"])
        )

    def check_achievements(self, user_id):
        """Check and award achievements"""
        user = self.get_user_wallet(user_id)

        achievements = []

        # Total earnings achievements
        if user["total_earned"] >= 1000 and "high_earner" not in user["achievements"]:
            achievements.append(
                {
                    "id": "high_earner",
                    "name": "BROski Millionaire",
                    "description": "Earned 1000+ BROski$",
                    "reward": 100,
                    "emoji": "💰",
                }
            )

        # Focus session achievements
        focus_sessions = len(
            [e for e in user["earnings_history"] if e["type"] == "focus_session"]
        )
        if focus_sessions >= 50 and "focus_master" not in user["achievements"]:
            achievements.append(
                {
                    "id": "focus_master",
                    "name": "Hyperfocus Master",
                    "description": "Completed 50 focus sessions",
                    "reward": 250,
                    "emoji": "🎯",
                }
            )

        # Community helper achievements
        help_count = len(
            [e for e in user["earnings_history"] if e["type"] == "help_community"]
        )
        if help_count >= 25 and "community_champion" not in user["achievements"]:
            achievements.append(
                {
                    "id": "community_champion",
                    "name": "Community Champion",
                    "description": "Helped 25 community members",
                    "reward": 200,
                    "emoji": "❤️",
                }
            )

        # Award achievements
        for achievement in achievements:
            user["achievements"].append(achievement["id"])
            user["balance"] += achievement["reward"]
            user["total_earned"] += achievement["reward"]

        return achievements


# Initialize service
economy_service = BroskiEconomyService()


@app.route("/api/wallet/<user_id>", methods=["GET"])
def get_wallet(user_id):
    """Get user wallet information"""
    wallet = economy_service.get_user_wallet(user_id)
    return jsonify(wallet)


@app.route("/api/earn", methods=["POST"])
def record_earning():
    """Record a social earning"""
    data = request.json
    user_id = data.get("user_id")
    earning_type = data.get("type")
    amount = data.get("amount")
    description = data.get("description", "")

    if not all([user_id, earning_type, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    earning = economy_service.record_social_earning(
        user_id, earning_type, amount, description
    )
    return jsonify(earning)


@app.route("/api/opportunities", methods=["GET"])
def get_earning_opportunities():
    """Get available earning opportunities"""
    return jsonify(economy_service.earning_opportunities)


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Get top earners leaderboard"""
    users = list(economy_service.users.values())
    users.sort(key=lambda x: x["total_earned"], reverse=True)

    leaderboard = []
    for i, user in enumerate(users[:10]):
        leaderboard.append(
            {
                "rank": i + 1,
                "user_id": user["user_id"],
                "total_earned": user["total_earned"],
                "achievements": len(user["achievements"]),
            }
        )

    return jsonify(leaderboard)


@app.route("/api/stats", methods=["GET"])
def get_platform_stats():
    """Get platform-wide statistics"""
    total_users = len(economy_service.users)
    total_earnings = sum(
        user["total_earned"] for user in economy_service.users.values()
    )
    total_transactions = len(economy_service.social_earnings)

    return jsonify(
        {
            "total_users": total_users,
            "total_earnings": total_earnings,
            "total_transactions": total_transactions,
            "average_per_user": total_earnings / max(total_users, 1),
        }
    )


@app.route("/api/celebrate/<user_id>", methods=["POST"])
def celebrate_achievement(user_id):
    """Trigger celebration for user achievement"""
    data = request.json
    achievement_type = data.get("type", "general")

    celebrations = {
        "focus_complete": "🎯 HYPERFOCUS LEGEND! Your ADHD superpower just earned you BROski$!",
        "help_given": "❤️ COMMUNITY SUPERSTAR! Your kindness is worth its weight in BROski$!",
        "knowledge_shared": "🧠 WISDOM WIZARD! Your knowledge just made the world more neurodivergent-friendly!",
        "milestone_reached": "🏆 ACHIEVEMENT UNLOCKED! Your persistence is LEGENDARY!",
        "streak_maintained": "🔥 STREAK MASTER! Your consistency is absolutely inspiring!",
    }

    message = celebrations.get(
        achievement_type, "🌟 AMAZING WORK! You're making the neuro community proud!"
    )

    return jsonify(
        {
            "message": message,
            "emoji": "🎉",
            "sound": "celebration.mp3",
            "haptic": "success",
        }
    )


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "BROski Economy Service",
            "version": "1.0",
            "timestamp": datetime.datetime.now().isoformat(),
            "users_connected": len(economy_service.users),
            "total_earnings_distributed": sum(
                user["total_earned"] for user in economy_service.users.values()
            ),
        }
    )


def simulate_activity():
    """Simulate some platform activity for demo purposes"""
    demo_users = [
        "alice_adhd",
        "bob_autism",
        "charlie_dyslexia",
        "diana_neurodivergent",
    ]

    while True:
        time.sleep(30)  # Every 30 seconds

        import random

        user = random.choice(demo_users)
        opportunity = random.choice(economy_service.earning_opportunities)
        amount = random.randint(opportunity["reward_min"], opportunity["reward_max"])

        economy_service.record_social_earning(
            user, opportunity["id"], amount, f"Demo: {opportunity['name']}"
        )

        print(
            f"💰 Demo activity: {user} earned {amount} BROski$ for {opportunity['name']}"
        )


if __name__ == "__main__":
    print("💰🤖 Starting BROski Economy Service for Neuro Social Platform 🤖💰")
    print("🌟 Serving social earning, rewards, and neurodivergent community economy!")
    print("❤️‍🔥 Built with love for ADHD minds who deserve to be rewarded! ❤️‍🔥")
    print()
    print("📊 Service running on: http://localhost:8888")
    print("🧠 Ready to power the most rewarding neuro social platform ever!")
    print()

    # Start demo activity in background
    activity_thread = threading.Thread(target=simulate_activity, daemon=True)
    activity_thread.start()

    app.run(host="0.0.0.0", port=8888, debug=True)
