# Time In Market Simulator
# Copyright (c) 2026 Khushaldas Vasant Badhan
# Licensed under the MIT License


import requests
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

def get_ticker_info(isin):
    """Searches Yahoo Finance for the Ticker symbol associated with an ISIN."""
    print(f"🔍 Searching for ISIN: {isin}...")
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin}"
    # Yahoo requires a User-Agent header for python scripts
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} 
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    if 'quotes' not in data or len(data['quotes']) == 0:
        raise ValueError(f"Could not find a valid ticker for ISIN: {isin}")
        
    symbol = data['quotes'][0]['symbol']
    name = data['quotes'][0].get('longname', data['quotes'][0].get('shortname', symbol))
    return symbol, name

def get_next_trading_day(target_date, trading_days):
    """Finds the next available trading day on or after the target date."""
    valid_dates = trading_days[trading_days >= target_date]
    if not valid_dates.empty:
        return valid_dates[0]
    return None

def calculate_sip(df, amount, freq_type, freq_val):
    """Calculates the Systematic Investment Plan (SIP) growth on daily data."""
    # Ensure we only work with the closing prices and drop missing data
    df = df[['Close']].dropna().copy()
    
    # Initialize tracking columns
    df['Invested_Today'] = 0.0
    df['Shares_Bought_Today'] = 0.0
    
    trading_days = df.index

    # Determine investment dates
    investment_dates = []
    
    if freq_type == 'monthly':
        day_of_month = int(freq_val)
        # Group by year and month
        for (year, month), _ in df.groupby([df.index.year, df.index.month]):
            # Construct target date
            try:
                target_date = pd.Timestamp(year=year, month=month, day=day_of_month, tz=df.index.tz)
            except ValueError:
                # Handle cases like Feb 30th -> snap to last day of month
                last_day = calendar.monthrange(year, month)[1]
                target_date = pd.Timestamp(year=year, month=month, day=last_day, tz=df.index.tz)
                
            actual_date = get_next_trading_day(target_date, trading_days)
            # Only add if actual_date is still within the same month (or we might skip if end of month, but next trading day is fine)
            if actual_date is not None:
                # To prevent double investing if target is late in month and rolls to next month
                if actual_date not in investment_dates:
                     investment_dates.append(actual_date)
            
    elif freq_type == 'weekly':
        # freq_val is weekday name, e.g., 'Monday'
        target_weekday = time.strptime(freq_val, '%A').tm_wday # 0=Mon, 6=Sun
        
        # Start from the first day in the dataframe
        current_date = df.index[0]
        end_date = df.index[-1]
        
        while current_date <= end_date:
            if current_date.weekday() == target_weekday:
                actual_date = get_next_trading_day(current_date, trading_days)
                if actual_date is not None and actual_date not in investment_dates:
                    investment_dates.append(actual_date)
            current_date += timedelta(days=1)
            
    # Apply investments
    for date in investment_dates:
        if date in df.index:
            df.loc[date, 'Invested_Today'] += amount
            df.loc[date, 'Shares_Bought_Today'] += amount / df.loc[date, 'Close']

    # Calculate cumulative totals
    df['Total_Invested'] = df['Invested_Today'].cumsum()
    df['Total_Shares'] = df['Shares_Bought_Today'].cumsum()
    
    df['Portfolio_Value'] = df['Total_Shares'] * df['Close']
    df['Profit'] = df['Portfolio_Value'] - df['Total_Invested']
    
    df['Profit_Pct'] = (df['Profit'] / df['Total_Invested']) * 100
    df['Profit_Pct'] = df['Profit_Pct'].fillna(0)
    return df

def plot_results(df, name, symbol, amount, freq_str):
    """Generates an interactive, premium Plotly chart."""
    fig = go.Figure()

    # Total Invested Line Chart (Step chart to show jumps on investment days)
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Total_Invested'],
        mode='lines',
        name='Total Cash Invested',
        line=dict(color='#94a3b8', width=2, dash='dash', shape='hv'),
        hovertemplate="<b>Total Invested:</b> €%{y:,.2f}<extra></extra>"
    ))

    # Portfolio Value Area Chart
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Portfolio_Value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#0ea5e9', width=3),
        fill='tozeroy',
        fillcolor='rgba(14, 165, 233, 0.15)',
        customdata=df[['Total_Invested', 'Profit', 'Profit_Pct']],
        hovertemplate=(
            "<b>Portfolio Value:</b> €%{y:,.2f}<br>"
            "<b>P&L:</b> €%{customdata[1]:,.2f} (%{customdata[2]:.2f}%)"
            "<extra></extra>"
        )
    ))

    # Advanced styling for a clean, beautiful look
    fig.update_layout(
        title=dict(
            text=f"<b>Time In Market Simulator</b><br><span style='font-size: 14px; color: #64748b;'>{name} ({symbol}) • €{amount} {freq_str}</span>",
            font=dict(family="Inter, Roboto, Arial", size=24, color="#0f172a"),
            y=0.95, x=0.05, xanchor='left', yanchor='top'
        ),
        xaxis_title="",
        yaxis_title="Value (€)",
        font=dict(family="Inter, Roboto, Arial", color="#334155"),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            font_size=13,
            font_family="Inter, Roboto, Arial",
            bordercolor="#e2e8f0"
        ),
        template="plotly_white",
        legend=dict(
            orientation="h", yanchor="top", y=1.08, xanchor="right", x=0.98,
            bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="#e2e8f0", borderwidth=1
        ),
        margin=dict(l=60, r=40, t=110, b=60),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    
    # Format axes with subtle grid lines
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="#f1f5f9",
        showline=True, linewidth=1, linecolor="#cbd5e1",
        tickfont=dict(color="#64748b")
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="#f1f5f9",
        showline=True, linewidth=1, linecolor="#cbd5e1",
        tickprefix="€", tickformat=",.0f",
        tickfont=dict(color="#64748b")
    )
    
    print("\n📈 Opening interactive chart in your web browser...")
    fig.show()

