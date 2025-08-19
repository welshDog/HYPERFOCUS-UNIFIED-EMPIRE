import logging
import time
from datetime import datetime
import json
import traceback

logger = logging.getLogger("BROski.NotificationService")

class NotificationService:
    def __init__(self, config):
        """
        Initialize the notification service with configuration
        
        Args:
            config (dict): Bot configuration containing notification settings
        """
        self.config = config
        self.telegram_enabled = config["notifications"]["telegram"]["enabled"]
        self.email_enabled = config["notifications"]["email"]["enabled"]
        
        # Initialize notification providers
        self.providers = []
        
        # Setup Telegram if enabled
        if self.telegram_enabled:
            try:
                telegram_config = config["notifications"]["telegram"]
                self.telegram = TelegramProvider(
                    bot_token=telegram_config["bot_token"], 
                    chat_id=telegram_config["chat_id"]
                )
                self.providers.append(self.telegram)
                logger.info("Telegram notifications enabled")
            except ImportError:
                logger.warning("Could not import telegram_provider. Install python-telegram-bot package.")
                self.telegram_enabled = False
            except Exception as e:
                logger.error(f"Failed to initialize Telegram notifications: {str(e)}")
                self.telegram_enabled = False
        
        # Setup Email if enabled
        # Setup Email if enabled
        if self.email_enabled:
            try:
                email_config = config["notifications"]["email"]
                self.email = EmailProvider(
                    smtp_server=email_config["smtp_server"],
                    smtp_port=email_config["smtp_port"],
                    sender_email=email_config["sender_email"],
                    password=email_config["password"],
                    receiver_email=email_config["receiver_email"]
                )
                logger.info("Email notifications enabled")
            except ImportError:
                logger.warning("Could not import email_provider.")
                self.email_enabled = False
            except Exception as e:
                logger.error(f"Failed to initialize Email notifications: {str(e)}")
                self.email_enabled = False
        
        # Rate limiting to prevent spam
        self.last_notification_time = {}
        self.min_interval = 10  # Minimum seconds between notifications of same type
        
        logger.info("Notification service initialized")
    
    def _should_send(self, notification_type):
        """Rate limiting check for notifications"""
        current_time = time.time()
        if notification_type in self.last_notification_time:
            time_since_last = current_time - self.last_notification_time[notification_type]
            if time_since_last < self.min_interval:
                return False
        
        self.last_notification_time[notification_type] = current_time
        return True
    
    def send_notification(self, message, notification_type="info", important=False):
        """
        Generic method to send notifications through all enabled channels
        
        Args:
            message (str): Notification message
            notification_type (str): Type of notification (info, warning, error, trade)
            important (bool): Whether this is an important notification that bypasses rate limiting
        """
        # Apply rate limiting unless it's an important notification
        if not important and not self._should_send(notification_type):
            logger.debug(f"Skipping {notification_type} notification due to rate limiting")
            return
        
        # Format timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # Add emoji based on notification type
        if notification_type == "trade_buy":
            formatted_message = f"🟢 BUY: {formatted_message}"
        elif notification_type == "trade_sell":
            formatted_message = f"🔴 SELL: {formatted_message}"
        elif notification_type == "error":
            formatted_message = f"❌ ERROR: {formatted_message}"
        elif notification_type == "warning":
            formatted_message = f"⚠️ WARNING: {formatted_message}"
        elif notification_type == "info":
            formatted_message = f"ℹ️ {formatted_message}"
        
        # Log the notification
        logger.info(f"Notification ({notification_type}): {message}")
        
        # Send through all providers
        for provider in self.providers:
            try:
                provider.send(formatted_message, notification_type)
            except Exception as e:
                logger.error(f"Failed to send {notification_type} notification: {str(e)}")
    
    def send_trade_notification(self, execution_result):
        """
        Send notification about a trade execution
        
        Args:
            execution_result (dict): Trade execution result
        """
        try:
            trade_type = execution_result.get("type", "unknown").lower()
            pair = execution_result.get("symbol", "unknown")
            price = execution_result.get("price", 0)
            amount = execution_result.get("amount", 0)
            
            # Calculate trade value
            value = price * amount
            
            message = f"Trade executed: {trade_type.upper()} {amount} {pair} @ {price} (Value: {value:.2f})"
            
            self.send_notification(
                message, 
                notification_type=f"trade_{trade_type}", 
                important=True
            )
        except Exception as e:
            logger.error(f"Error formatting trade notification: {str(e)}")
            self.send_error_notification(f"Trade notification failed: {str(e)}")
    
    def send_error_notification(self, error_message):
        """
        Send notification about an error
        
        Args:
            error_message (str): Error message
        """
        self.send_notification(error_message, notification_type="error", important=True)
    
    def send_signal_notification(self, signal):
        """
        Send notification about a trading signal
        
        Args:
            signal (dict): Trading signal data
        """
        try:
            signal_type = signal.get("type", "unknown").lower()
            pair = signal.get("symbol", "unknown")
            price = signal.get("price", 0)
            
            # Get strategy-specific info
            strategy = signal.get("strategy", "unknown")
            
            # Additional info based on strategy
            details = ""
            if "rsi" in strategy:
                details = f"RSI: {signal.get('rsi', 'N/A')}"
            elif "macd" in strategy:
                details = f"MACD/Signal: {signal.get('macd', 'N/A')}/{signal.get('signal', 'N/A')}"
            
            message = f"Signal: {signal_type.upper()} {pair} @ {price} ({strategy.upper()}) {details}"
            
            self.send_notification(
                message, 
                notification_type=f"signal_{signal_type}"
            )
        except Exception as e:
            logger.error(f"Error formatting signal notification: {str(e)}")
    
    def send_status_notification(self, status_data):
        """
        Send periodic status update
        
        Args:
            status_data (dict): Bot status information
        """
        try:
            # Format status message
            pair = status_data.get("trading_pair", "unknown")
            price = status_data.get("current_price", 0)
            strategy = status_data.get("active_strategy", "unknown")
            
            message = (
                f"Status Update - {pair} @ {price}\n"
                f"Strategy: {strategy}\n"
                f"24h Change: {status_data.get('24h_change', '0')}%\n"
                f"Auto-trade: {'ON' if status_data.get('auto_trade', False) else 'OFF'}"
            )
            
            self.send_notification(
                message, 
                notification_type="status"
            )
        except Exception as e:
            logger.error(f"Error formatting status notification: {str(e)}")


