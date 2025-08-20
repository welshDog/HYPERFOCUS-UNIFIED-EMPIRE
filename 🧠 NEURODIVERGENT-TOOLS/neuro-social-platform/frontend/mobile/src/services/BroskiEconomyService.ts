/**
 * 💰🤖 BROski Economy Service for Neurodivergent Social Platform 🤖💰
 *
 * This service handles BROski$ cryptocurrency integration for social earning,
 * rewards, and the revolutionary neurodivergent social economy.
 *
 * Features:
 * - Social earning tracking for ADHD/Autism/Dyslexia activities
 * - Real-time BROski$ wallet integration
 * - Dopamine-friendly reward celebrations
 * - Achievement milestone tracking
 * - Community contribution points
 * - Crisis support earning mechanisms
 *
 * @author HYPERFOCUS ZONE Development Team
 * @version 1.0 - Neurodivergent Social Economy
 */

export interface BroskiUser {
    userId: string;
    username: string;
    balance: number;
    totalEarned: number;
    earningsHistory: SocialEarning[];
    achievements: Achievement[];
    preferences: UserPreferences;
    neurodivergentProfile: NeurodivergentProfile;
    createdAt: string;
    lastActive: string;
}

export interface SocialEarning {
    earningId: string;
    userId: string;
    type: EarningType;
    amount: number;
    description: string;
    timestamp: string;
    celebrationMessage?: string;
    category: EarningCategory;
    metadata?: Record<string, any>;
}

export interface Achievement {
    id: string;
    name: string;
    description: string;
    emoji: string;
    reward: number;
    unlockedAt: string;
    category: AchievementCategory;
}

export interface UserPreferences {
    celebrationStyle: 'gentle' | 'energetic' | 'minimal';
    notificationFrequency: 'high' | 'medium' | 'low';
    motivationMessages: boolean;
    hapticFeedback: boolean;
    audioFeedback: boolean;
    visualEffects: boolean;
}

export interface NeurodivergentProfile {
    primaryCondition: 'ADHD' | 'Autism' | 'Dyslexia' | 'Multiple' | 'Other';
    supportNeeds: string[];
    strengths: string[];
    triggers: string[];
    accommodations: string[];
    focusPatterns: FocusPattern[];
}

export interface FocusPattern {
    timeOfDay: string;
    duration: number;
    effectiveness: number;
    environment: string;
}

export type EarningType =
    | 'focus_session'
    | 'help_community'
    | 'share_knowledge'
    | 'mentor_session'
    | 'create_content'
    | 'complete_challenge'
    | 'provide_support'
    | 'attend_event'
    | 'milestone_achievement'
    | 'crisis_support';

export type EarningCategory =
    | 'productivity'
    | 'social'
    | 'knowledge'
    | 'mentoring'
    | 'content'
    | 'community'
    | 'achievement'
    | 'wellness';

export type AchievementCategory =
    | 'focus_master'
    | 'community_helper'
    | 'knowledge_sharer'
    | 'milestone_achiever'
    | 'consistency_champion'
    | 'crisis_supporter'
    | 'platform_pioneer';

export class BroskiEconomyService {
    private apiUrl: string;
    private wsConnection: WebSocket | null = null;

    constructor(apiUrl: string = 'http://localhost:8888') {
        this.apiUrl = apiUrl;
        this.initializeWebSocket();
    }

