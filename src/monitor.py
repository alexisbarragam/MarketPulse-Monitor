# MarketPulse.Monitor v3.3.2
# A real-time market monitoring tool with a polished UI and dynamic annotations.

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Dict
from datetime import datetime, timedelta

class MarketMonitor:
    """
    Fetches, displays, and updates real-time financial data plots with a
    dynamic info labels.
    """

    def __init__(self, tickers: Dict[str, str], interval_seconds: int = 60, fetch_period: str = "1d"):
        self.tickers = tickers
        self.data_update_interval = timedelta(seconds=interval_seconds)
        self.yf_fetch_interval = self._get_valid_yf_interval(interval_seconds)
        self.period = fetch_period
        self.data_frames: Dict[str, pd.DataFrame] = {name: pd.DataFrame() for name in tickers.keys()}
        self.ani = None
        self.last_fetch_time = datetime.min

        # --- VISUAL STYLING ---
        plt.style.use('dark_background')
        self.fig, self.axes = plt.subplots(
            len(tickers), 1, figsize=(16, 6 * len(tickers)), sharex=True
        )
        self.fig.patch.set_facecolor('#2d2d2d')
        if len(tickers) == 1:
            self.axes = [self.axes]

        self.clock_text = self.fig.text(0.95, 0.97, '', transform=self.fig.transFigure,
                                        fontsize=12, color='white', ha='right')

        self.colors = ['#87CEEB', '#FFD700', '#98FB98'] # Light Blue, Gold, Light Green

    def _get_valid_yf_interval(self, seconds: int) -> str:
        """Helper to select a valid yfinance interval."""
        if seconds < 60: return "1m"
        if seconds < 300: return "5m"
        return "15m"

    def _fetch_data(self) -> None:
        """Fetches the latest data for all tickers."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching market data...")
        for name, symbol in self.tickers.items():
            try:
                new_data = yf.download(
                    tickers=symbol, period=self.period, interval=self.yf_fetch_interval, progress=False
                )
                if not new_data.empty:
                    self.data_frames[name] = new_data
            except Exception as e:
                print(f"Could not fetch data for {name}: {e}")
        print("Data fetch complete.")

    def _redraw_plots(self):
        """Redraws all the subplots with current data."""
        for i, (ax, name) in enumerate(zip(self.axes, self.tickers.keys())):
            ax.clear()
            df = self.data_frames[name]
            color = self.colors[i % len(self.colors)]

            if not df.empty:
                y_values = df['Close'].values.flatten()
                last_price = float(df['Close'].iloc[-1])
                last_time = df.index[-1]
                label_text = f"Value: {last_price:,.2f}"
                
                # Plot the main line with the label for the legend
                ax.plot(df.index, y_values, color=color, label=label_text)

                # --- REFINEMENTS ---
                ax.set_facecolor('#2d2d2d')
                ax.set_title(name, fontsize=16, color='white')
                ax.set_ylabel("Value / Points", color='lightgray')

                # Dynamic Value Label on the plot line itself
                ax.text(last_time, last_price, f' {last_price:,.2f}',
                        color=color, va='center', ha='left', fontsize=11, weight='bold')

                # Dynamic Y-Axis Limits for stability
                day_low = float(df['Close'].min())
                day_high = float(df['Close'].max())
                padding = (day_high - day_low) * 0.1
                ax.set_ylim(day_low - padding, day_high + padding)

                # Professional Watermark
                ax.text(0.5, 0.5, name, transform=ax.transAxes,
                        fontsize=40, color='gray', alpha=0.15,
                        ha='center', va='center')
                
                # --- NEW: re-add the styled legend box ---
                legend = ax.legend(loc='upper left', frameon=True, facecolor='black', edgecolor='white')
                plt.setp(legend.get_texts(), color='white')

                for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
                for spine in ['left', 'bottom']: ax.spines[spine].set_color('gray')
                
                ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
                ax.tick_params(axis='x', colors='lightgray')
                ax.tick_params(axis='y', colors='lightgray')

        self.axes[-1].set_xlabel("Time (UTC)", color='lightgray')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    def _update_frame(self, frame: int) -> None:
        """
        Called by FuncAnimation every second. Updates clock and triggers data fetch.
        """
        current_time = datetime.now()
        
        self.clock_text.set_text(current_time.strftime('%Y-%m-%d %I:%M:%S %p'))

        if current_time - self.last_fetch_time > self.data_update_interval:
            self.last_fetch_time = current_time
            self._fetch_data()
            self._redraw_plots()

    def run(self) -> None:
        """Starts the real-time plot animation."""
        self.fig.suptitle('MarketPulse.Monitor', fontsize=20, weight='bold', color='white')
        self.ani = animation.FuncAnimation(self.fig, self._update_frame, interval=1000)
        plt.show()

if __name__ == "__main__":
    assets_to_track: Dict[str, str] = {
        "Ibovespa": "^BVSP",
        "Euro (EUR/BRL)": "EURBRL=X",
        "Dollar (USD/BRL)": "BRL=X"
    }
    
    monitor = MarketMonitor(tickers=assets_to_track, interval_seconds=60)
    monitor.run()