# MarketPulse.Monitor v4.0.0
# Real-time market monitor
# Final portfolio build

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Dict
from datetime import datetime, timedelta

class MarketMonitor:
    """
    Fetches, displays, and updates real-time financial data plots with a
    custom UI, optimized for stability.
    """

    def __init__(self, tickers: Dict[str, str], interval_seconds: int = 60, fetch_period: str = "1d"):
        self.tickers = tickers
        self.data_update_interval = timedelta(seconds=interval_seconds)
        self.yf_fetch_interval = self._get_valid_yf_interval(interval_seconds)
        self.period = fetch_period
        self.data_frames: Dict[str, pd.DataFrame] = {name: pd.DataFrame() for name in tickers.keys()}
        self.last_fetch_time = datetime.min
        self.y_limits_set = False

        # Figure and style setup
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 9))
        
        gs = self.fig.add_gridspec(len(tickers) + 1, 1, height_ratios=[10] * len(tickers) + [1])
        
        self.axes = [self.fig.add_subplot(gs[i, 0]) for i in range(len(tickers))]
        self.ticker_ax = self.fig.add_subplot(gs[len(tickers), 0])
        self.fig.patch.set_facecolor('#2d2d2d')
        
        # Fix subplot margins to prevent autoscaling shifts
        self.fig.subplots_adjust(
            left=0.06, right=0.94, bottom=0.08, top=0.92, hspace=0.45
        )
        
        # Ticker tape overlay setup
        self.ticker_text_obj = self.ticker_ax.text(1.5, 0.5, 'Fetching initial data...', va='center', ha='left', fontsize=12, color='white', transform=self.ticker_ax.transAxes)
        self.ticker_ax.axis('off')
        self.ticker_state = 'scrolling'
        self.ticker_wait_start_time = None
        self.ticker_wait_duration = timedelta(seconds=20)

        self.colors = ['#91bec0', '#a591c5', '#f36e53'] # Color order: Ibovespa, Euro, Dollar

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
                new_data = yf.download(tickers=symbol, period=self.period, interval=self.yf_fetch_interval, progress=False)
                if not new_data.empty:
                    self.data_frames[name] = new_data
            except Exception as e:
                print(f"Could not fetch data for {name}: {e}")
        print("Data fetch complete.")

    def _update_frame(self, frame: int) -> None:
        """
        This function is called by FuncAnimation at each update interval.
        It redraws the plots with the latest data.
        """
        current_time = datetime.now()
        
        # Ticker-tape state machine
        if self.ticker_state == 'scrolling':
            current_pos = self.ticker_text_obj.get_position()[0]
            new_pos = current_pos - 0.005
            self.ticker_text_obj.set_position((new_pos, 0.5))
            if self.ticker_text_obj.get_window_extent().x1 < 0:
                self.ticker_state = 'waiting'
                self.ticker_wait_start_time = current_time
                self.ticker_text_obj.set_visible(False)
        
        elif self.ticker_state == 'waiting':
            if current_time - self.ticker_wait_start_time > self.ticker_wait_duration:
                self.ticker_state = 'scrolling'
                self.ticker_text_obj.set_position((1.0, 0.5))
                self.ticker_text_obj.set_visible(True)

        # Throttle data fetches (lower rate than frame updates)
        if current_time - self.last_fetch_time > self.data_update_interval:
            self.last_fetch_time = current_time
            self._fetch_data()
            
            ticker_content_parts = [f"LAST UPDATE: {current_time.strftime('%I:%M:%S %p')}"]
            for name, df in self.data_frames.items():
                if not df.empty:
                    last_price = df['Close'].iloc[-1].item()
                    ticker_content_parts.append(f"{name.upper()}: {last_price:,.2f}")
            ticker_full_content = "      |      ".join(ticker_content_parts)
            self.ticker_text_obj.set_text("      " + ticker_full_content)
            
            # Re-render all subplots with the latest data
            for i, (ax, name) in enumerate(zip(self.axes, self.tickers.keys())):
                ax.clear()
                df = self.data_frames[name]
                color = self.colors[i % len(self.colors)]

                if not df.empty:
                    last_price = df['Close'].iloc[-1].item()
                    label_text = f"Value: {last_price:,.2f}"
                    
                    ax.plot(df.index, df['Close'], color=color, label=label_text)
                    ax.text(df.index[-1], last_price, f' {last_price:,.2f}', color=color, va='center', ha='left', fontsize=11, weight='bold')

                    if not self.y_limits_set:
                        day_low = float(df['Close'].min())
                        day_high = float(df['Close'].max())
                        padding = (day_high - day_low) * 0.1
                        ax.set_ylim(day_low - padding, day_high + padding)
                
                ax.set_facecolor('#2d2d2d')
                ax.set_title(name, fontsize=16, color='white')
                ax.set_ylabel("Value / Points", color='lightgray')
                ax.text(0.5, 0.5, name, transform=ax.transAxes, fontsize=40, color='gray', alpha=0.15, ha='center', va='center')
                legend = ax.legend(loc='upper left', frameon=True, facecolor='black', edgecolor='white')
                plt.setp(legend.get_texts(), color='white')
                for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
                for spine in ['left', 'bottom']: ax.spines[spine].set_color('gray')
                ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
                ax.tick_params(axis='y', colors='lightgray')

                # Minimalist UI tweaks
                # Hide X-axis datetime labels to keep the chart uncluttered
                ax.set_xticklabels([])
                ax.tick_params(axis='x', length=0) # Hide minor tick marks as well
            
            if not self.y_limits_set and any(not df.empty for df in self.data_frames.values()):
                self.y_limits_set = True
        
        self.fig.suptitle('MarketPulse.Monitor', fontsize=20, weight='bold', color='white')
        self.axes[-1].set_xlabel("Time (UTC)", color='lightgray')
        self.fig.canvas.draw_idle()

    def run(self) -> None:
        """Starts the real-time plot animation."""
        self.ani = animation.FuncAnimation(
            self.fig, self._update_frame, interval=40, blit=False
        )
        plt.show()

if __name__ == "__main__":
    assets_to_track: Dict[str, str] = {
        "Ibovespa": "^BVSP",
        "Euro (EUR/BRL)": "EURBRL=X",
        "Dollar (USD/BRL)": "BRL=X"
    }
    
    monitor = MarketMonitor(tickers=assets_to_track, interval_seconds=60)
    monitor.run()