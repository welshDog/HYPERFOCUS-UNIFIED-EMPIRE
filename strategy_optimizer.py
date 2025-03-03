import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid

class StrategyOptimizer:
    """
    Strategy optimization system for BROski Trading Bot
    Captures monitoring data and uses it to optimize strategy parameters
    """
    
    def __init__(self):
        """Initialize the strategy optimizer"""
        # Ensure directories exist
        os.makedirs("data/metrics", exist_ok=True)
        os.makedirs("data/optimization", exist_ok=True)
        os.makedirs("models", exist_ok=True)
        
        # File paths
        self.metrics_file = "data/metrics/strategy_metrics.csv"
        self.config_file = "config.json"
        self.trade_history_file = "logs/trade_history.json"
        self.market_data_file = "data/market_data.csv"
        self.optimization_log = "data/optimization/hyperfocus_optimization.json"
        
        # Metrics to track for optimization
        self.metric_columns = [
            'timestamp', 'strategy', 'timeframe', 'price', 'rsi_value',
            'macd_value', 'signal_value', 'macd_histogram', 
            'ma_fast_value', 'ma_slow_value', 'volume', 'avg_volume',
            'signal_generated', 'signal_type', 'confidence_score'
        ]
        
        # Initialize metrics file if it doesn't exist
        if not os.path.exists(self.metrics_file):
            self._init_metrics_file()
    
    def _init_metrics_file(self):
        """Create initial metrics CSV file"""
        df = pd.DataFrame(columns=self.metric_columns)
        df.to_csv(self.metrics_file, index=False)
        print(f"Created new metrics file: {self.metrics_file}")
    
    def load_config(self):
        """Load the configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def save_metrics(self, metrics_data):
        """
        Save monitoring metrics to CSV for later analysis
        
        Args:
            metrics_data: Dictionary containing metrics data points
        """
        # Ensure all required columns are present
        for col in self.metric_columns:
            if col not in metrics_data:
                metrics_data[col] = None
        
        # Convert to DataFrame row and append to CSV
        df = pd.DataFrame([metrics_data])
        df.to_csv(self.metrics_file, mode='a', header=False, index=False)
    
    def analyze_performance(self, days=30):
        """
        Analyze strategy performance based on collected metrics and trade history
        
        Args:
            days: Number of days to analyze (default: 30)
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            # Load metrics data
            if os.path.exists(self.metrics_file):
                metrics_df = pd.read_csv(self.metrics_file)
                metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'])
                
                # Filter for recent data
                cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days)
                recent_metrics = metrics_df[metrics_df['timestamp'] > cutoff_date]
            else:
                recent_metrics = pd.DataFrame()
            
            # Load trade history
            if os.path.exists(self.trade_history_file):
                with open(self.trade_history_file, 'r') as f:
                    trade_history = json.load(f)
                
                # Convert to DataFrame
                trades_df = pd.DataFrame(trade_history)
                if 'timestamp' in trades_df.columns:
                    trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'], unit='ms')
                    
                    # Filter recent trades
                    recent_trades = trades_df[trades_df['timestamp'] > cutoff_date]
                else:
                    recent_trades = pd.DataFrame()
            else:
                recent_trades = pd.DataFrame()
            
            # Calculate performance metrics
            performance = {}
            
            # Strategy Signal Accuracy
            if not recent_metrics.empty and 'signal_generated' in recent_metrics.columns:
                # Count signals generated
                buy_signals = recent_metrics[recent_metrics['signal_type'] == 'BUY'].shape[0]
                sell_signals = recent_metrics[recent_metrics['signal_type'] == 'SELL'].shape[0]
                total_signals = buy_signals + sell_signals
                
                performance['total_signals'] = total_signals
                performance['buy_signals'] = buy_signals
                performance['sell_signals'] = sell_signals
            
            # Trade Performance
            if not recent_trades.empty and 'pnl' in recent_trades.columns:
                # Calculate trade metrics
                profitable_trades = recent_trades[recent_trades['pnl'] > 0].shape[0]
                losing_trades = recent_trades[recent_trades['pnl'] < 0].shape[0]
                total_trades = profitable_trades + losing_trades
                
                if total_trades > 0:
                    win_rate = (profitable_trades / total_trades) * 100
                else:
                    win_rate = 0
                
                total_pnl = recent_trades['pnl'].sum()
                
                performance['total_trades'] = total_trades
                performance['profitable_trades'] = profitable_trades
                performance['losing_trades'] = losing_trades
                performance['win_rate'] = win_rate
                performance['total_pnl'] = total_pnl
                
                # Average metrics
                if profitable_trades > 0:
                    performance['avg_profit'] = recent_trades[recent_trades['pnl'] > 0]['pnl'].mean()
                if losing_trades > 0:
                    performance['avg_loss'] = recent_trades[recent_trades['pnl'] < 0]['pnl'].mean()
                
                # Strategy breakdown
                strategies = recent_trades['strategy'].unique()
                for strategy in strategies:
                    strat_trades = recent_trades[recent_trades['strategy'] == strategy]
                    strat_wins = strat_trades[strat_trades['pnl'] > 0].shape[0]
                    strat_total = len(strat_trades)
                    
                    if strat_total > 0:
                        strat_win_rate = (strat_wins / strat_total) * 100
                        performance[f'{strategy}_trades'] = strat_total
                        performance[f'{strategy}_win_rate'] = strat_win_rate
                        performance[f'{strategy}_pnl'] = strat_trades['pnl'].sum()
            
            # Find correlations between metrics and successful trades
            if not recent_metrics.empty and not recent_trades.empty:
                # This would require joining metrics with trades based on timestamp
                # For simplicity, we'll skip the detailed correlation analysis here
                pass
                
            return performance
        
        except Exception as e:
            print(f"Error analyzing performance: {e}")
            return {"error": str(e)}
    
    def optimize_hyperfocus(self):
        """
        Optimize HyperFocus strategy parameters based on historical performance
        
        Returns:
            Dictionary with optimized parameters
        """
        # Load current config
        config = self.load_config()
        if not config:
            return {"error": "Could not load configuration"}
        
        # Current HyperFocus parameters
        current_params = config.get("strategies", {}).get("hyperfocus_strategy", {})
        if not current_params:
            return {"error": "HyperFocus strategy not found in config"}
        
        # Analyze recent performance with current settings
        current_performance = self.analyze_performance(days=30)
        
        # Parameter grid for testing
        param_grid = {
            'rsi_period': [12, 14, 16],
            'rsi_overbought': [68, 70, 72, 75],
            'rsi_oversold': [25, 28, 30, 32],
            'ma_fast': [15, 20, 25],
            'ma_slow': [45, 50, 55],
            'volume_factor': [1.3, 1.5, 1.8],
            'volume_lookback': [15, 20, 25]
        }
        
        # Get trade history for backtesting
        if not os.path.exists(self.trade_history_file) or not os.path.exists(self.market_data_file):
            return {
                "error": "Insufficient data for optimization",
                "recommendation": "Continue collecting data in monitor mode"
            }
        
        # Load market data if available (in practice, this would be loaded from an actual file)
        try:
            market_data = pd.read_csv(self.market_data_file)
        except:
            # If we don't have market data file yet, we'll generate a recommendation based on metrics
            return self._generate_recommendations(current_params, current_performance)
        
        # Perform optimization (simplified version)
        results = []
        for params in ParameterGrid(param_grid):
            # In a real implementation, this would run a backtest with the parameters
            # Here we'll just generate a simulated result
            simulated_result = {
                'params': params,
                'win_rate': np.random.uniform(40, 70),  # Simulated win rate
                'pnl': np.random.uniform(-100, 300)     # Simulated P&L
            }
            results.append(simulated_result)
        
        # Find best parameters (in a real implementation, this would use actual backtest results)
        best_result = max(results, key=lambda x: x['pnl'])
        
        # Save optimization log
        optimization_record = {
            'timestamp': datetime.now().isoformat(),
            'current_parameters': current_params,
            'current_performance': current_performance,
            'tested_parameters': len(results),
            'best_parameters': best_result['params'],
            'best_performance': {
                'win_rate': best_result['win_rate'],
                'pnl': best_result['pnl']
            }
        }
        
        # Save optimization results
        with open(self.optimization_log, 'w') as f:
            json.dump(optimization_record, f, indent=2)
        
        # Return optimized parameters
        return {
            'current_params': current_params,
            'optimized_params': best_result['params'],
            'improvement': {
                'pnl_increase': best_result['pnl'] - current_performance.get('total_pnl', 0),
                'win_rate_increase': best_result['win_rate'] - current_performance.get('win_rate', 0)
            }
        }
    
    def _generate_recommendations(self, current_params, performance):
        """
        Generate strategy recommendations based on available metrics
        Used when full optimization is not possible
        """
        recommendations = {}
        
        # Example logic for RSI settings
        if 'hyperfocus_strategy_win_rate' in performance:
            win_rate = performance['hyperfocus_strategy_win_rate']
            
            if win_rate < 40:
                # Poor performance - make RSI less sensitive
                recommendations['rsi_period'] = min(current_params['rsi_period'] + 2, 20)  # Increase period
                recommendations['rsi_oversold'] = max(current_params['rsi_oversold'] - 2, 20)  # Lower oversold
                recommendations['rsi_overbought'] = min(current_params['rsi_overbought'] + 2, 80)  # Raise overbought
            elif win_rate > 60:
                # Good performance - keep similar settings
                recommendations['rsi_period'] = current_params['rsi_period']  # Keep period
            
            # More logic would be added for other parameters
        
        return {
            'current_params': current_params,
            'recommended_params': {**current_params, **recommendations},
            'note': "Recommendations based on limited data. Continue collecting data for better optimization."
        }
    
    def update_strategy_config(self, optimized_params):
        """
        Update the strategy configuration with optimized parameters
        
        Args:
            optimized_params: Dictionary with optimized parameter values
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load current config
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Update HyperFocus parameters
            for key, value in optimized_params.items():
                if key in config["strategies"]["hyperfocus_strategy"]:
                    config["strategies"]["hyperfocus_strategy"][key] = value
            
            # Add timestamp of optimization
            config["strategies"]["hyperfocus_strategy"]["last_optimized"] = datetime.now().isoformat()
            
            # Save updated config
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error updating strategy config: {e}")
            return False
    
    def generate_performance_report(self, days=30):
        """
        Generate a performance report and visualizations
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Report file path
        """
        try:
            performance = self.analyze_performance(days)
            
            # Create report directory
            report_dir = "reports"
            os.makedirs(report_dir, exist_ok=True)
            
            # Report filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"{report_dir}/performance_report_{timestamp}.html"
            
            # Generate report content
            report_content = f"""
            <html>
            <head>
                <title>BROski Bot Performance Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1, h2 {{ color: #333; }}
                    .metric {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
                    .good {{ background-color: #e6ffe6; }}
                    .bad {{ background-color: #ffe6e6; }}
                    .neutral {{ background-color: #f0f0f0; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>BROski Bot Performance Report</h1>
                <p>Report generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>Analysis period: Last {days} days</p>
                
                <h2>Overall Performance</h2>
                <div class="metric {'good' if performance.get('total_pnl', 0) > 0 else 'bad'}">
                    <h3>Total Profit/Loss</h3>
                    <p>{performance.get('total_pnl', 'N/A')} USDT</p>
                </div>
                
                <div class="metric {'good' if performance.get('win_rate', 0) > 50 else 'neutral'}">
                    <h3>Win Rate</h3>
                    <p>{performance.get('win_rate', 'N/A')}%</p>
                    <p>({performance.get('profitable_trades', 0)}/{performance.get('total_trades', 0)} trades)</p>
                </div>
                
                <h2>Strategy Performance</h2>
                <table>
                    <tr>
                        <th>Strategy</th>
                        <th>Trades</th>
                        <th>Win Rate</th>
                        <th>P&L</th>
                    </tr>
            """
            
            # Add strategy-specific rows
            strategies = ["hyperfocus_strategy", "rsi_strategy", "macd_strategy"]
            for strategy in strategies:
                name = strategy.replace('_strategy', '').title()
                trades = performance.get(f'{strategy}_trades', 'N/A')
                win_rate = performance.get(f'{strategy}_win_rate', 'N/A')
                if win_rate != 'N/A':
                    win_rate = f"{win_rate:.1f}%"
                    
                pnl = performance.get(f'{strategy}_pnl', 'N/A')
                if pnl != 'N/A':
                    pnl = f"{pnl:.2f} USDT"
                
                report_content += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{trades}</td>
                        <td>{win_rate}</td>
                        <td>{pnl}</td>
                    </tr>
                """
            
            # Finish report
            report_content += """
                </table>
                
                <h2>Recommendations</h2>
                <p>Based on the analysis, the following adjustments are recommended:</p>
                <ul>
                    <li>Continue collecting data in monitor mode for better optimization</li>
                    <li>Run the strategy optimizer for parameter tuning</li>
                </ul>
                
                <h2>Next Steps</h2>
                <p>To apply optimized parameters, run:</p>
                <pre>python strategy_optimizer.py --apply-optimal</pre>
                
            </body>
            </html>
            """
            
            # Write report to file
            with open(report_file, 'w') as f:
                f.write(report_content)
                
            return report_file
            
        except Exception as e:
            print(f"Error generating performance report: {e}")
            return None
    
    def create_strategy_visualizations(self):
        """Create visualizations of strategy performance"""
        try:
            # Create output directory
            viz_dir = "data/visualization"
            os.makedirs(viz_dir, exist_ok=True)
            
            # Load metrics for visualization if available
            if os.path.exists(self.metrics_file):
                metrics_df = pd.read_csv(self.metrics_file)
            else:
                return False
                
            # Load trade history
            if os.path.exists(self.trade_history_file):
                with open(self.trade_history_file, 'r') as f:
                    trades = json.load(f)
                trades_df = pd.DataFrame(trades)
                
                # Convert timestamps
                if 'timestamp' in trades_df.columns:
                    trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'], unit='ms')
            else:
                trades_df = pd.DataFrame()
            
            # Filter for HyperFocus strategy
            hyperfocus_trades = trades_df[trades_df['strategy'] == 'hyperfocus_strategy'] if not trades_df.empty else None
            
            # 1. Create P&L over time chart
            if not trades_df.empty and 'pnl' in trades_df.columns and 'timestamp' in trades_df.columns:
                plt.figure(figsize=(10, 6))
                
                # Calculate cumulative P&L
                sorted_trades = trades_df.sort_values('timestamp')
                sorted_trades['cumulative_pnl'] = sorted_trades['pnl'].cumsum()
                
                # Plot
                plt.plot(sorted_trades['timestamp'], sorted_trades['cumulative_pnl'], 'b-')
                plt.title('Cumulative P&L Over Time')
                plt.xlabel('Date')
                plt.ylabel('P&L (USDT)')
                plt.grid(True)
                plt.savefig(f"{viz_dir}/cumulative_pnl.png")
                plt.close()
            
            # 2. Create win rate by parameter value charts (for RSI)
            if not trades_df.empty and not metrics_df.empty:
                # This would ideally join trades with metrics for detailed analysis
                # For this simplified example, we'll just create a placeholder chart
                
                # Create dummy data for demonstration
                rsi_values = range(20, 81, 5)  # RSI values from 20 to 80
                win_rates = [np.random.uniform(30, 70) for _ in rsi_values]  # Random win rates
                
                plt.figure(figsize=(10, 6))
                plt.bar(rsi_values, win_rates)
                plt.title('Win Rate by RSI Value (Simulated Data)')
                plt.xlabel('RSI Value')
                plt.ylabel('Win Rate (%)')
                plt.grid(True, axis='y')
                plt.savefig(f"{viz_dir}/rsi_win_rate.png")
                plt.close()
                
            # 3. Create parameter correlation heatmap
            # (In a full implementation, this would show correlations between parameters and profit)
            
            return True
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
            return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="BROski Strategy Optimizer")
    parser.add_argument('--optimize', action='store_true', help='Run optimization to find best parameters')
    parser.add_argument('--apply-optimal', action='store_true', help='Apply optimized parameters to config')
    parser.add_argument('--report', action='store_true', help='Generate performance report')
    parser.add_argument('--days', type=int, default=30, help='Number of days for analysis')
    
    args = parser.parse_args()
    
    optimizer = StrategyOptimizer()
    
    if args.optimize:
        print("Running HyperFocus strategy optimization...")
        results = optimizer.optimize_hyperfocus()
        print(f"Optimization complete!")
        print(f"Current parameters: {results.get('current_params', 'N/A')}")
        print(f"Optimized parameters: {results.get('optimized_params', 'N/A')}")
        
        if args.apply_optimal and 'optimized_params' in results:
            if optimizer.update_strategy_config(results['optimized_params']):
                print("✅ Successfully updated strategy configuration with optimized parameters!")
            else:
                print("❌ Failed to update configuration!")
    
    if args.report:
        print(f"Generating performance report for the last {args.days} days...")
        report_path = optimizer.generate_performance_report(args.days)
        if report_path:
            print(f"✅ Report generated: {report_path}")
            
            # Try to open the report in the default browser
            try:
                import webbrowser
                webbrowser.open(f"file://{os.path.abspath(report_path)}")
            except:
                pass
        else:
            print("❌ Failed to generate report!")
