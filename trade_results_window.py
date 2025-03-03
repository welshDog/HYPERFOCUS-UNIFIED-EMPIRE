import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import threading
import time

# Add path fixing for imports
import sys
import os
from pathlib import Path

# Ensure we can import from any directory
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



class TradeResultsWindow:
    """
    Creates a pop-up window to display trade results, profits, and performance metrics.
    Provides visual representations of trading performance with charts.
    """
    
    def __init__(self, root=None):
        """Initialize the trade results window"""
        self.trades_file = os.path.join("logs", "trade_history.json")
        
        # Create a new window if root is not provided
        self.standalone = root is None
        if self.standalone:
            self.root = tk.Tk()
            self.root.title("BROski Trade Results")
            self.root.geometry("900x700")
            self.root.configure(bg="#f0f0f0")
            # Set window icon if available
            try:
                self.root.iconbitmap("favicon.ico")
            except:
                pass
        else:
            self.root = tk.Toplevel(root)
            self.root.title("BROski Trade Results")
            self.root.geometry("900x700")
            self.root.configure(bg="#f0f0f0")
            self.root.transient(root)  # Set to be on top of the parent window
            self.root.grab_set()  # Make window modal
        
        # Load trade data
        self.trades = []
        self.load_trades()
        
        # Create UI
        self.create_widgets()
        
        # Set up auto-refresh mechanism
        self.auto_refresh_enabled = tk.BooleanVar(value=True)
        self.refresh_thread = None
        self.stop_refresh = False
        
        if self.auto_refresh_enabled.get():
            self.start_auto_refresh()
        
        if self.standalone:
            self.root.mainloop()
    
    def load_trades(self):
        """Load trade data from JSON file"""
        try:
            if os.path.exists(self.trades_file):
                with open(self.trades_file, 'r') as f:
                    self.trades = json.load(f)
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trade data: {str(e)}")
            return False
    
    def create_widgets(self):
        """Create all widgets for the window"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Summary tab
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary")
        
        # Trade History tab
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Trade History")
        
        # Performance Charts tab
        charts_frame = ttk.Frame(notebook)
        notebook.add(charts_frame, text="Charts")
        
        # Strategy Comparison tab
        strategy_frame = ttk.Frame(notebook)
        notebook.add(strategy_frame, text="Strategy Comparison")
        
        # Populate the tabs
        self.create_summary_tab(summary_frame)
        self.create_history_tab(history_frame)
        self.create_charts_tab(charts_frame)
        self.create_strategy_tab(strategy_frame)
        
        # Bottom frame with controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill="x", pady=10)
        
        # Auto-refresh checkbox
        auto_refresh_check = ttk.Checkbutton(
            controls_frame, 
            text="Auto-refresh (30s)",
            variable=self.auto_refresh_enabled,
            command=self.toggle_auto_refresh
        )
        auto_refresh_check.pack(side="left", padx=10)
        
        # Refresh button
        refresh_btn = ttk.Button(
            controls_frame,
            text="Refresh Now",
            command=self.refresh_data
        )
        refresh_btn.pack(side="left", padx=10)
        
        # Export button
        export_btn = ttk.Button(
            controls_frame,
            text="Export Data",
            command=self.export_data
        )
        export_btn.pack(side="left", padx=10)
        
        # Close button
        close_btn = ttk.Button(
            controls_frame,
            text="Close",
            command=self.close_window
        )
        close_btn.pack(side="right", padx=10)
    
    def create_summary_tab(self, parent):
        """Create the summary tab with overall performance metrics"""
        # Top frame with overall performance
        top_frame = ttk.LabelFrame(parent, text="Overall Performance")
        top_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Calculate metrics
        metrics = self.calculate_performance_metrics()
        
        # Create 2x3 grid for metrics
        for i in range(2):
            top_frame.columnconfigure(i, weight=1)
        
        # Overall metrics - left side
        ttk.Label(top_frame, text="Total Trades:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(top_frame, text=f"{metrics['total_trades']}").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        ttk.Label(top_frame, text="Profitable Trades:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(top_frame, text=f"{metrics['profitable_trades']} ({metrics['win_rate']:.1f}%)").grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        ttk.Label(top_frame, text="Losing Trades:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(top_frame, text=f"{metrics['losing_trades']}").grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Overall metrics - right side
        ttk.Label(top_frame, text="Total Profit/Loss:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        profit_color = "green" if metrics['total_pnl'] >= 0 else "red"
        profit_label = ttk.Label(top_frame, text=f"{metrics['total_pnl']:.2f} USDT")
        profit_label.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        profit_label.configure(foreground=profit_color)
        
        ttk.Label(top_frame, text="Average Profit per Trade:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        avg_profit_color = "green" if metrics['avg_profit_per_trade'] >= 0 else "red"
        avg_profit_label = ttk.Label(top_frame, text=f"{metrics['avg_profit_per_trade']:.2f} USDT")
        avg_profit_label.grid(row=1, column=3, sticky="w", padx=10, pady=5)
        avg_profit_label.configure(foreground=avg_profit_color)
        
        ttk.Label(top_frame, text="Most Active Strategy:").grid(row=2, column=2, sticky="w", padx=10, pady=5)
        ttk.Label(top_frame, text=f"{metrics['most_active_strategy']}").grid(row=2, column=3, sticky="w", padx=10, pady=5)
        
        # Middle frame with profit metrics
        middle_frame = ttk.LabelFrame(parent, text="Profit Metrics")
        middle_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Create 2x2 grid for profit metrics
        for i in range(2):
            middle_frame.columnconfigure(i, weight=1)
        
        ttk.Label(middle_frame, text="Largest Win:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        largest_win_label = ttk.Label(middle_frame, text=f"{metrics['largest_win']:.2f} USDT")
        largest_win_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        largest_win_label.configure(foreground="green")
        
        ttk.Label(middle_frame, text="Largest Loss:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        largest_loss_label = ttk.Label(middle_frame, text=f"{metrics['largest_loss']:.2f} USDT")
        largest_loss_label.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        largest_loss_label.configure(foreground="red")
        
        ttk.Label(middle_frame, text="Average Win:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        avg_win_label = ttk.Label(middle_frame, text=f"{metrics['avg_win']:.2f} USDT")
        avg_win_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        avg_win_label.configure(foreground="green")
        
        ttk.Label(middle_frame, text="Average Loss:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        avg_loss_label = ttk.Label(middle_frame, text=f"{metrics['avg_loss']:.2f} USDT")
        avg_loss_label.grid(row=1, column=3, sticky="w", padx=10, pady=5)
        avg_loss_label.configure(foreground="red")
        
        # Bottom frame with recent activity
        bottom_frame = ttk.LabelFrame(parent, text="Recent Trading Activity")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Recent trades table
        columns = ("Date", "Type", "Symbol", "Price", "Amount", "P&L")
        recent_trades_tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        
        # Define column headings
        for col in columns:
            recent_trades_tree.heading(col, text=col)
            recent_trades_tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=recent_trades_tree.yview)
        recent_trades_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        recent_trades_tree.pack(side="left", fill="both", expand=True)
        
        # Add recent trades data
        closed_trades = [t for t in self.trades if t.get('status') == 'closed']
        recent_trades = sorted(closed_trades, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
        
        for trade in recent_trades:
            date_str = datetime.fromtimestamp(trade.get('timestamp', 0) / 1000).strftime('%Y-%m-%d %H:%M')
            pnl = trade.get('pnl', 0)
            pnl_str = f"{pnl:.2f}" if pnl != 0 else "-"
            
            values = (
                date_str,
                trade.get('type', ''),
                trade.get('symbol', ''),
                f"{trade.get('price', 0):.4f}",
                trade.get('amount', 0),
                pnl_str
            )
            
            # Use different colors for profit/loss
            if pnl > 0:
                recent_trades_tree.insert('', tk.END, values=values, tags=('profit',))
            elif pnl < 0:
                recent_trades_tree.insert('', tk.END, values=values, tags=('loss',))
            else:
                recent_trades_tree.insert('', tk.END, values=values)
        
        # Configure tag colors
        recent_trades_tree.tag_configure('profit', background='#e6ffe6')  # Light green
        recent_trades_tree.tag_configure('loss', background='#ffe6e6')    # Light red
    
    def create_history_tab(self, parent):
        """Create the trade history tab with detailed trade list"""
        # Create frame for controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Filter controls
        ttk.Label(controls_frame, text="Filter:").pack(side="left", padx=5)
        
        filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(controls_frame, textvariable=filter_var, width=15)
        filter_combo['values'] = ("All", "Profitable", "Loss", "Buy", "Sell")
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_history(filter_var.get(), history_tree))
        
        # Search field
        ttk.Label(controls_frame, text="Search:").pack(side="left", padx=5, pady=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(controls_frame, textvariable=search_var, width=20)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda e: self.search_history(search_var.get(), history_tree))
        
        # Trade history table
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("Date/Time", "Type", "Symbol", "Price", "Amount", "Value", "Status", "P&L", "Strategy")
        history_tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Define column headings and widths
        widths = {
            "Date/Time": 150, "Type": 80, "Symbol": 100, "Price": 100, 
            "Amount": 80, "Value": 100, "Status": 80, "P&L": 100, "Strategy": 150
        }
        
        for col in columns:
            history_tree.heading(col, text=col, command=lambda c=col: self.sort_history_column(history_tree, c, False))
            history_tree.column(col, width=widths.get(col, 100), anchor="center")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=history_tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=history_tree.xview)
        history_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        history_tree.pack(side="left", fill="both", expand=True)
        
        # Populate trade history
        self.update_trade_history(history_tree)
    
    def update_trade_history(self, tree):
        """Update trade history table"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Add all trades
        for trade in self.trades:
            # Format data
            timestamp = trade.get('timestamp', 0)
            date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "-"
            price = trade.get('price', 0)
            amount = trade.get('amount', 0)
            value = price * amount if price and amount else 0
            pnl = trade.get('pnl', 0)
            
            values = (
                date_str,
                trade.get('type', ''),
                trade.get('symbol', ''),
                f"{price:.4f}",
                f"{amount:.4f}",
                f"{value:.2f}",
                trade.get('status', ''),
                f"{pnl:.2f}" if pnl else "-",
                trade.get('strategy', '-')
            )
            
            # Use different colors for profit/loss
            if pnl > 0:
                tree.insert('', tk.END, values=values, tags=('profit',))
            elif pnl < 0:
                tree.insert('', tk.END, values=values, tags=('loss',))
            else:
                tree.insert('', tk.END, values=values)
        
        # Configure tag colors
        tree.tag_configure('profit', background='#e6ffe6')  # Light green
        tree.tag_configure('loss', background='#ffe6e6')    # Light red
    
    def create_charts_tab(self, parent):
        """Create charts tab with performance visualizations"""
        # Main frame with tabs for different charts
        charts_notebook = ttk.Notebook(parent)
        charts_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs for different chart types
        equity_frame = ttk.Frame(charts_notebook)
        charts_notebook.add(equity_frame, text="Equity Curve")
        
        pnl_frame = ttk.Frame(charts_notebook)
        charts_notebook.add(pnl_frame, text="Profit/Loss")
        
        win_loss_frame = ttk.Frame(charts_notebook)
        charts_notebook.add(win_loss_frame, text="Win/Loss")
        
        # Create charts
        self.create_equity_curve(equity_frame)
        self.create_pnl_distribution(pnl_frame)
        self.create_win_loss_chart(win_loss_frame)
    
    def create_equity_curve(self, parent):
        """Create equity curve chart"""
        # Create a figure
        fig = plt.Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Calculate equity curve data
        closed_trades = sorted([t for t in self.trades if t.get('status') == 'closed'], 
                              key=lambda x: x.get('timestamp', 0))
        
        dates = []
        equity = [0]  # Start with 0
        
        for trade in closed_trades:
            timestamp = trade.get('timestamp', 0)
            if timestamp:
                date = datetime.fromtimestamp(timestamp / 1000)
                dates.append(date)
                
                # Calculate running balance
                pnl = trade.get('pnl', 0)
                equity.append(equity[-1] + pnl)
        
        # Skip the first zero value for plotting
        if dates:  # Only plot if we have data
            ax.plot(dates, equity[1:], 'b-', linewidth=2)
            ax.set_title('Equity Curve')
            ax.set_xlabel('Date')
            ax.set_ylabel('Cumulative Profit/Loss (USDT)')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Color the background based on if we're profitable
            if equity[-1] > 0:
                ax.axhspan(0, max(equity), alpha=0.1, color='green')
            else:
                ax.axhspan(min(equity), 0, alpha=0.1, color='red')
                
            fig.tight_layout()
        else:
            # No data message
            ax.text(0.5, 0.5, "No closed trades data available", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12)
            
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_pnl_distribution(self, parent):
        """Create profit/loss distribution histogram"""
        # Create a figure
        fig = plt.Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Get P&L values from closed trades
        pnl_values = [t.get('pnl', 0) for t in self.trades if t.get('status') == 'closed' and t.get('pnl') is not None]
        
        if pnl_values:  # Only plot if we have data
            # Create histogram
            bins = min(20, max(5, len(pnl_values) // 5))  # Adjust bin count based on data size
            n, bins, patches = ax.hist(pnl_values, bins=bins, alpha=0.7)
            
            # Color bars based on profit/loss
            for i, p in enumerate(patches):
                if bins[i] < 0:
                    p.set_facecolor('red')
                else:
                    p.set_facecolor('green')
            
            ax.set_title('Profit/Loss Distribution')
            ax.set_xlabel('Profit/Loss (USDT)')
            ax.set_ylabel('Frequency')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Add a vertical line at zero
            ax.axvline(0, color='k', linestyle='--', alpha=0.7)
            
            # Add annotations for mean and median
            mean_pnl = np.mean(pnl_values)
            median_pnl = np.median(pnl_values)
            
            ax.axvline(mean_pnl, color='blue', linestyle='-', label=f'Mean: {mean_pnl:.2f}')
            ax.axvline(median_pnl, color='orange', linestyle='-', label=f'Median: {median_pnl:.2f}')
            
            ax.legend()
            fig.tight_layout()
        else:
            # No data message
            ax.text(0.5, 0.5, "No profit/loss data available", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12)
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_win_loss_chart(self, parent):
        """Create win/loss ratio chart"""
        # Create a figure
        fig = plt.Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Calculate win/loss count
        closed_trades = [t for t in self.trades if t.get('status') == 'closed']
        winning_trades = len([t for t in closed_trades if t.get('pnl', 0) > 0])
        losing_trades = len([t for t in closed_trades if t.get('pnl', 0) < 0])
        break_even_trades = len([t for t in closed_trades if t.get('pnl', 0) == 0])
        
        if closed_trades:  # Only plot if we have data
            # Data for pie chart
            labels = ['Winning', 'Losing', 'Break Even']
            sizes = [winning_trades, losing_trades, break_even_trades]
            colors = ['green', 'red', 'gray']
            explode = (0.1, 0, 0)  # Explode the winning slice
            
            # Only include non-zero values
            plot_labels = [label for label, size in zip(labels, sizes) if size > 0]
            plot_sizes = [size for size in sizes if size > 0]
            plot_colors = [color for color, size in zip(colors, sizes) if size > 0]
            plot_explode = [ex for ex, size in zip(explode, sizes) if size > 0]
            
            if plot_sizes:  # Make sure we still have data after filtering zeros
                # Create pie chart
                ax.pie(plot_sizes, explode=plot_explode, labels=plot_labels, colors=plot_colors,
                      autopct='%1.1f%%', shadow=True, startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
                
                ax.set_title('Win/Loss Distribution')
                
                # Add text with absolute numbers
                fig.text(0.5, 0.05, f"Total Trades: {len(closed_trades)} | "
                        f"Winning: {winning_trades} | Losing: {losing_trades} | "
                        f"Break Even: {break_even_trades}", 
                        ha='center')
            else:
                ax.text(0.5, 0.5, "No win/loss data available", 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12)
        else:
            # No data message
            ax.text(0.5, 0.5, "No closed trades data available", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12)
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_strategy_tab(self, parent):
        """Create strategy comparison tab"""
        # Create a frame for the strategy performance table
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Strategy performance table
        columns = ("Strategy", "Trades", "Win Rate", "Profit/Loss", "Avg P&L", "Best Trade", "Worst Trade")
        strategy_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Define column headings
        for col in columns:
            strategy_tree.heading(col, text=col)
            strategy_tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=strategy_tree.yview)
        strategy_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        strategy_tree.pack(side="left", fill="both", expand=True)
        
        # Calculate strategy performance
        strategy_stats = self.calculate_strategy_performance()
        
        # Add strategy data
        for strategy, stats in strategy_stats.items():
            pnl_color = 'profit' if stats['total_pnl'] >= 0 else 'loss'
            
            values = (
                strategy,
                stats['total_trades'],
                f"{stats['win_rate']:.1f}%",
                f"{stats['total_pnl']:.2f}",
                f"{stats['avg_pnl']:.2f}",
                f"{stats['best_trade']:.2f}",
                f"{stats['worst_trade']:.2f}"
            )
            
            strategy_tree.insert('', tk.END, values=values, tags=(pnl_color,))
        
        # Configure tag colors
        strategy_tree.tag_configure('profit', background='#e6ffe6')  # Light green
        strategy_tree.tag_configure('loss', background='#ffe6e6')    # Light red
        
        # Create chart comparing strategy performance
        chart_frame = ttk.Frame(parent)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create visualization
        self.create_strategy_comparison_chart(chart_frame, strategy_stats)
    
    def create_strategy_comparison_chart(self, parent, strategy_stats):
        """Create bar chart comparing strategy performance"""
        # Create a figure
        fig = plt.Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if strategy_stats:  # Only plot if we have data
            # Extract data for plotting
            strategies = list(strategy_stats.keys())
            win_rates = [stats['win_rate'] for stats in strategy_stats.values()]
            pnl_values = [stats['total_pnl'] for stats in strategy_stats.values()]
            
            # Bar positions
            x = np.arange(len(strategies))
            width = 0.35
            
            # Create bars
            bars1 = ax.bar(x - width/2, win_rates, width, label='Win Rate (%)', color='skyblue')
            bars2 = ax.bar(x + width/2, pnl_values, width, label='Total P&L (USDT)', color='lightgreen')
            
            # Add some text for labels, title and axes ticks
            ax.set_title('Strategy Performance Comparison')
            ax.set_xticks(x)
            ax.set_xticklabels(strategies)
            ax.legend()
            
            # Label bars with values
            self.autolabel(ax, bars1, format_str="{:.1f}%")
            self.autolabel(ax, bars2, format_str="{:.2f}")
            
            # Color P&L bars based on positive/negative
            for i, bar in enumerate(bars2):
                if pnl_values[i] < 0:
                    bar.set_color('salmon')
            
            fig.tight_layout()
        else:
            # No data message
            ax.text(0.5, 0.5, "No strategy performance data available", 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12)
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def autolabel(self, ax, bars, format_str="{:.2f}"):
        """Add labels to the top of the bars in a bar chart"""
        for bar in bars:
            height = bar.get_height()
            ax.annotate(format_str.format(height),
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom',
                     fontsize=8)

    def calculate_performance_metrics(self):
        """Calculate and return overall performance metrics"""
        metrics = {
            'total_trades': 0,
            'profitable_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_profit_per_trade': 0,
            'largest_win': 0,
            'largest_loss': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'most_active_strategy': 'None'
        }
        
        # Get closed trades
        closed_trades = [t for t in self.trades if t.get('status') == 'closed']
        
        if not closed_trades:
            return metrics
        
        # Basic counts
        metrics['total_trades'] = len(closed_trades)
        
        # Profit/loss metrics
        winning_trades = [t for t in closed_trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in closed_trades if t.get('pnl', 0) < 0]
        
        metrics['profitable_trades'] = len(winning_trades)
        metrics['losing_trades'] = len(losing_trades)
        
        # Win rate
        if metrics['total_trades'] > 0:
            metrics['win_rate'] = (metrics['profitable_trades'] / metrics['total_trades']) * 100
        
        # Total P&L
        metrics['total_pnl'] = sum(t.get('pnl', 0) for t in closed_trades)
        
        # Average P&L per trade
        if metrics['total_trades'] > 0:
            metrics['avg_profit_per_trade'] = metrics['total_pnl'] / metrics['total_trades']
        
        # Largest win/loss & average win/loss
        if winning_trades:
            metrics['largest_win'] = max(t.get('pnl', 0) for t in winning_trades)
            metrics['avg_win'] = sum(t.get('pnl', 0) for t in winning_trades) / len(winning_trades)
            
        if losing_trades:
            metrics['largest_loss'] = min(t.get('pnl', 0) for t in losing_trades)
            metrics['avg_loss'] = sum(t.get('pnl', 0) for t in losing_trades) / len(losing_trades)
            
        # Most active strategy
        strategy_counts = {}
        for trade in closed_trades:
            strategy = trade.get('strategy', 'unknown')
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            
        if strategy_counts:
            metrics['most_active_strategy'] = max(strategy_counts, key=strategy_counts.get)
            
        return metrics
    
    def calculate_strategy_performance(self):
        """Calculate performance metrics by strategy"""
        strategy_stats = {}
        
        # Get all closed trades
        closed_trades = [t for t in self.trades if t.get('status') == 'closed']
        
        # Group trades by strategy
        strategy_trades = {}
        for trade in closed_trades:
            strategy = trade.get('strategy', 'unknown')
            if strategy not in strategy_trades:
                strategy_trades[strategy] = []
            strategy_trades[strategy].append(trade)
            
        # Calculate metrics for each strategy
        for strategy, trades in strategy_trades.items():
            winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
            losing_trades = [t for t in trades if t.get('pnl', 0) < 0]
            
            # Skip if no trades for this strategy
            if not trades:
                continue
                
            total_pnl = sum(t.get('pnl', 0) for t in trades)
            win_rate = (len(winning_trades) / len(trades)) * 100 if trades else 0
            
            best_trade = max(trades, key=lambda x: x.get('pnl', 0)).get('pnl', 0) if trades else 0
            worst_trade = min(trades, key=lambda x: x.get('pnl', 0)).get('pnl', 0) if trades else 0
            
            strategy_stats[strategy] = {
                'total_trades': len(trades),
                'win_rate': win_rate,
                'total_pnl': total_pnl,
                'avg_pnl': total_pnl / len(trades) if trades else 0,
                'best_trade': best_trade,
                'worst_trade': worst_trade
            }
            
        return strategy_stats
    
    def filter_history(self, filter_type, tree):
        """Filter trade history by type"""
        # Clear the tree
        for item in tree.get_children():
            tree.delete(item)
            
        filtered_trades = []
        
        # Apply filter
        if filter_type == "All":
            filtered_trades = self.trades
        elif filter_type == "Profitable":
            filtered_trades = [t for t in self.trades if t.get('pnl', 0) > 0]
        elif filter_type == "Loss":
            filtered_trades = [t for t in self.trades if t.get('pnl', 0) < 0]
        elif filter_type == "Buy":
            filtered_trades = [t for t in self.trades if t.get('type', '').lower() == 'buy']
        elif filter_type == "Sell":
            filtered_trades = [t for t in self.trades if t.get('type', '').lower() == 'sell']
            
        # Add filtered trades to the tree
        for trade in filtered_trades:
            # Format data
            timestamp = trade.get('timestamp', 0)
            date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "-"
            price = trade.get('price', 0)
            amount = trade.get('amount', 0)
            value = price * amount if price and amount else 0
            pnl = trade.get('pnl', 0)
            
            values = (
                date_str,
                trade.get('type', ''),
                trade.get('symbol', ''),
                f"{price:.4f}",
                f"{amount:.4f}",
                f"{value:.2f}",
                trade.get('status', ''),
                f"{pnl:.2f}" if pnl else "-",
                trade.get('strategy', '-')
            )
            
            # Use different colors for profit/loss
            if pnl > 0:
                tree.insert('', tk.END, values=values, tags=('profit',))
            elif pnl < 0:
                tree.insert('', tk.END, values=values, tags=('loss',))
            else:
                tree.insert('', tk.END, values=values)
    
    def search_history(self, search_term, tree):
        """Search trade history for a term"""
        if not search_term:
            self.update_trade_history(tree)
            return
            
        # Clear the tree
        for item in tree.get_children():
            tree.delete(item)
            
        # Search all fields
        search_term = search_term.lower()
        for trade in self.trades:
            # Check if search term is in any string field
            found = False
            for key, value in trade.items():
                if isinstance(value, str) and search_term in value.lower():
                    found = True
                    break
                    
            if found:
                # Format data
                timestamp = trade.get('timestamp', 0)
                date_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "-"
                price = trade.get('price', 0)
                amount = trade.get('amount', 0)
                value = price * amount if price and amount else 0
                pnl = trade.get('pnl', 0)
                
                values = (
                    date_str,
                    trade.get('type', ''),
                    trade.get('symbol', ''),
                    f"{price:.4f}",
                    f"{amount:.4f}",
                    f"{value:.2f}",
                    trade.get('status', ''),
                    f"{pnl:.2f}" if pnl else "-",
                    trade.get('strategy', '-')
                )
                
                # Use different colors for profit/loss
                if pnl > 0:
                    tree.insert('', tk.END, values=values, tags=('profit',))
                elif pnl < 0:
                    tree.insert('', tk.END, values=values, tags=('loss',))
                else:
                    tree.insert('', tk.END, values=values)
    
    def sort_history_column(self, tree, column, reverse):
        """Sort treeview by column"""
        # Get column index
        column_idx = tree["columns"].index(column)
        
        # Get all items with values
        items = [(tree.set(k, column), k) for k in tree.get_children('')]
        
        # Try to convert to numeric for proper sorting
        try:
            items.sort(key=lambda x: float(x[0].replace(',', '')), reverse=reverse)
        except:
            items.sort(reverse=reverse)
            
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(items):
            tree.move(k, '', index)
            
        # Switch sorting direction next time
        tree.heading(column, command=lambda: self.sort_history_column(tree, column, not reverse))
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        if self.auto_refresh_enabled.get():
            self.start_auto_refresh()
        else:
            self.stop_refresh = True
            if self.refresh_thread:
                self.refresh_thread.join(0.1)
    
    def start_auto_refresh(self):
        """Start auto-refresh thread"""
        if self.refresh_thread and self.refresh_thread.is_alive():
            return
            
        self.stop_refresh = False
        self.refresh_thread = threading.Thread(target=self._auto_refresh_task)
        self.refresh_thread.daemon = True
        self.refresh_thread.start()
    
    def _auto_refresh_task(self):
        """Background task to refresh data periodically"""
        while not self.stop_refresh:
            # Sleep for 30 seconds
            for _ in range(30):
                if self.stop_refresh:
                    break
                time.sleep(1)
                
            if not self.stop_refresh:
                # Use after() to schedule GUI updates on the main thread
                self.root.after(0, self.refresh_data)
    
    def refresh_data(self):
        """Refresh all data"""
        # Reload trade data
        self.load_trades()
        
        # Refresh all tabs
        # We need to get references to all trees and charts
        # For simplicity, we'll just recreate all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.create_widgets()
    
    def export_data(self):
        """Export trade data to CSV"""
        try:
            import pandas as pd
            
            if not self.trades:
                messagebox.showinfo("Export", "No trade data to export")
                return
                
            # Convert to DataFrame
            df = pd.DataFrame(self.trades)
            
            # Format timestamp
            if 'timestamp' in df.columns:
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                
            # Ask for save location
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Trade Data"
            )
            
            if not file_path:
                return
                
            # Save to CSV
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export", f"Trade data exported to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def close_window(self):
        """Close the window"""
        self.stop_refresh = True
        if self.refresh_thread:
            self.refresh_thread.join(0.1)
            
        if self.standalone:
            self.root.quit()
        else:
            self.root.destroy()

# Allow the window to be run directly
if __name__ == "__main__":
    # Create the window
    TradeResultsWindow()
