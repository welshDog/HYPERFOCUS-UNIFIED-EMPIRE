/**
 * BROski Bot Economy Integration Service
 * Connects social platform with crypto trading economy
 */

import axios from 'axios';

interface BroskiUser {
    id: string;
    wallet_address: string;
    broski_balance: number;
    trading_level: 'BEGINNER' | 'INTERMEDIATE' | 'LEGENDARY';
    total_earnings: number;
    social_contributions: number;
}

interface BroskiTransaction {
    id: string;
    user_id: string;
    amount: number;
    type: 'EARN' | 'SPEND' | 'TRADE';
    category: string;
    description: string;
    timestamp: Date;
}

interface SocialEarning {
    action: 'POST_HELPFUL_COMMENT' | 'CREATE_VIRAL_CONTENT' | 'MENTOR_USER' | 'COMPLETE_FOCUS_SESSION';
    base_reward: number;
    multiplier: number;
    description: string;
}

class BroskiEconomyService {
    private baseURL = process.env.BROSKI_BOT_API_URL || 'http://localhost:3001/api';
    private apiKey = process.env.BROSKI_API_KEY;

    async getUserWallet(userId: string): Promise<BroskiUser | null> {
        try {
            const response = await axios.get(`${this.baseURL}/wallet/${userId}`, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch user wallet:', error);
            return null;
        }
    }

    async recordSocialEarning(
        userId: string,
        earning: SocialEarning
    ): Promise<BroskiTransaction | null> {
        try {
            const finalAmount = earning.base_reward * earning.multiplier;

            const transaction = {
                user_id: userId,
                amount: finalAmount,
                type: 'EARN' as const,
                category: 'SOCIAL_CONTRIBUTION',
                description: earning.description,
                action: earning.action
            };

            const response = await axios.post(`${this.baseURL}/transactions`, transaction, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });

            // Trigger dopamine notification for ADHD users
            this.triggerEarningNotification(userId, finalAmount, earning.action);

            return response.data;
        } catch (error) {
            console.error('Failed to record social earning:', error);
            return null;
        }
    }

    async getEarningOpportunities(): Promise<SocialEarning[]> {
        return [
            {
                action: 'POST_HELPFUL_COMMENT',
                base_reward: 5,
                multiplier: 1.0,
                description: 'Help someone in the community'
            },
            {
                action: 'CREATE_VIRAL_CONTENT',
                base_reward: 50,
                multiplier: 2.0,
                description: 'Create content that goes viral'
            },
            {
                action: 'MENTOR_USER',
                base_reward: 25,
                multiplier: 1.5,
                description: 'Mentor a new community member'
            },
            {
                action: 'COMPLETE_FOCUS_SESSION',
                base_reward: 10,
                multiplier: 1.2,
                description: 'Complete a 25-minute focus session'
            }
        ];
    }

    private async triggerEarningNotification(
        userId: string,
        amount: number,
        action: string
    ): Promise<void> {
        // ADHD-friendly dopamine boost notification
        const notification = {
            user_id: userId,
            title: 'BROski$ EARNED!',
            message: `Amazing! You just earned ${amount} BROski$ for ${action}!`,
            type: 'EARNINGS_CELEBRATION',
            dopamine_boost: true,
            sound: 'success_chime',
            vibration: 'celebration'
        };

        try {
            await axios.post(`${this.baseURL}/notifications`, notification, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });
        } catch (error) {
            console.error('Failed to send earning notification:', error);
        }
    }
}

export { BroskiEconomyService, type BroskiTransaction, type BroskiUser, type SocialEarning };
