import logging
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import numpy as np
from collections import defaultdict

# Add path fixing for imports
import sys
import os
from pathlib import Path

# Ensure we can import from any directory
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



logger = logging.getLogger("BROski.PerformanceTracker")

class PerformanceTracker:
    """
    Tracks trading performance metrics for BROski Bot.
    Calculates detailed statistics and provides visualization capabilities.
    """
    
    def __init__(self, config):
        """
        Initialize performance tracker with configuration
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        self.trades = []
        self.open_trades = []
        self.closed_trades = []
        
        # Initialize metrics dictionary with comprehensive metrics
        self.metrics = {
            # Overall performance
            'total_profit_loss': 0.0,
            'total_profit_loss_pct': 0.0,
            'win_rate': 0.0,
            'total_trades': 0,
            'open_trades': 0,
            'closed_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'breakeven_trades': 0,
            
            # Profit metrics
            'gross_profit': 0.0,
            'gross_loss': 0.0,
            'average_profit': 0.0,
            'average_loss': 0.0,
            'largest_profit': 0.0,
            'largest_loss': 0.0,
            'profit_factor': 0.0,
            
            # Risk metrics
            'max_drawdown': 0.0,
            'max_drawdown_pct': 0.0,
            'risk_reward_ratio': 0.0,
            'sharpe_ratio': 0.0,
            
            # Time metrics
            'avg_trade_duration': 0.0,
            'avg_bars_in_trades': 0,
            'total_trading_days': 0,
            
            # Strategy metrics
            'strategy_performance': {},
            
            # Recent activity
            'recent_trades': []
        }
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Load any existing trade history
        self._load_trades()
        
        logger.info("Performance tracker initialized with enhanced metrics")
    
    def _load_trades(self):
        """Load trades from file if it exists"""
        try:
            trade_file = os.path.join('logs', 'trade_history.json')
            if os.path.exists(trade_file):
                with open(trade_file, 'r') as f:
                    self.trades = json.load(f)
                    
                # Separate into open and closed trades
                self.open_trades = [t for t in self.trades if t.get('status') == 'open']
                self.closed_trades = [t for t in self.trades if t.get('status') == 'closed']
                
                logger.info(f"Loaded {len(self.trades)} trades from history file")
                self.update_metrics()
        except Exception as e:
            logger.error(f"Error loading trade history: {str(e)}")
    
    def _save_trades(self):
        """Save trades to file"""
        try:
            trade_file = os.path.join('logs', 'trade_history.json')
            with open(trade_file, 'w') as f:
                json.dump(self.trades, f, indent=4)
            logger.debug("Trade history saved to file")
        except Exception as e:
            logger.error(f"Error saving trade history: {str(e)}")
    
    def record_trade(self, execution_result):
        """
        Record a new trade
        
        Args:
            execution_result (dict): Trade execution details
        """
        try:
            # Validate execution result
            required_fields = ['type', 'symbol', 'price', 'timestamp']
            for field in required_fields:
                if field not in execution_result:
                    logger.warning(f"Missing required field in execution result: {field}")
                    execution_result[field] = "unknown"
            
            # Add additional fields
            execution_result['id'] = len(self.trades) + 1
            if 'timestamp' not in execution_result:
                execution_result['timestamp'] = datetime.now().isoformat()
            if 'status' not in execution_result:
                execution_result['status'] = 'open'
            
            # Calculate trade value
            if 'value' not in execution_result and 'amount' in execution_result and 'price' in execution_result:
                execution_result['value'] = float(execution_result['amount']) * float(execution_result['price'])
            
            # Add to trades list
            self.trades.append(execution_result)
            
            # Add to open trades if it's a new position
            if execution_result.get('status') == 'open':
                self.open_trades.append(execution_result)
            
            # Add to closed trades if it's a closed position
            elif execution_result.get('status') == 'closed':
                self.closed_trades.append(execution_result)
            
            # Update metrics after recording
            self.update_metrics()
            self._save_trades()
            
            logger.info(f"Recorded trade: {execution_result['type']} {execution_result.get('amount', 'unknown')} {execution_result['symbol']} at {execution_result['price']}")
            
        except Exception as e:
            logger.error(f"Error recording trade: {str(e)}")
    
    def close_trade(self, trade_id, close_price, close_time=None, pnl=None, pnl_pct=None):
        """
        Close a trade and update metrics
        
        Args:
            trade_id: ID of the trade to close
            close_price: Closing price
            close_time: Closing timestamp (optional)
            pnl: Profit/loss (optional)
            pnl_pct: Profit/loss percentage (optional)
        
        Returns:
            dict: Updated trade object or None if not found
        """
        try:
            # Find the trade to close
            trade = None
            for t in self.trades:
                if t.get('id') == trade_id:
                    trade = t
                    break
            
            if trade is None:
                logger.warning(f"Trade with ID {trade_id} not found")
                return None
            
            # Skip if already closed
            if trade.get('status') == 'closed':
                logger.warning(f"Trade {trade_id} is already closed")
                return trade
            
            # Update trade with closing details
            trade['close_price'] = close_price
            trade['close_time'] = close_time if close_time else datetime.now().isoformat()
            trade['status'] = 'closed'
            
            # Calculate P&L if not provided
            if pnl is None and 'price' in trade and 'amount' in trade:
                if trade['type'].lower() == 'buy':
                    pnl = (float(close_price) - float(trade['price'])) * float(trade['amount'])
                    if pnl_pct is None:
                        pnl_pct = ((float(close_price) / float(trade['price'])) - 1) * 100
                else:  # sell
                    pnl = (float(trade['price']) - float(close_price)) * float(trade['amount'])
                    if pnl_pct is None:
                        pnl_pct = ((float(trade['price']) / float(close_price)) - 1) * 100
            
            trade['pnl'] = pnl
            trade['pnl_pct'] = pnl_pct
            
            # Move from open to closed trades
            if trade in self.open_trades:
                self.open_trades.remove(trade)
            self.closed_trades.append(trade)
            
            # Update metrics and save
            self.update_metrics()
            self._save_trades()
            
            logger.info(f"Closed trade {trade_id}: {trade.get('type')} {trade.get('amount', 'unknown')} {trade.get('symbol')} at {close_price}, P&L: {pnl}")
            
            return trade
            
        except Exception as e:
            logger.error(f"Error closing trade: {str(e)}")
            return None
    
    def update_metrics(self):
        """Calculate and update all performance metrics"""
        try:
            # Basic counts
            self.metrics['total_trades'] = len(self.trades)
            self.metrics['open_trades'] = len(self.open_trades)
            self.metrics['closed_trades'] = len(self.closed_trades)
            
            # Skip further calculations if no closed trades
            if not self.closed_trades:
                logger.debug("No closed trades to calculate metrics")
                return
            
            # Profit/loss metrics
            winning_trades = [t for t in self.closed_trades if t.get('pnl', 0) > 0]
            losing_trades = [t for t in self.closed_trades if t.get('pnl', 0) < 0]
            breakeven_trades = [t for t in self.closed_trades if t.get('pnl', 0) == 0]
            
            self.metrics['winning_trades'] = len(winning_trades)
            self.metrics['losing_trades'] = len(losing_trades)
            self.metrics['breakeven_trades'] = len(breakeven_trades)
            
            # Calculate win rate
            if self.metrics['closed_trades'] > 0:
                self.metrics['win_rate'] = (self.metrics['winning_trades'] / self.metrics['closed_trades']) * 100
            
            # Calculate profit metrics
            self.metrics['gross_profit'] = sum(t.get('pnl', 0) for t in winning_trades)
            self.metrics['gross_loss'] = sum(t.get('pnl', 0) for t in losing_trades)
            self.metrics['total_profit_loss'] = self.metrics['gross_profit'] + self.metrics['gross_loss']
            
            if winning_trades:
                self.metrics['average_profit'] = self.metrics['gross_profit'] / len(winning_trades)
                self.metrics['largest_profit'] = max(t.get('pnl', 0) for t in winning_trades)
            
            if losing_trades:
                self.metrics['average_loss'] = self.metrics['gross_loss'] / len(losing_trades)
                self.metrics['largest_loss'] = min(t.get('pnl', 0) for t in losing_trades)
            
            # Calculate profit factor
            if self.metrics['gross_loss'] != 0:
                self.metrics['profit_factor'] = abs(self.metrics['gross_profit'] / self.metrics['gross_loss'])
            
            # Calculate risk-reward ratio
            if self.metrics['average_loss'] != 0:
                self.metrics['risk_reward_ratio'] = abs(self.metrics['average_profit'] / self.metrics['average_loss'])
            
            # Calculate maximum drawdown
            self._calculate_drawdown()
            
            # Strategy performance
            self._calculate_strategy_performance()
            
            # Update recent trades
            self._update_recent_trades()
            
            logger.debug("Performance metrics updated")
        
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
    
    def _calculate_drawdown(self):
        """Calculate maximum drawdown"""
        try:
            # Need closed trades with timestamps and PnL
            if not self.closed_trades:
                return
            
            # Sort trades by timestamp
            sorted_trades = sorted(self.closed_trades, key=lambda x: x.get('timestamp', ''))
            
            # Create equity curve
            equity = [0]
            peak = 0
            drawdown = 0
            max_drawdown = 0
            
            for trade in sorted_trades:
                pnl = trade.get('pnl', 0)
                equity.append(equity[-1] + pnl)
                
                if equity[-1] > peak:
                    peak = equity[-1]
                
                drawdown = peak - equity[-1]
                max_drawdown = max(max_drawdown, drawdown)
            
            # Store max drawdown in metrics
            self.metrics['max_drawdown'] = max_drawdown
            
            # Calculate percentage drawdown
            if peak > 0:
                self.metrics['max_drawdown_pct'] = (max_drawdown / peak) * 100
            
        except Exception as e:
            logger.error(f"Error calculating drawdown: {str(e)}")
    
    def _calculate_strategy_performance(self):
        """Calculate performance metrics by strategy"""
        try:
            # Group trades by strategy
            strategy_trades = defaultdict(list)
            
            for trade in self.closed_trades:
                strategy = trade.get('strategy', 'unknown')
                strategy_trades[strategy].append(trade)
            
            # Calculate metrics for each strategy
            strategy_metrics = {}
            
            for strategy, trades in strategy_trades.items():
                winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
                
                metrics = {
                    'total_trades': len(trades),
                    'winning_trades': len(winning_trades),
                    'win_rate': (len(winning_trades) / len(trades) * 100) if trades else 0,
                    'total_profit': sum(t.get('pnl', 0) for t in trades),
                    'avg_profit_per_trade': sum(t.get('pnl', 0) for t in trades) / len(trades) if trades else 0
                }
                
                strategy_metrics[strategy] = metrics
            
            self.metrics['strategy_performance'] = strategy_metrics
            
        except Exception as e:
            logger.error(f"Error calculating strategy performance: {str(e)}")
    
    def _update_recent_trades(self):
        """Update the list of recent trades"""
        try:
            # Sort trades by timestamp (newest first)
            sorted_trades = sorted(
                self.closed_trades, 
                key=lambda x: x.get('timestamp', ''), 
                reverse=True
            )
            
            # Keep only the most recent trades
            recent_limit = 10
            self.metrics['recent_trades'] = sorted_trades[:recent_limit]
            
        except Exception as e:
            logger.error(f"Error updating recent trades: {str(e)}")
    
    def get_metrics(self):
        """
        Get current performance metrics
        
        Returns:
            dict: Performance metrics
        """
        return self.metrics
    
    def get_equity_curve(self):
        """
        Get equity curve data for visualization
        
        Returns:
            tuple: (dates, equity_values)
        """
        try:
            if not self.closed_trades:
                return [], []
            
            # Sort trades by timestamp
            sorted_trades = sorted(self.closed_trades, key=lambda x: x.get('timestamp', ''))
            
            dates = []
            equity = [0]
            
            for trade in sorted_trades:
                try:
                    # Parse timestamp
                    timestamp = trade.get('timestamp')
                    if isinstance(timestamp, str):
                        date = datetime.fromisoformat(timestamp)
                    else:
                        date = datetime.now()
                    
                    dates.append(date)
                    equity.append(equity[-1] + trade.get('pnl', 0))
                except Exception as e:
                    logger.warning(f"Error processing trade for equity curve: {e}")
            
            return dates, equity[1:]  # Skip the first zero
            
        except Exception as e:
            logger.error(f"Error getting equity curve: {str(e)}")
            return [], []
    
    def generate_report(self, output_file="performance_report.html"):
        """
        Generate an HTML performance report
        
        Args:
            output_file: Output file path for the report
            
        Returns:
            bool: Success/failure
        """
        try:
            # Basic HTML template
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>BROski Trading Performance Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1, h2 { color: #333; }
                    .metrics { margin: 20px 0; }
                    table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                    th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
                    th { background-color: #f2f2f2; }
                    .win { color: green; }
                    .loss { color: red; }
                    .chart { width: 100%; height: 400px; margin: 20px 0; }
                </style>
            </head>
            <body>
                <h1>BROski Trading Performance Report</h1>
                <p>Generated on: {date}</p>
                
                <h2>Overall Performance</h2>
                <div class="metrics">
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Total P&L</td><td class="{profit_class}">{total_pnl}</td></tr>
                        <tr><td>Win Rate</td><td>{win_rate}%</td></tr>
                        <tr><td>Total Trades</td><td>{total_trades}</td></tr>
                        <tr><td>Profit Factor</td><td>{profit_factor}</td></tr>
                        <tr><td>Max Drawdown</td><td>{max_drawdown}</td></tr>
                    </table>
                </div>
                
                <h2>Trade Statistics</h2>
                <div class="metrics">
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Winning Trades</td><td>{winning_trades}</td></tr>
                        <tr><td>Losing Trades</td><td>{losing_trades}</td></tr>
                        <tr><td>Average Win</td><td class="win">{avg_win}</td></tr>
                        <tr><td>Average Loss</td><td class="loss">{avg_loss}</td></tr>
                        <tr><td>Largest Win</td><td class="win">{largest_win}</td></tr>
                        <tr><td>Largest Loss</td><td class="loss">{largest_loss}</td></tr>
                    </table>
                </div>
                
                <h2>Strategy Performance</h2>
                <div class="metrics">
                    <table>
                        <tr><th>Strategy</th><th>Win Rate</th><th>Total P&L</th><th>Trades</th></tr>
                        {strategy_rows}
                    </table>
                </div>
                
                <h2>Recent Trades</h2>
                <div class="metrics">
                    <table>
                        <tr><th>Date</th><th>Type</th><th>Symbol</th><th>Price</th><th>P&L</th></tr>
                        {trade_rows}
                    </table>
                </div>
                
                <p>End of report.</p>
            </body>
            </html>
            """
            
            # Generate strategy rows
            strategy_rows = ""
            for strategy, metrics in self.metrics['strategy_performance'].items():
                pnl_class = "win" if metrics['total_profit'] >= 0 else "loss"
                strategy_rows += f"""
                <tr>
                    <td>{strategy}</td>
                    <td>{metrics['win_rate']:.1f}%</td>
                    <td class="{pnl_class}">{metrics['total_profit']:.2f}</td>
                    <td>{metrics['total_trades']}</td>
                </tr>
                """
            
            # Generate trade rows
            trade_rows = ""
            for trade in self.metrics['recent_trades'][:10]:
                date = datetime.fromisoformat(trade.get('timestamp')).strftime('%Y-%m-%d %H:%M')
                pnl = trade.get('pnl', 0)
                pnl_class = "win" if pnl >= 0 else "loss"
                
                trade_rows += f"""
                <tr>
                    <td>{date}</td>
                    <td>{trade.get('type', '')}</td>
                    <td>{trade.get('symbol', '')}</td>
                    <td>{trade.get('price', '')}</td>
                    <td class="{pnl_class}">{pnl:.2f}</td>
                </tr>
                """
            
            # Format overall metrics
            profit_class = "win" if self.metrics['total_profit_loss'] >= 0 else "loss"
            
            # Fill the template
            report = html.format(
                date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                profit_class=profit_class,
                total_pnl=f"{self.metrics['total_profit_loss']:.2f}",
                win_rate=f"{self.metrics['win_rate']:.1f}",
                total_trades=self.metrics['total_trades'],
                profit_factor=f"{self.metrics['profit_factor']:.2f}",
                max_drawdown=f"{self.metrics['max_drawdown']:.2f} ({self.metrics['max_drawdown_pct']:.1f}%)",
                winning_trades=self.metrics['winning_trades'],
                losing_trades=self.metrics['losing_trades'],
                avg_win=f"{self.metrics['average_profit']:.2f}",
                avg_loss=f"{self.metrics['average_loss']:.2f}",
                largest_win=f"{self.metrics['largest_profit']:.2f}",
                largest_loss=f"{self.metrics['largest_loss']:.2f}",
                strategy_rows=strategy_rows,
                trade_rows=trade_rows
            )
            
            # Write to file
            with open(output_file, 'w') as f:
                f.write(report)
            
            logger.info(f"Performance report generated: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return False
    
    def plot_equity_curve(self, show=True, save_path=None):
        """
        Plot equity curve
        
        Args:
            show (bool): Whether to display the plot
            save_path (str): Path to save the plot image
            
        Returns:
            bool: Success/failure
        """
        try:
            dates, equity = self.get_equity_curve()
            
            if not dates:
                logger.warning("No data available to plot equity curve")
                return False
            
            plt.figure(figsize=(10, 6))
            plt.plot(dates, equity, 'b-', linewidth=2)
            plt.title('BROski Trading Equity Curve')
            plt.xlabel('Date')
            plt.ylabel('Cumulative P&L')
            plt.grid(True)
            
            if save_path:
                plt.savefig(save_path)
                logger.info(f"Equity curve saved to {save_path}")
            
            if show:
                plt.show()
            
            return True
            
        except Exception as e:
            logger.error(f"Error plotting equity curve: {str(e)}")
            return False
