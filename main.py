import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our custom modules (with error handling for development)
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
    from scripts.data_processor import DataProcessor
    from scripts.metrics_calculator import MetricsCalculator
except ImportError:
    st.error("Unable to import custom modules. Please ensure all dependencies are installed.")
    st.stop()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .insight-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_real_data():
    """Load actual marketing data from CSV files"""
    try:
        # Load Facebook data
        facebook_df = pd.read_csv('data/Facebook.csv')
        facebook_df['channel'] = 'Facebook'
        
        # Load Google data
        google_df = pd.read_csv('data/Google.csv')
        google_df['channel'] = 'Google'
        
        # Load TikTok data
        tiktok_df = pd.read_csv('data/TikTok.csv')
        tiktok_df['channel'] = 'TikTok'
        
        # Load Business data
        business_df = pd.read_csv('data/business.csv')
        
        # Standardize column names for marketing data
        marketing_column_mapping = {
            'impression': 'impressions',
            'attributed revenue': 'attributed_revenue'
        }
        
        for df in [facebook_df, google_df, tiktok_df]:
            df.rename(columns=marketing_column_mapping, inplace=True)
        
        # Standardize column names for business data
        business_column_mapping = {
            '# of orders': 'orders',
            '# of new orders': 'new_orders',
            'total revenue': 'total_revenue',
            'gross profit': 'gross_profit',
            'new customers': 'new_customers',
            'COGS': 'cogs'
        }
        business_df.rename(columns=business_column_mapping, inplace=True)
        
        # Combine marketing data
        marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        
        # Convert date columns to datetime
        marketing_df['date'] = pd.to_datetime(marketing_df['date'])
        business_df['date'] = pd.to_datetime(business_df['date'])
        
        return marketing_df, business_df
        
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.info("📁 Please ensure Facebook.csv, Google.csv, TikTok.csv, and business.csv are in the data/ directory")
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.info("🔍 Please check your data file formats and column names")
        return None, None

