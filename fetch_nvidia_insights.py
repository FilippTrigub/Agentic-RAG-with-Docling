#!/usr/bin/env python3
"""
NVIDIA Insights Fetcher and Visualizer
Fetches NVIDIA stock data and generates comprehensive PDF visualization report
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import warnings

warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9


class NVIDIAInsightsFetcher:
    def __init__(self, ticker='NVDA', period='1y'):
        """Initialize with NVIDIA ticker and time period"""
        self.ticker = ticker
        self.period = period
        self.stock = None
        self.data = None
        self.info = None
        
    def fetch_data(self):
        """Fetch stock data from Yahoo Finance"""
        print(f"Fetching {self.ticker} data for period: {self.period}...")
        self.stock = yf.Ticker(self.ticker)
        self.data = self.stock.history(period=self.period)
        self.info = self.stock.info
        print(f"✓ Fetched {len(self.data)} days of data")
        return self.data
    
    def calculate_metrics(self):
        """Calculate technical indicators and metrics"""
        print("Calculating technical indicators...")
        
        # Moving averages
        self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
        
        # Daily returns
        self.data['Returns'] = self.data['Close'].pct_change()
        
        # Cumulative returns
        self.data['Cumulative_Returns'] = (1 + self.data['Returns']).cumprod() - 1
        
        # Volatility (rolling 30-day standard deviation)
        self.data['Volatility'] = self.data['Returns'].rolling(window=30).std() * np.sqrt(252)
        
        # Volume moving average
        self.data['Volume_MA'] = self.data['Volume'].rolling(window=20).mean()
        
        print("✓ Calculated technical indicators")
        
    def get_summary_stats(self):
        """Get summary statistics"""
        stats = {
            'Current Price': self.data['Close'].iloc[-1],
            'Period High': self.data['High'].max(),
            'Period Low': self.data['Low'].min(),
            'Average Volume': self.data['Volume'].mean(),
            'Total Return': self.data['Cumulative_Returns'].iloc[-1] * 100,
            'Volatility': self.data['Volatility'].iloc[-1] * 100,
            'Market Cap': self.info.get('marketCap', 'N/A')
        }
        return stats


class NVIDIAVisualizer:
    def __init__(self, data, ticker='NVDA'):
        """Initialize visualizer with data"""
        self.data = data
        self.ticker = ticker
        self.chart_images = []
        
    def create_price_chart(self):
        """Create stock price chart with moving averages"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(self.data.index, self.data['Close'], label='Close Price', linewidth=2, color='#76B900')
        ax.plot(self.data.index, self.data['MA50'], label='50-Day MA', linewidth=1.5, alpha=0.7, color='#FF6B00')
        ax.plot(self.data.index, self.data['MA200'], label='200-Day MA', linewidth=1.5, alpha=0.7, color='#1E90FF')
        
        ax.set_title(f'{self.ticker} Stock Price with Moving Averages', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Price (USD)', fontsize=11)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_volume_chart(self):
        """Create trading volume chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['#76B900' if self.data['Close'].iloc[i] >= self.data['Open'].iloc[i] 
                  else '#E74C3C' for i in range(len(self.data))]
        
        ax.bar(self.data.index, self.data['Volume'], color=colors, alpha=0.6, width=1)
        ax.plot(self.data.index, self.data['Volume_MA'], label='20-Day Volume MA', 
                linewidth=2, color='#1E90FF')
        
        ax.set_title(f'{self.ticker} Trading Volume', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Volume', fontsize=11)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Format y-axis for millions
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_returns_distribution(self):
        """Create daily returns distribution"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        returns = self.data['Returns'].dropna() * 100
        
        ax.hist(returns, bins=50, color='#76B900', alpha=0.7, edgecolor='black')
        ax.axvline(returns.mean(), color='#FF6B00', linestyle='--', linewidth=2, 
                   label=f'Mean: {returns.mean():.2f}%')
        ax.axvline(returns.median(), color='#1E90FF', linestyle='--', linewidth=2, 
                   label=f'Median: {returns.median():.2f}%')
        
        ax.set_title(f'{self.ticker} Daily Returns Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Daily Return (%)', fontsize=11)
        ax.set_ylabel('Frequency', fontsize=11)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_volatility_chart(self):
        """Create volatility chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        volatility = self.data['Volatility'].dropna() * 100
        
        ax.plot(volatility.index, volatility, linewidth=2, color='#E74C3C')
        ax.fill_between(volatility.index, volatility, alpha=0.3, color='#E74C3C')
        
        ax.set_title(f'{self.ticker} 30-Day Rolling Volatility (Annualized)', 
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Volatility (%)', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_cumulative_returns(self):
        """Create cumulative returns chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        cum_returns = self.data['Cumulative_Returns'].dropna() * 100
        
        ax.plot(cum_returns.index, cum_returns, linewidth=2, color='#76B900')
        ax.fill_between(cum_returns.index, cum_returns, alpha=0.3, color='#76B900')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        ax.set_title(f'{self.ticker} Cumulative Returns', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Cumulative Return (%)', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_price_volume_correlation(self):
        """Create price vs volume scatter plot"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        scatter = ax.scatter(self.data['Volume']/1e6, self.data['Close'], 
                            c=self.data['Returns']*100, cmap='RdYlGn', 
                            alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        
        ax.set_title(f'{self.ticker} Price vs Volume (colored by daily return)', 
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Volume (Millions)', fontsize=11)
        ax.set_ylabel('Close Price (USD)', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Daily Return (%)', fontsize=10)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_monthly_heatmap(self):
        """Create monthly performance heatmap"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare monthly returns
        monthly_data = self.data['Returns'].resample('M').apply(lambda x: (1 + x).prod() - 1) * 100
        monthly_data.index = monthly_data.index.to_period('M')
        
        # Create pivot table for heatmap
        pivot_data = pd.DataFrame({
            'Year': monthly_data.index.year,
            'Month': monthly_data.index.month,
            'Return': monthly_data.values
        })
        
        pivot_table = pivot_data.pivot(index='Month', columns='Year', values='Return')
        
        # Create heatmap
        sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                   cbar_kws={'label': 'Return (%)'}, linewidths=0.5, ax=ax)
        
        ax.set_title(f'{self.ticker} Monthly Returns Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=11)
        ax.set_ylabel('Month', fontsize=11)
        
        # Set month labels
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax.set_yticklabels(month_labels, rotation=0)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def create_ohlc_chart(self):
        """Create OHLC (candlestick-style) chart for recent period"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Use last 60 days for clarity
        recent_data = self.data.tail(60)
        
        for idx, row in recent_data.iterrows():
            color = '#76B900' if row['Close'] >= row['Open'] else '#E74C3C'
            
            # Draw high-low line
            ax.plot([idx, idx], [row['Low'], row['High']], color=color, linewidth=1)
            
            # Draw open-close box
            height = abs(row['Close'] - row['Open'])
            bottom = min(row['Open'], row['Close'])
            ax.bar(idx, height, bottom=bottom, width=0.8, color=color, alpha=0.7)
        
        ax.set_title(f'{self.ticker} OHLC Chart (Last 60 Days)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Price (USD)', fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return self._save_figure(fig)
    
    def _save_figure(self, fig):
        """Save figure to bytes buffer"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return buf
    
    def generate_all_charts(self):
        """Generate all visualization charts"""
        print("\nGenerating visualizations...")
        
        charts = [
            ("Price with Moving Averages", self.create_price_chart),
            ("Trading Volume", self.create_volume_chart),
            ("Daily Returns Distribution", self.create_returns_distribution),
            ("Volatility Analysis", self.create_volatility_chart),
            ("Cumulative Returns", self.create_cumulative_returns),
            ("Price vs Volume Correlation", self.create_price_volume_correlation),
            ("Monthly Returns Heatmap", self.create_monthly_heatmap),
            ("OHLC Chart", self.create_ohlc_chart),
        ]
        
        for name, func in charts:
            print(f"  Creating: {name}")
            img_buf = func()
            self.chart_images.append((name, img_buf))
        
        print(f"✓ Generated {len(self.chart_images)} charts")
        return self.chart_images


class PDFReportGenerator:
    def __init__(self, ticker='NVDA', stats=None):
        """Initialize PDF generator"""
        self.ticker = ticker
        self.stats = stats or {}
        self.filename = f'nvidia_insights_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        
    def create_report(self, chart_images):
        """Create PDF report with all charts"""
        print(f"\nGenerating PDF report: {self.filename}")
        
        c = canvas.Canvas(self.filename, pagesize=letter)
        width, height = letter
        
        # Title page
        self._create_title_page(c, width, height)
        c.showPage()
        
        # Add charts (2 per page)
        for i in range(0, len(chart_images), 2):
            # First chart
            title1, img1 = chart_images[i]
            self._add_chart_to_page(c, title1, img1, width, height, position='top')
            
            # Second chart if available
            if i + 1 < len(chart_images):
                title2, img2 = chart_images[i + 1]
                self._add_chart_to_page(c, title2, img2, width, height, position='bottom')
            
            c.showPage()
        
        c.save()
        print(f"✓ PDF report saved: {self.filename}")
        return self.filename
    
    def _create_title_page(self, c, width, height):
        """Create title page with summary statistics"""
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height - 100, f"{self.ticker} Stock Insights Report")
        
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height - 130, 
                           f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}")
        
        # Summary statistics
        y_pos = height - 200
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y_pos, "Summary Statistics")
        
        y_pos -= 30
        c.setFont("Helvetica", 11)
        
        for key, value in self.stats.items():
            if isinstance(value, float):
                if 'Return' in key or 'Volatility' in key:
                    text = f"{key}: {value:.2f}%"
                elif 'Price' in key or 'High' in key or 'Low' in key:
                    text = f"{key}: ${value:.2f}"
                elif 'Volume' in key:
                    text = f"{key}: {value:,.0f}"
                else:
                    text = f"{key}: {value:,.2f}"
            elif isinstance(value, int):
                if key == 'Market Cap':
                    text = f"{key}: ${value:,.0f}"
                else:
                    text = f"{key}: {value:,}"
            else:
                text = f"{key}: {value}"
            
            c.drawString(120, y_pos, text)
            y_pos -= 25
        
        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width/2, 50, 
                           "Data source: Yahoo Finance | This report is for informational purposes only")
    
    def _add_chart_to_page(self, c, title, img_buf, width, height, position='top'):
        """Add a chart to the page"""
        img_buf.seek(0)
        img = ImageReader(img_buf)
        
        # Calculate dimensions
        chart_height = (height - 100) / 2
        chart_width = width - 100
        
        if position == 'top':
            y_pos = height - chart_height - 50
        else:
            y_pos = 50
        
        # Draw chart
        c.drawImage(img, 50, y_pos, width=chart_width, height=chart_height, 
                   preserveAspectRatio=True, mask='auto')