    /**
     * Initialize WebSocket connection for real-time updates
     */
    private initializeWebSocket(): void {
        try {
            const wsUrl = this.apiUrl.replace('http', 'ws');
            this.wsConnection = new WebSocket(`${wsUrl}/ws`);

            this.wsConnection.onopen = () => {
                console.log('🔗 BROski Economy WebSocket connected');
            };

            this.wsConnection.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleRealtimeUpdate(data);
            };

            this.wsConnection.onerror = (error) => {
                console.error('❌ BROski Economy WebSocket error:', error);
            };
        } catch (error) {
            console.error('❌ Failed to initialize WebSocket:', error);
        }
    }

    /**
     * Handle real-time updates from the economy service
     */
    private handleRealtimeUpdate(data: any): void {
        switch (data.type) {
            case 'earning_recorded':
                this.triggerCelebration(data.earning);
                break;
            case 'achievement_unlocked':
                this.triggerAchievementCelebration(data.achievement);
                break;
            case 'balance_updated':
                this.updateUserBalance(data.userId, data.newBalance);
                break;
        }
    }

    /**
     * Get user wallet information
     */
    async getUserWallet(userId: string): Promise<BroskiUser | null> {
        try {
            const response = await fetch(`${this.apiUrl}/api/wallet/${userId}`);
            if (!response.ok) throw new Error('Failed to fetch wallet');
            return await response.json() as BroskiUser;
        } catch (error) {
            console.error('❌ Error fetching user wallet:', error);
            return null;
        }
    }

    /**
     * Record a social earning transaction
     */
    async recordSocialEarning(
        userId: string,
        type: EarningType,
        amount: number,
        description: string = '',
        metadata?: Record<string, any>
    ): Promise<SocialEarning | null> {
        try {
            const response = await fetch(`${this.apiUrl}/api/earn`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    type,
                    amount,
                    description,
                    metadata
                }),
            });

            if (!response.ok) throw new Error('Failed to record earning');

            const earning = await response.json() as SocialEarning;

            // Trigger celebration for ADHD dopamine boost
            this.triggerCelebration(earning);

            return earning;
        } catch (error) {
            console.error('❌ Error recording social earning:', error);
            return null;
        }
    }

    /**
     * Get available earning opportunities
     */
    async getEarningOpportunities(): Promise<SocialEarning[]> {
        try {
            const response = await fetch(`${this.apiUrl}/api/opportunities`);
            if (!response.ok) throw new Error('Failed to fetch opportunities');
            return await response.json();
        } catch (error) {
            console.error('❌ Error fetching earning opportunities:', error);
            return [];
        }
    }

    /**
     * Get community leaderboard
     */
    async getLeaderboard(limit: number = 10): Promise<any[]> {
        try {
            const response = await fetch(`${this.apiUrl}/api/leaderboard?limit=${limit}`);
            if (!response.ok) throw new Error('Failed to fetch leaderboard');
            return await response.json();
        } catch (error) {
            console.error('❌ Error fetching leaderboard:', error);
            return [];
        }
    }

    /**
     * Create a social trading pool
     */
    async createSocialTradingPool(
        creatorId: string,
        poolName: string,
        description: string,
        entryFee: number
    ): Promise<any> {
        try {
            const response = await fetch(`${this.apiUrl}/api/trading-pool`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    creator_id: creatorId,
                    pool_name: poolName,
                    description,
                    entry_fee: entryFee
                }),
            });

            if (!response.ok) throw new Error('Failed to create trading pool');
            return await response.json();
        } catch (error) {
            console.error('❌ Error creating trading pool:', error);
            return null;
        }
    }

    /**
     * Trigger celebration for earning (ADHD-optimized dopamine boost)
     */
    private triggerCelebration(earning: SocialEarning): void {
        // Visual celebration
        this.showCelebrationPopup(earning.celebrationMessage || '🎉 Amazing!');

        // Haptic feedback for mobile
        if ('vibrate' in navigator && earning.amount >= 10) {
            navigator.vibrate([100, 50, 100, 50, 200]);
        }

        // Audio feedback (if enabled in user preferences)
        this.playRewardSound(earning.amount);

        // Update UI elements
        this.updateBalanceDisplay(earning.userId, earning.amount);
    }

    /**
     * Trigger achievement celebration
     */
    private triggerAchievementCelebration(achievement: Achievement): void {
        console.log(`🏆 Achievement Unlocked: ${achievement.name}`);

        // More intense celebration for achievements
        if ('vibrate' in navigator) {
            navigator.vibrate([200, 100, 200, 100, 300]);
        }

        this.showAchievementModal(achievement);
        this.playAchievementSound();
    }

    /**
     * Show celebration popup
     */
    private showCelebrationPopup(message: string): void {
        // Create celebration popup element
        const popup = document.createElement('div');
        popup.className = 'broski-celebration-popup';
        popup.innerHTML = `
      <div class="celebration-content">
        <div class="celebration-emoji">🎉💰</div>
        <div class="celebration-message">${message}</div>
      </div>
    `;

        // Add ADHD-friendly styling
        popup.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
      border-radius: 15px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      z-index: 10000;
      animation: celebrationSlideIn 0.5s ease-out;
      font-family: 'Arial', sans-serif;
      text-align: center;
      max-width: 300px;
    `;

        document.body.appendChild(popup);

        // Remove after 3 seconds
        setTimeout(() => {
            popup.style.animation = 'celebrationSlideOut 0.5s ease-in';
            setTimeout(() => popup.remove(), 500);
        }, 3000);
    }

    /**
     * Show achievement modal
     */
    private showAchievementModal(achievement: Achievement): void {
        console.log(`🏆 Displaying achievement: ${achievement.name}`);
        // Implementation for achievement modal
    }

    /**
     * Play reward sound
     */
    private playRewardSound(amount: number): void {
        try {
            const audio = new Audio();

            // Different sounds based on earning amount
            if (amount >= 50) {
                audio.src = '/sounds/big-reward.mp3';
            } else if (amount >= 20) {
                audio.src = '/sounds/medium-reward.mp3';
            } else {
                audio.src = '/sounds/small-reward.mp3';
            }

            audio.volume = 0.3; // Gentle volume for sensory considerations
            audio.play().catch(() => {
                // Silently fail if audio can't play
            });
        } catch (error) {
            // Silently handle audio errors
        }
    }

    /**
     * Play achievement sound
     */
    private playAchievementSound(): void {
        try {
            const audio = new Audio('/sounds/achievement.mp3');
            audio.volume = 0.5;
            audio.play().catch(() => { });
        } catch (error) {
            // Silently handle audio errors
        }
    }

    /**
     * Update balance display in UI
     */
    private updateBalanceDisplay(userId: string, earnedAmount: number): void {
        const balanceElements = document.querySelectorAll(`[data-balance-user="${userId}"]`);
        balanceElements.forEach(element => {
            const currentBalance = parseInt(element.textContent || '0');
            element.textContent = (currentBalance + earnedAmount).toString();

            // Add temporary highlight animation
            element.classList.add('balance-updated');
            setTimeout(() => element.classList.remove('balance-updated'), 2000);
        });
    }

    /**
     * Update user balance (called from WebSocket updates)
     */
    private updateUserBalance(userId: string, newBalance: number): void {
        const balanceElements = document.querySelectorAll(`[data-balance-user="${userId}"]`);
        balanceElements.forEach(element => {
            element.textContent = newBalance.toString();
        });
    }

    /**
     * Get platform statistics
     */
    async getPlatformStats(): Promise<any> {
        try {
            const response = await fetch(`${this.apiUrl}/api/stats`);
            if (!response.ok) throw new Error('Failed to fetch platform stats');
            return await response.json();
        } catch (error) {
            console.error('❌ Error fetching platform stats:', error);
            return null;
        }
    }

    /**
     * Disconnect WebSocket
     */
    disconnect(): void {
        if (this.wsConnection) {
            this.wsConnection.close();
            this.wsConnection = null;
        }
    }
}

// Export singleton instance
export const broskiEconomy = new BroskiEconomyService();

// Export helper functions for common earning scenarios
export const EarningHelpers = {
    /**
     * Record ADHD focus session completion
     */
    async recordFocusSession(userId: string, duration: number): Promise<SocialEarning | null> {
        const amount = Math.min(Math.max(Math.floor(duration / 2), 10), 12);
        return broskiEconomy.recordSocialEarning(
            userId,
            'focus_session',
            amount,
            `Completed ${duration}-minute focus session`,
            { duration, sessionType: 'hyperfocus' }
        );
    },

    /**
     * Record community help action
     */
    async recordCommunityHelp(userId: string, helpType: string): Promise<SocialEarning | null> {
        const amount = Math.floor(Math.random() * 11) + 5; // 5-15 BROski$
        return broskiEconomy.recordSocialEarning(
            userId,
            'help_community',
            amount,
            `Helped community member: ${helpType}`,
            { helpType }
        );
    },

    /**
     * Record knowledge sharing
     */
    async recordKnowledgeSharing(userId: string, topic: string): Promise<SocialEarning | null> {
        const amount = Math.floor(Math.random() * 11) + 15; // 15-25 BROski$
        return broskiEconomy.recordSocialEarning(
            userId,
            'share_knowledge',
            amount,
            `Shared knowledge about: ${topic}`,
            { topic, category: 'neurodivergent_strategy' }
        );
    }
};

export default BroskiEconomyService;
