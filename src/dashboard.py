import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config
st.set_page_config(
    page_title="Primetrade: Trader Behavior",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Trader Behavior vs. Market Sentiment")
st.markdown("""
**Objective:** Analyze how market sentiment (Fear vs. Greed) impacts trader profitability and risk management.
""")

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        df_daily = pd.read_csv('data/prepared_trader_sentiment.csv')
        df_clusters = pd.read_csv('data/trader_profiles_clustered.csv')
        
        df_daily['date'] = pd.to_datetime(df_daily['date'])
        
        # Merge archetype data into the daily data so we can filter by it
        df_merged = pd.merge(df_daily, df_clusters[['Account', 'Archetype']], on='Account', how='left')
        
        sentiment_order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
        return df_merged, df_clusters, sentiment_order
    except FileNotFoundError:
        st.error("❌ Data files not found! Please check the 'data/' folder.")
        return None, None, None

df_merged, df_clusters, sentiment_order = load_data()

if df_merged is not None:

    st.sidebar.header("🔍 Global Filters")
    
    # Archetype Filter
    selected_archetypes = st.sidebar.multiselect(
        "Filter by Trader Archetype",
        options=df_clusters['Archetype'].unique(),
        default=df_clusters['Archetype'].unique()
    )
    
    # Filter Data based on selection
    df_filtered = df_merged[df_merged['Archetype'].isin(selected_archetypes)]

    # --- KPI Row ---
    st.markdown("### 📊 Market Snapshot")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_win_rate = df_filtered['win_rate'].mean()
    fear_trades = df_filtered[df_filtered['sentiment_label'] == 'Extreme Fear']['total_trades'].sum()
    greed_trades = df_filtered[df_filtered['sentiment_label'] == 'Extreme Greed']['total_trades'].sum()
    total_pnl = df_filtered['daily_pnl'].sum()

    col1.metric("Avg Win Rate", f"{avg_win_rate:.1%}")
    col2.metric("Total PnL Tracked", f"${total_pnl:,.0f}")
    col3.metric("Trades in Extreme Fear", f"{fear_trades:,}")
    col4.metric("Trades in Extreme Greed", f"{greed_trades:,}")

    st.divider()

    # --- Tab Layout ---
    tab1, tab2, tab3, tab4 = st.tabs(["📉 Sentiment Analysis", "🧠 Trader Clusters", "🔎 Individual Deep Dive", "🤖 Strategy Rules"])

    # === TAB 1: SENTIMENT ANALYSIS ===
    with tab1:
        st.subheader("Interactive Sentiment Performance")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("**Insight 1: Daily PnL Distribution**")
            pnl_clipped = df_filtered[df_filtered['daily_pnl'].between(-1000, 1000)]
            fig_box = px.box(
                pnl_clipped, 
                x='sentiment_label', 
                y='daily_pnl', 
                color='sentiment_label',
                category_orders={'sentiment_label': sentiment_order},
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_box.update_layout(showlegend=False, xaxis_title="Sentiment", yaxis_title="Daily PnL ($)")
            st.plotly_chart(fig_box, use_container_width=True)

        with col_right:
            st.markdown("**Insight 2: Win Rate vs. Sentiment**")
            avg_wr = df_filtered.groupby('sentiment_label')['win_rate'].mean().reindex(sentiment_order).reset_index()
            fig_bar = px.bar(
                avg_wr, 
                x='sentiment_label', 
                y='win_rate',
                color='sentiment_label',
                category_orders={'sentiment_label': sentiment_order},
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_bar.update_layout(showlegend=False, xaxis_title="Sentiment", yaxis_title="Win Rate")
            fig_bar.update_yaxes(tickformat=".1%")
            st.plotly_chart(fig_bar, use_container_width=True)

    # === TAB 2: CLUSTERING ===
    with tab2:
        st.subheader("Behavioral Archetypes (K-Means)")
        
        # Create an absolute value column just for bubble sizing
        df_clusters['abs_pnl'] = df_clusters['lifetime_pnl'].abs()
        
        # Interactive Scatter Plot
        st.markdown("**Cluster Visualization: Frequency vs. Trade Size**")
        fig_cluster = px.scatter(
            df_clusters, 
            x='total_lifetime_trades', 
            y='avg_trade_size', 
            color='Archetype',
            size='abs_pnl',  # <--- FIX: Using absolute value for size
            size_max=40,
            hover_name='Account',
            # We hide 'abs_pnl' from the hover and show the real 'lifetime_pnl'
            hover_data={'abs_pnl': False, 'lifetime_pnl': ':$,.2f', 'avg_win_rate': ':.1%'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_cluster.update_layout(xaxis_title="Total Lifetime Trades", yaxis_title="Average Trade Size ($)")
        st.plotly_chart(fig_cluster, use_container_width=True)
        st.caption("*Bubble size represents total magnitude of PnL (Wins or Losses). Hover over bubbles to see actual PnL and Account IDs.*")
    
    
    # === TAB 3: INDIVIDUAL DEEP DIVE ===
    with tab3:
        st.subheader("🔎 Search Individual Trader")
        
        # Top 50 accounts by PnL to make the dropdown manageable, or allow typing
        top_accounts = df_clusters.sort_values(by='lifetime_pnl', ascending=False)['Account'].head(100).tolist()
        selected_account = st.selectbox("Select or Type an Account ID (Top 100 Profitable shown):", top_accounts)
        
        if selected_account:
            acc_data = df_clusters[df_clusters['Account'] == selected_account].iloc[0]
            st.markdown(f"### Profile: **{acc_data['Archetype']}**")
            
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Lifetime PnL", f"${acc_data['lifetime_pnl']:,.2f}")
            sc2.metric("Win Rate", f"{acc_data['avg_win_rate']:.1%}")
            sc3.metric("Total Trades", f"{acc_data['total_lifetime_trades']:,}")

    # === TAB 4: STRATEGY ===
    with tab4:
        st.subheader("💡 Actionable Rules of Thumb")
        st.success("""
        ### ✅ Rule 1: The "Volatility Filter"
        **IF** Sentiment == `Extreme Fear` (< 20):
        * **Reduce Trade Frequency by 50%**.
        * **Reason:** Data shows `Extreme Fear` days have 133+ trades/day (panic scalping) but lower win rates. Avoid the chop.
        """)
        st.warning("""
        ### ⚠️ Rule 2: The "Greed De-Leveraging"
        **IF** Sentiment == `Greed` (> 60):
        * **Cap Max Leverage & Take Profit**.
        * **Reason:** While win rates are high, the largest historical drawdowns (-$350k+) happen here due to over-leverage.
        """)