def main():
    """Main execution function"""
    print("=" * 60)
    print("NVIDIA Stock Insights Fetcher & Visualizer")
    print("=" * 60)
    
    # Fetch data
    fetcher = NVIDIAInsightsFetcher(ticker='NVDA', period='1y')
    data = fetcher.fetch_data()
    fetcher.calculate_metrics()
    stats = fetcher.get_summary_stats()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary Statistics:")
    print("=" * 60)
    for key, value in stats.items():
        if isinstance(value, float):
            if 'Return' in key or 'Volatility' in key:
                print(f"{key:.<40} {value:.2f}%")
            elif 'Price' in key or 'High' in key or 'Low' in key:
                print(f"{key:.<40} ${value:.2f}")
            elif 'Volume' in key:
                print(f"{key:.<40} {value:,.0f}")
            else:
                print(f"{key:.<40} {value:,.2f}")
        else:
            print(f"{key:.<40} {value}")
    
    # Generate visualizations
    visualizer = NVIDIAVisualizer(data, ticker='NVDA')
    chart_images = visualizer.generate_all_charts()
    
    # Create PDF report
    pdf_gen = PDFReportGenerator(ticker='NVDA', stats=stats)
    pdf_filename = pdf_gen.create_report(chart_images)
    
    print("\n" + "=" * 60)
    print(f"✓ Complete! PDF report saved as: {pdf_filename}")
    print("=" * 60)


if __name__ == "__main__":
    main()
