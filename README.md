 📊 Trader Behavior Insights vs. Market Sentiment
**🔗 Live Demo:** [yash-behavioral-finance.streamlit.app](https://yash-behavioral-finance.streamlit.app/)
## 1. Project Overview & Methodology
This project investigates whether crypto traders on the Hyperliquid exchange act rationally or if they are driven by the psychological cycles of **Fear and Greed**. The goal was to align market sentiment with transactional data to uncover behavioral patterns and formulate actionable trading "Rules of Thumb."

### 🔧 The Pipeline

1. **Data Engineering:**  
   - Merged two disparate datasets: Daily Bitcoin Fear/Greed Index and high-frequency Hyperliquid trade logs (IST timestamps).  
   - Aggregated **211,224 individual trades** into daily account-level metrics, calculating daily PnL, Win Rate, Volume, and Trade Frequency per user.

2. **Exploratory Data Analysis:**  
   - Visualized the distribution of PnL and Win Rates across 5 sentiment tiers (Extreme Fear to Extreme Greed).

3. **Machine Learning:**  
   - Deployed **K-Means Clustering** on standardized lifetime trader metrics to mathematically identify distinct behavioral segments:
     - **Scalpers:** Algorithmic bots or highly disciplined high-frequency traders.
     - **Whales:** Institutional or heavily capitalized traders who deploy large position sizes strategically.
     - **Retail Traders:** Emotion-driven traders with smaller capital bases and higher exposure to behavioral bias.

---

## 2. Key Insights (The "Why")

### 📉 Insight 1: Fear Creates Hyperactivity
* **The Data:** During "Extreme Fear" days, the average trade frequency spikes to its highest level (**133 trades/day**), but the average trade size drops significantly to **$6,773**.
* **Interpretation:** Traders panic-scalp. They are too scared to hold positions, resulting in a "chop" environment where they over-trade with small size to avoid exposure.

### 🐋 Insight 2: Whales Buy the Fear
* **The Data:** While the herd panics, the absolute highest average trade sizes (**$8,975 per trade**) occur during standard "Fear" days.
* **Interpretation:** "Smart Money" or capitalized traders act as contrarians, deploying their largest position sizes when the market is fearful, likely accumulating at discounted prices.

### 🚨 Insight 3: The "Greed Trap"
* **The Data:** "Extreme Greed" days show the highest win rate (**38.6%**). However, regular "Greed" days contain the most catastrophic tail-risk, including the single largest daily loss in the dataset (**-$358,963**).
* **Interpretation:** Retail traders get overconfident during rallies, using excessive leverage. When the inevitable pullback occurs, they face massive liquidations, leading to outsized losses despite the generally bullish trend.

---

## 3. Trader Segmentation (K-Means Clustering)
Using unsupervised learning, I identified three distinct trader profiles:

| Archetype | Behavior Profile | Performance |
| :--- | :--- | :--- |
| **The High-Frequency Scalpers** | Huge volume (21k+ trades), tiny size ($2.5k), high win rate (50.7%). | **Most Profitable ($571k)** |
| **The Whales** | Low frequency (~5k trades), massive size ($23.8k), moderate win rate. | **Highly Profitable ($498k)** |
| **The Retail Average** | Moderate frequency, medium size, lowest win rate (31.9%). | **Least Profitable** |

---

## 4. Actionable Strategy Recommendations
Based on these findings, I propose the following algorithmic rules:

### ✅ Rule 1: The "Volatility Filter" (Defensive)
* **Trigger:** Market Sentiment drops below 20 (**Extreme Fear**).
* **Logic:** The data proves this environment is characterized by irrational high-frequency "chop" (133 trades/day) and low win rates (32.9%).
* **Action:** - **Reduce Execution Frequency by 50%**: Stop chasing every tick.
   - **Widen Stop-Losses**: To account for the increased volatility and avoid getting wicked out.

### ✅ Rule 2: The "Greed De-Leveraging" Protocol (Risk Mgmt)
* **Trigger:** Market Sentiment crosses above 60 (**Greed**).
* **Logic:** While win rates are high, the risk of catastrophic liquidation is at its peak (max drawdown -$358k).
* **Action:** - **Cap Maximum Leverage**: Strictly forbid increasing leverage.
   - **Take Profit Aggressively**: Counter-trade the "Retail Average" segment who are likely over-leveraged at the top.

---

## 💻 How to Run This Project
1. Clone the repository:
   ```bash
   git clone https://github.com/yashkumar181/Behavioral_Finance

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the Jupyter Notebooks in the notebooks/ folder to reproduce the analysis.
  