class TelegramProvider:
    """Basic implementation of Telegram notification provider"""
    
    def __init__(self, bot_token, chat_id):
        """Initialize Telegram provider"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        
        # Initialize bot
        try:
            import telegram
            self.bot = telegram.Bot(token=bot_token)
            logger.info("Telegram bot initialized")
        except ImportError:
            logger.error("Telegram package not installed. Run: pip install python-telegram-bot")
            raise
        except Exception as e:
            logger.error(f"Error initializing Telegram bot: {str(e)}")
            raise
    
    def send(self, message, notification_type="info"):
        """Send message via Telegram"""
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="HTML")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            logger.debug(traceback.format_exc())
            return False


class EmailProvider:
    """Basic implementation of Email notification provider"""
    
    def __init__(self, smtp_server, smtp_port, sender_email, password, receiver_email):
        """Initialize Email provider"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = receiver_email
    
    def send(self, message, notification_type="info"):
        """Send message via Email"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            
            # Set subject based on notification type
            if "trade" in notification_type:
                msg["Subject"] = f"BROski Bot - Trade Notification"
            elif notification_type == "error":
                msg["Subject"] = f"BROski Bot - ERROR ALERT"
            else:
                msg["Subject"] = f"BROski Bot - Notification"
            
            # Attach message body
            msg.attach(MIMEText(message, "plain"))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            logger.error(f"Error sending Email: {str(e)}")
            return False