@st.cache_data
def process_data(marketing_df, business_df):
    """Process and combine data"""
    # Convert date columns to datetime
    marketing_df['date'] = pd.to_datetime(marketing_df['date'])
    business_df['date'] = pd.to_datetime(business_df['date'])
    
    # Calculate derived metrics for marketing data
    marketing_df['ctr'] = np.where(
        marketing_df['impressions'] > 0,
        marketing_df['clicks'] / marketing_df['impressions'] * 100,
        0
    )
    marketing_df['cpc'] = np.where(
        marketing_df['clicks'] > 0,
        marketing_df['spend'] / marketing_df['clicks'],
        0
    )
    marketing_df['roas'] = np.where(
        marketing_df['spend'] > 0,
        marketing_df['attributed_revenue'] / marketing_df['spend'],
        0
    )
    
    # Calculate derived metrics for business data
    business_df['aov'] = np.where(
        business_df['orders'] > 0,
        business_df['total_revenue'] / business_df['orders'],
        0
    )
    business_df['gross_margin'] = np.where(
        business_df['total_revenue'] > 0,
        business_df['gross_profit'] / business_df['total_revenue'] * 100,
        0
    )
    
    # Aggregate marketing data by date
    daily_marketing = marketing_df.groupby('date').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum',
        'attributed_revenue': 'sum'
    }).reset_index()
    
    # Recalculate daily metrics
    daily_marketing['ctr'] = np.where(
        daily_marketing['impressions'] > 0,
        daily_marketing['clicks'] / daily_marketing['impressions'] * 100,
        0
    )
    daily_marketing['cpc'] = np.where(
        daily_marketing['clicks'] > 0,
        daily_marketing['spend'] / daily_marketing['clicks'],
        0
    )
    daily_marketing['roas'] = np.where(
        daily_marketing['spend'] > 0,
        daily_marketing['attributed_revenue'] / daily_marketing['spend'],
        0
    )
    
    # Combine data
    combined_df = pd.merge(business_df, daily_marketing, on='date', how='left')
    combined_df = combined_df.fillna(0)
    
    # Additional metrics
    combined_df['marketing_efficiency'] = np.where(
        combined_df['spend'] > 0,
        combined_df['total_revenue'] / combined_df['spend'],
        0
    )
    combined_df['cpa'] = np.where(
        combined_df['new_customers'] > 0,
        combined_df['spend'] / combined_df['new_customers'],
        0
    )
    
    return marketing_df, business_df, combined_df

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Marketing Intelligence Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("### Real-Time Marketing Performance Analysis")
    st.markdown("*Analyzing Facebook, Google, and TikTok campaign data*")
    
    # Load real data
    with st.spinner("Loading your marketing data..."):
        marketing_df, business_df = load_real_data()
        
        if marketing_df is None or business_df is None:
            st.stop()
            
        marketing_df, business_df, combined_df = process_data(marketing_df, business_df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = combined_df['date'].min().date()
    max_date = combined_df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Channel filter
    channels = ['All'] + list(marketing_df['channel'].unique())
    selected_channel = st.sidebar.selectbox("Select Channel", channels)
    
    # Campaign filter
    if selected_channel != 'All':
        campaigns = ['All'] + list(marketing_df[marketing_df['channel'] == selected_channel]['campaign'].unique())
    else:
        campaigns = ['All'] + list(marketing_df['campaign'].unique())
    selected_campaign = st.sidebar.selectbox("Select Campaign", campaigns)
    
    # Filter data based on selections
    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        
        filtered_combined = combined_df[
            (combined_df['date'] >= start_date) & 
            (combined_df['date'] <= end_date)
        ]
        filtered_marketing = marketing_df[
            (marketing_df['date'] >= start_date) & 
            (marketing_df['date'] <= end_date)
        ]
    else:
        filtered_combined = combined_df
        filtered_marketing = marketing_df
    
    if selected_channel != 'All':
        filtered_marketing = filtered_marketing[filtered_marketing['channel'] == selected_channel]
    
    if selected_campaign != 'All':
        filtered_marketing = filtered_marketing[filtered_marketing['campaign'] == selected_campaign]
    
    # Executive Summary
    st.header("📈 Executive Summary")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_combined['total_revenue'].sum()
        st.metric(
            label="Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"{(total_revenue/len(filtered_combined)):.0f}/day avg"
        )
    
    with col2:
        total_spend = filtered_marketing['spend'].sum()
        st.metric(
            label="Marketing Spend",
            value=f"${total_spend:,.0f}",
            delta=f"{(total_spend/len(filtered_combined)):.0f}/day avg"
        )
    
    with col3:
        overall_roas = filtered_marketing['attributed_revenue'].sum() / filtered_marketing['spend'].sum() if filtered_marketing['spend'].sum() > 0 else 0
        st.metric(
            label="Overall ROAS",
            value=f"{overall_roas:.2f}x",
            delta="Return on Ad Spend"
        )
    
    with col4:
        total_customers = filtered_combined['new_customers'].sum()
        cac = total_spend / total_customers if total_customers > 0 else 0
        st.metric(
            label="Customer Acquisition Cost",
            value=f"${cac:.2f}",
            delta=f"{total_customers:,.0f} new customers"
        )
    
    # Main charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Revenue vs Marketing Spend Trend")
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Daily Revenue', 'Daily Marketing Spend'),
            vertical_spacing=0.1
        )
        
        # Revenue trend
        fig.add_trace(
            go.Scatter(
                x=filtered_combined['date'],
                y=filtered_combined['total_revenue'],
                mode='lines+markers',
                name='Total Revenue',
                line=dict(color='#1f77b4', width=3)
            ),
            row=1, col=1
        )
        
        # Spend trend
        fig.add_trace(
            go.Scatter(
                x=filtered_combined['date'],
                y=filtered_combined['spend'],
                mode='lines+markers',
                name='Marketing Spend',
                line=dict(color='#ff7f0e', width=3)
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=500, showlegend=True)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Spend ($)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Channel Performance")
        
        # Channel metrics
        channel_metrics = filtered_marketing.groupby('channel').agg({
            'spend': 'sum',
            'attributed_revenue': 'sum',
            'impressions': 'sum',
            'clicks': 'sum'
        })
        
        channel_metrics['roas'] = channel_metrics['attributed_revenue'] / channel_metrics['spend']
        
        # ROAS by channel chart
        fig_roas = px.bar(
            x=channel_metrics.index,
            y=channel_metrics['roas'],
            title="ROAS by Channel",
            labels={'x': 'Channel', 'y': 'ROAS'},
            color=channel_metrics['roas'],
            color_continuous_scale='Viridis'
        )
        fig_roas.update_layout(height=300)
        st.plotly_chart(fig_roas, use_container_width=True)
        
        # Channel spend distribution
        fig_spend = px.pie(
            values=channel_metrics['spend'],
            names=channel_metrics.index,
            title="Spend Distribution"
        )
        fig_spend.update_layout(height=300)
        st.plotly_chart(fig_spend, use_container_width=True)
    
    # Channel Deep Dive
    st.header("🔍 Channel Deep Dive")
    
    col1, col2, col3 = st.columns(3)
    
    channels_list = filtered_marketing['channel'].unique()
    
    for i, channel in enumerate(channels_list):
        channel_data = filtered_marketing[filtered_marketing['channel'] == channel]
        
        with [col1, col2, col3][i % 3]:
            st.subheader(f"{channel}")
            
            total_spend_ch = channel_data['spend'].sum()
            total_revenue_ch = channel_data['attributed_revenue'].sum()
            roas_ch = total_revenue_ch / total_spend_ch if total_spend_ch > 0 else 0
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>{channel} Performance</h4>
                <p><strong>Spend:</strong> ${total_spend_ch:,.0f}</p>
                <p><strong>Revenue:</strong> ${total_revenue_ch:,.0f}</p>
                <p><strong>ROAS:</strong> {roas_ch:.2f}x</p>
                <p><strong>Campaigns:</strong> {channel_data['campaign'].nunique()}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Campaign Performance Table
    st.header("📋 Campaign Performance Analysis")
    
    campaign_summary = filtered_marketing.groupby(['channel', 'campaign']).agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum',
        'attributed_revenue': 'sum'
    }).reset_index()
    
    campaign_summary['CTR'] = (campaign_summary['clicks'] / campaign_summary['impressions'] * 100).round(2)
    campaign_summary['CPC'] = (campaign_summary['spend'] / campaign_summary['clicks']).round(2)
    campaign_summary['ROAS'] = (campaign_summary['attributed_revenue'] / campaign_summary['spend']).round(2)
    
    # Format for display
    display_df = campaign_summary.copy()
    display_df['Spend'] = display_df['spend'].apply(lambda x: f"${x:,.0f}")
    display_df['Revenue'] = display_df['attributed_revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Impressions'] = display_df['impressions'].apply(lambda x: f"{x:,}")
    display_df['Clicks'] = display_df['clicks'].apply(lambda x: f"{x:,}")
    
    st.dataframe(
        display_df[['channel', 'campaign', 'Impressions', 'Clicks', 'CTR', 'CPC', 'Spend', 'Revenue', 'ROAS']],
        use_container_width=True
    )
    
    # Insights Section
    st.header("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Best performing channel
        best_channel = channel_metrics['roas'].idxmax()
        best_roas = channel_metrics['roas'].max()
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>🏆 Top Performing Channel</h4>
            <p><strong>{best_channel}</strong> is delivering the highest ROAS at <strong>{best_roas:.2f}x</strong></p>
            <p>Consider increasing budget allocation to this channel for better overall performance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Marketing efficiency
        total_revenue_all = filtered_combined['total_revenue'].sum()
        total_spend_all = filtered_marketing['spend'].sum()
        efficiency = total_revenue_all / total_spend_all if total_spend_all > 0 else 0
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>📈 Marketing Efficiency</h4>
            <p>Every $1 spent on marketing generates <strong>${efficiency:.2f}</strong> in total revenue</p>
            <p>{"Strong" if efficiency > 5 else "Moderate" if efficiency > 3 else "Needs improvement"} marketing efficiency overall.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Growth trend
        if len(filtered_combined) >= 30:
            recent_avg = filtered_combined.tail(15)['total_revenue'].mean()
            early_avg = filtered_combined.head(15)['total_revenue'].mean()
            growth = ((recent_avg - early_avg) / early_avg) * 100 if early_avg > 0 else 0
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>📊 Revenue Trend</h4>
                <p>Revenue is <strong>{"growing" if growth > 0 else "declining"}</strong> by <strong>{abs(growth):.1f}%</strong></p>
                <p>Recent 15-day average: ${recent_avg:,.0f} vs Early 15-day average: ${early_avg:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Customer acquisition
        avg_cac = cac
        avg_aov = filtered_combined['aov'].mean()
        cac_ratio = avg_cac / avg_aov if avg_aov > 0 else 0
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>👥 Customer Acquisition</h4>
            <p>CAC is <strong>{cac_ratio:.1f}x</strong> the average order value (${avg_aov:.2f})</p>
            <p>{"Excellent" if cac_ratio < 0.3 else "Good" if cac_ratio < 0.5 else "Needs optimization"} customer acquisition efficiency.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
 #   st.markdown("Built with ❤️ using Streamlit | Data refreshes automatically")

if __name__ == "__main__":
    main()