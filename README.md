---
### ⚖️ Copyright & Credit
Copyright (c) 2026 Khushaldas Vasant Badhan
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
**Credit is required** if you use, modify, or redistribute this script.

# **🚀 Time In Market Simulator**

An interactive Python tool designed to simulate **Systematic Investment Plans (SIP)** using historical market data. This script helps visualize the power of long-term investing ("Time in the Market") versus trying to predict price movements.

## **📋 Table of Contents**

* [Features](https://www.google.com/search?q=%23-features)  
* [Dependencies](https://www.google.com/search?q=%23-dependencies)  
* [Installation](https://www.google.com/search?q=%23%25EF%25B8%258F-installation)  
* [Usage](https://www.google.com/search?q=%23-usage)  
* [License](https://www.google.com/search?q=%23-license)  
* [Disclaimer](https://www.google.com/search?q=%23-disclaimer)

## **✨ Features**

* **Automated ISIN Lookup:** Seamlessly converts international ISIN codes to Yahoo Finance tickers using their search API.  
* **Flexible Investment Frequency:** Supports both **Weekly** (specific days of the week) and **Monthly** (specific dates) investment schedules.  
* **Smart Calendar Logic:** Automatically identifies the next available trading day if a scheduled investment falls on a weekend or market holiday.  
* **Interactive Visualizations:** Generates high-fidelity, interactive charts via **Plotly**, allowing you to inspect portfolio value, total invested cash, and P\&L percentages at any point in time.  
* **Robust Error Handling:** Includes built-in guidance for users on corporate networks facing SSL certificate verification issues.

## **📦 Dependencies**

To run this simulator, you will need Python 3.x installed along with the following libraries:

* [**yfinance**](https://www.google.com/search?q=https://github.com/ranaroussi/yfinance)**:** Used to fetch historical market price data from Yahoo Finance.  
* [**pandas**](https://www.google.com/search?q=https://pandas.pydata.org/)**:** Core library for data manipulation and performing time-series SIP calculations.  
* [**plotly**](https://www.google.com/search?q=https://plotly.com/python/)**:** Powers the high-quality, interactive web-based charts.  
* [**requests**](https://www.google.com/search?q=https://requests.readthedocs.io/)**:** Handles the API requests needed for the ISIN-to-Ticker resolution.

## **🛠️ Installation**

### **1\. Clone the Repository**

git clone \[https://github.com/YOUR\_USERNAME/time-in-market-simulator.git\](https://github.com/YOUR\_USERNAME/time-in-market-simulator.git)  
cd time-in-market-simulator

### **2\. Install Required Packages**

You can install all dependencies at once using the provided requirements file:  
pip install \-r requirements.txt

*Alternatively, you can install them individually:*  
pip install yfinance pandas plotly requests

## **🚀 Usage**

Launch the simulator by running the main script and following the terminal prompts:  
python main.py

### **Example Simulation Input:**

* **Instrument ISIN:** IE00B4L5Y983 (e.g., iShares Core MSCI World)  
* **Investment Amount:** 500  
* **Frequency:** Monthly  
* **Day of Month:** 1  
* **Start Date:** 2010-01-01

The script will fetch the data, calculate the growth, and automatically open a new tab in your default web browser with the interactive results.

## **⚖️ License**

This project is licensed under the **MIT License**.  
Under this license, you are free to use, modify, and distribute this software, provided that the **original copyright notice** and this permission notice are included in all copies or substantial portions of the software. This ensures that credit is attributed to the original author.

## **📊 Disclaimer**

*This software is for educational and informational purposes only. It does not constitute financial advice. Past performance of any financial instrument is not a reliable indicator of future results. Always perform your own due diligence or consult with a certified financial advisor before making investment decisions.*  
**Maintained by:** \[Your Name/Username\]  
**Project Link:** [https://github.com/YOUR\_USERNAME/time-in-market-simulator](https://www.google.com/search?q=https://github.com/YOUR_USERNAME/time-in-market-simulator)