import time

def parse_date(date_str, default):
    if not date_str: return default
    try:
        pd.to_datetime(date_str)
        return date_str
    except:
        return default

def main():
    print("="*50)
    print(" 🚀 Time In Market Simulator  ")
    print("="*50)
    
    # 1. Input ISIN
    isin = input("Enter Instrument ISIN (e.g., 'IE00B4L5Y983'): ").strip().upper()
    while not isin:
        print("ISIN not correctly entered. Please try again.")
        isin = input("Enter Instrument ISIN (e.g., 'IE00B4L5Y983'): ").strip().upper()
        
    # 2. Input Amount
    try:
        amount = float(input("Enter investment amount per period (e.g., 100, 250.50) [default 100]: ") or 100)
    except ValueError:
        amount = 100.0
        print("Invalid input, defaulting to €100")
        
    # 3. Frequency
    freq_choice = input("Enter investment frequency ('Weekly' or 'Monthly') [default: Monthly]: ").strip().lower()
    if freq_choice == 'weekly':
        freq_type = 'weekly'
        default_day = 'Monday'
        freq_val = input("Enter day of week to invest (e.g., 'Monday', 'Tuesday') [default: Monday]: ").strip().capitalize()
        # validate weekday
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if freq_val not in days:
            print(f"Invalid day, defaulting to {default_day}")
            freq_val = default_day
        freq_str = f"weekly on {freq_val}s"
    else:
        freq_type = 'monthly'
        default_day = '1'
        freq_val = input("Enter calendar day of month to invest (1-28) [default: 1]: ").strip()
        if not freq_val.isdigit() or not (1 <= int(freq_val) <= 31):
            print(f"Invalid day, defaulting to {default_day}")
            freq_val = default_day
        freq_str = f"monthly on the {freq_val}th"

    # 4. Dates
    start_date_str = input("Enter start date in YYYY-MM-DD format (e.g., '2015-01-01') [default: 10 years ago]: ").strip()
    end_date_str = input("Enter end date in YYYY-MM-DD format (e.g., '2024-01-01') [default: Today]: ").strip()
    
    end_date = parse_date(end_date_str, pd.Timestamp.today().strftime('%Y-%m-%d'))
    default_start = (pd.Timestamp(end_date) - pd.DateOffset(years=10)).strftime('%Y-%m-%d')
    start_date = parse_date(start_date_str, default_start)

    try:
        # a. Map ISIN to Ticker
        symbol, name = get_ticker_info(isin)
        print(f"✅ Found: {name} ({symbol})")
        
        # b. Fetch Historical Data (Daily intervals)
        print(f"📥 Fetching daily historical data from {start_date} to {end_date}...")
        try:
            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(start=start_date, end=end_date, interval="1d")
        except Exception as data_err:
            err_msg = str(data_err).lower()
            if 'ssl' in err_msg or 'certificate' in err_msg or 'curl' in err_msg:
                print("\n" + "!" * 80)
                print(" 🔒 CORPORATE NETWORK DETECTED: SSL Certificate Verification Failed")
                print("!" * 80)
                print("Your IT department is intercepting the connection with a self-signed certificate.")
                print("To securely resolve this without bypassing your company's security policies:")
                print(" 1. Ask your IT team for the company's Root CA Certificate (.pem file)")
                print(" 2. Set the environment variable 'CURL_CA_BUNDLE' to the path of that file.")
                print("    Example (Windows Command Prompt):  set CURL_CA_BUNDLE=C:\\path\\to\\cert.pem")
                print("    Example (PowerShell):             $env:CURL_CA_BUNDLE=\"C:\\path\\to\\cert.pem\"")
                print(" Then run this script again.")
                print("!" * 80 + "\n")
                return # Exit gracefully
            else:
                raise data_err
        
        if hist_data.empty:
            raise ValueError("No historical price data found for this instrument in the given date range.")

        # c. Process Data
        print("🧮 Calculating portfolio growth...")
        results_df = calculate_sip(hist_data, amount, freq_type, freq_val)
        
        # d. Print KPIs to console
        final_stats = results_df.iloc[-1]
        if final_stats['Total_Invested'] > 0:
            roi = (final_stats['Profit'] / final_stats['Total_Invested']) * 100
        else:
            roi = 0.0
            
        print("\n" + "="*50)
        print(" 📊 SIMULATION SUMMARY")
        print("="*50)
        print(f"Total Invested:        €{final_stats['Total_Invested']:,.2f}")
        print(f"Final Portfolio Value: €{final_stats['Portfolio_Value']:,.2f}")
        print(f"Total Profit:          €{final_stats['Profit']:,.2f}")
        print(f"Return on Investment:  {roi:.2f}%")
        print(f"Period:                {start_date} to {end_date}")
        print(f"Investment Frequency:  {freq_str.capitalize()}")
        print("="*50)

        # e. Visualize
        plot_results(results_df, name, symbol, amount, freq_str)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":

    main()
