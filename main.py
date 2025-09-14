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
    
    # Geographic Performance Analysis
    st.header("🌍 Geographic Performance Analysis")
    
    # Check if state data is available
    if 'state' in filtered_marketing.columns and filtered_marketing['state'].notna().any():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # State-level performance metrics
            state_metrics = filtered_marketing.groupby('state').agg({
                'impressions': 'sum',
                'clicks': 'sum',
                'spend': 'sum',
                'attributed_revenue': 'sum'
            }).reset_index()
            
            state_metrics['CTR'] = (state_metrics['clicks'] / state_metrics['impressions'] * 100).round(2)
            state_metrics['ROAS'] = (state_metrics['attributed_revenue'] / state_metrics['spend']).round(2)
            state_metrics['Efficiency'] = (state_metrics['attributed_revenue'] / state_metrics['spend']).round(2)
            
            # Geographic performance chart
            fig_geo = px.bar(
                state_metrics.sort_values('attributed_revenue', ascending=False).head(10),
                x='state',
                y='attributed_revenue',
                title="Top 10 States by Revenue Attribution",
                labels={'attributed_revenue': 'Revenue ($)', 'state': 'State'},
                color='ROAS',
                color_continuous_scale='Viridis'
            )
            fig_geo.update_layout(height=400)
            st.plotly_chart(fig_geo, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Top Performing States")
            
            # Top 5 states by ROAS
            top_states = state_metrics.nlargest(5, 'ROAS')[['state', 'ROAS', 'attributed_revenue', 'spend']]
            
            for _, state in top_states.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{state['state']}</h4>
                    <p><strong>ROAS:</strong> {state['ROAS']:.2f}x</p>
                    <p><strong>Revenue:</strong> ${state['attributed_revenue']:,.0f}</p>
                    <p><strong>Spend:</strong> ${state['spend']:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Geographic insights
            best_state = state_metrics.loc[state_metrics['ROAS'].idxmax(), 'state']
            worst_state = state_metrics.loc[state_metrics['ROAS'].idxmin(), 'state']
            total_states = len(state_metrics)
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>🎯 Geographic Insights</h4>
                <p><strong>{best_state}</strong> is the top performing state</p>
                <p>Active in <strong>{total_states}</strong> states/regions</p>
                <p>Consider expanding budget in high-ROAS regions</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📍 Geographic data not available in current dataset")
    
    # Marketing Funnel Analysis
    st.header("🔄 Marketing Funnel Analysis")
    
    try:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Calculate funnel metrics
            total_impressions = filtered_marketing['impressions'].sum()
            total_clicks = filtered_marketing['clicks'].sum()
            total_attributed_revenue = filtered_marketing['attributed_revenue'].sum()
            
            # Estimate conversions (assuming average order value)
            avg_aov = filtered_combined['aov'].mean() if 'aov' in filtered_combined.columns else 100
            estimated_conversions = total_attributed_revenue / avg_aov if avg_aov > 0 else 0
            
            # Calculate conversion rates
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            conversion_rate = (estimated_conversions / total_clicks * 100) if total_clicks > 0 else 0
            
            # Only proceed if we have valid data
            if total_impressions > 0 and total_clicks > 0:
                # Funnel visualization using bar chart (more compatible)
                funnel_data = pd.DataFrame({
                    'Stage': ['Impressions', 'Clicks', 'Conversions'],
                    'Count': [total_impressions, total_clicks, estimated_conversions],
                    'Conversion_Rate': [100, ctr, conversion_rate]
                })
                
                # Create a horizontal bar chart that looks like a funnel
                fig_funnel = px.bar(
                    funnel_data,
                    x='Count',
                    y='Stage',
                    orientation='h',
                    title="Marketing Funnel Performance",
                    color='Conversion_Rate',
                    color_continuous_scale='RdYlGn',
                    text='Count'
                )
                
                # Format the text on bars
                fig_funnel.update_traces(
                    texttemplate='%{text:,.0f} (%{customdata:.1f}%)',
                    customdata=funnel_data['Conversion_Rate'],
                    textposition="inside"
                )
                
                fig_funnel.update_layout(
                    height=400,
                    yaxis={'categoryorder': 'array', 'categoryarray': ['Conversions', 'Clicks', 'Impressions']}
                )
                st.plotly_chart(fig_funnel, use_container_width=True)
                
                # Funnel metrics by channel
                st.subheader("📊 Channel Funnel Comparison")
                
                channel_funnel = filtered_marketing.groupby('channel').agg({
                    'impressions': 'sum',
                    'clicks': 'sum',
                    'attributed_revenue': 'sum'
                }).reset_index()
                
                channel_funnel['CTR'] = (channel_funnel['clicks'] / channel_funnel['impressions'] * 100).round(2)
                channel_funnel['Est_Conversions'] = (channel_funnel['attributed_revenue'] / avg_aov).round(0)
                channel_funnel['CVR'] = (channel_funnel['Est_Conversions'] / channel_funnel['clicks'] * 100).round(2)
                
                # Format for display
                funnel_display = channel_funnel.copy()
                funnel_display['Impressions'] = funnel_display['impressions'].apply(lambda x: f"{x:,}")
                funnel_display['Clicks'] = funnel_display['clicks'].apply(lambda x: f"{x:,}")
                funnel_display['Conversions'] = funnel_display['Est_Conversions'].apply(lambda x: f"{x:,.0f}")
                
                st.dataframe(
                    funnel_display[['channel', 'Impressions', 'Clicks', 'CTR', 'Conversions', 'CVR']],
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Insufficient data for funnel analysis")
        
        with col2:
            st.subheader("⚡ Funnel Insights")
            
            if total_impressions > 0 and total_clicks > 0:
                # Overall funnel performance
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Overall Funnel Performance</h4>
                    <p><strong>Click-Through Rate:</strong> {ctr:.2f}%</p>
                    <p><strong>Conversion Rate:</strong> {conversion_rate:.2f}%</p>
                    <p><strong>Overall Conversion:</strong> {(estimated_conversions/total_impressions*100):.3f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Best performing channel in funnel
                if len(filtered_marketing) > 0 and 'channel' in filtered_marketing.columns:
                    channel_funnel = filtered_marketing.groupby('channel').agg({
                        'impressions': 'sum',
                        'clicks': 'sum',
                        'attributed_revenue': 'sum'
                    }).reset_index()
                    
                    channel_funnel['CTR'] = (channel_funnel['clicks'] / channel_funnel['impressions'] * 100).round(2)
                    channel_funnel['CVR'] = ((channel_funnel['attributed_revenue'] / avg_aov) / channel_funnel['clicks'] * 100).round(2)
                    
                    if len(channel_funnel) > 0:
                        best_ctr_channel = channel_funnel.loc[channel_funnel['CTR'].idxmax(), 'channel']
                        best_cvr_channel = channel_funnel.loc[channel_funnel['CVR'].idxmax(), 'channel']
                        
                        st.markdown(f"""
                        <div class="insight-card">
                            <h4>🎯 Funnel Optimization</h4>
                            <p><strong>{best_ctr_channel}</strong> has the best CTR</p>
                            <p><strong>{best_cvr_channel}</strong> has the best conversion rate</p>
                            <p>Focus on improving conversion rates for better ROI</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Improvement opportunities
                        worst_ctr = channel_funnel['CTR'].min()
                        worst_cvr = channel_funnel['CVR'].min()
                        
                        st.markdown(f"""
                        <div class="insight-card">
                            <h4>📈 Improvement Opportunities</h4>
                            <p>Lowest CTR: {worst_ctr:.2f}% - optimize ad creative</p>
                            <p>Lowest CVR: {worst_cvr:.2f}% - improve landing pages</p>
                            <p>Focus on weak points in the funnel</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📊 Need data for funnel insights")
                
    except Exception as e:
        st.error(f"Error in funnel analysis: {str(e)}")
        st.info("📊 Funnel analysis temporarily unavailable")
    
    # Seasonality & Time Analysis
    st.header("📅 Seasonality & Time Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Day of week analysis
        if len(filtered_combined) > 7:
            # Add day of week to the data
            filtered_combined_copy = filtered_combined.copy()
            filtered_combined_copy['day_of_week'] = pd.to_datetime(filtered_combined_copy['date']).dt.day_name()
            filtered_combined_copy['week_day'] = pd.to_datetime(filtered_combined_copy['date']).dt.weekday
            
            # Group by day of week
            dow_performance = filtered_combined_copy.groupby(['day_of_week', 'week_day']).agg({
                'total_revenue': 'mean',
                'spend': 'mean',
                'new_customers': 'mean'
            }).reset_index().sort_values('week_day')
            
            # Day of week revenue pattern
            fig_dow = px.bar(
                dow_performance,
                x='day_of_week',
                y='total_revenue',
                title="Average Daily Revenue by Day of Week",
                labels={'total_revenue': 'Avg Revenue ($)', 'day_of_week': 'Day of Week'},
                color='total_revenue',
                color_continuous_scale='Blues'
            )
            fig_dow.update_layout(height=300)
            st.plotly_chart(fig_dow, use_container_width=True)
            
            # Weekly trends over time
            if len(filtered_combined) > 14:
                filtered_combined_copy['week'] = pd.to_datetime(filtered_combined_copy['date']).dt.isocalendar().week
                filtered_combined_copy['month'] = pd.to_datetime(filtered_combined_copy['date']).dt.month
                
                weekly_trends = filtered_combined_copy.groupby('week').agg({
                    'total_revenue': 'sum',
                    'spend': 'sum',
                    'marketing_efficiency': 'mean'
                }).reset_index()
                
                fig_weekly = px.line(
                    weekly_trends,
                    x='week',
                    y=['total_revenue', 'spend'],
                    title="Weekly Revenue and Spend Trends",
                    labels={'value': 'Amount ($)', 'week': 'Week of Year'}
                )
                fig_weekly.update_layout(height=300)
                st.plotly_chart(fig_weekly, use_container_width=True)
        else:
            st.info("📊 Need more data points for detailed seasonality analysis")
    
    with col2:
        st.subheader("⏰ Time Insights")
        
        if len(filtered_combined) > 7:
            # Best and worst performing days
            best_day = dow_performance.loc[dow_performance['total_revenue'].idxmax(), 'day_of_week']
            worst_day = dow_performance.loc[dow_performance['total_revenue'].idxmin(), 'day_of_week']
            best_revenue = dow_performance['total_revenue'].max()
            worst_revenue = dow_performance['total_revenue'].min()
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>📈 Best Performance Day</h4>
                <p><strong>{best_day}</strong></p>
                <p>Avg Revenue: ${best_revenue:,.0f}</p>
                <p>{((best_revenue/worst_revenue-1)*100):+.1f}% vs worst day</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Weekend vs Weekday performance
            weekend_revenue = dow_performance[dow_performance['week_day'].isin([5, 6])]['total_revenue'].mean()
            weekday_revenue = dow_performance[~dow_performance['week_day'].isin([5, 6])]['total_revenue'].mean()
            
            weekend_better = weekend_revenue > weekday_revenue
            difference = abs(weekend_revenue - weekday_revenue)
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>🗓️ Weekend vs Weekday</h4>
                <p><strong>{"Weekend" if weekend_better else "Weekday"}</strong> performs better</p>
                <p>Difference: ${difference:,.0f} avg daily revenue</p>
                <p>{"Focus weekend campaigns" if weekend_better else "Optimize weekday strategy"}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Month-over-month growth (if enough data)
            if len(filtered_combined) > 30:
                filtered_combined_copy['month'] = pd.to_datetime(filtered_combined_copy['date']).dt.month
                monthly_revenue = filtered_combined_copy.groupby('month')['total_revenue'].sum()
                
                if len(monthly_revenue) >= 2:
                    recent_month = monthly_revenue.iloc[-1]
                    previous_month = monthly_revenue.iloc[-2]
                    growth = ((recent_month - previous_month) / previous_month * 100) if previous_month > 0 else 0
                    
                    st.markdown(f"""
                    <div class="insight-card">
                        <h4>📊 Month-over-Month</h4>
                        <p>Revenue Growth: <strong>{growth:+.1f}%</strong></p>
                        <p>Latest: ${recent_month:,.0f}</p>
                        <p>Previous: ${previous_month:,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("📅 Need more historical data for time-based insights")
    
    # Enhanced Customer Metrics
    st.header("👥 Enhanced Customer Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Customer Acquisition Trends")
        
        # Customer acquisition by channel
        if len(filtered_combined) > 1:
            # Calculate customer acquisition metrics
            daily_customers = filtered_combined.groupby('date').agg({
                'new_customers': 'sum',
                'spend': 'sum',
                'total_revenue': 'sum'
            }).reset_index()
            
            daily_customers['cac'] = daily_customers['spend'] / daily_customers['new_customers']
            daily_customers['cac'] = daily_customers['cac'].replace([np.inf, -np.inf], 0)
            
            # Rolling average CAC
            daily_customers['cac_7day_avg'] = daily_customers['cac'].rolling(window=7, min_periods=1).mean()
            
            fig_cac = px.line(
                daily_customers,
                x='date',
                y=['cac', 'cac_7day_avg'],
                title="Customer Acquisition Cost Trend",
                labels={'value': 'CAC ($)', 'date': 'Date'}
            )
            fig_cac.update_layout(height=300)
            st.plotly_chart(fig_cac, use_container_width=True)
            
            # Customer acquisition efficiency by period
            if len(daily_customers) >= 14:
                recent_period = daily_customers.tail(7)
                previous_period = daily_customers.iloc[-14:-7] if len(daily_customers) >= 14 else daily_customers.head(7)
                
                recent_cac = recent_period['cac'].mean()
                previous_cac = previous_period['cac'].mean()
                cac_change = ((recent_cac - previous_cac) / previous_cac * 100) if previous_cac > 0 else 0
                
                recent_customers = recent_period['new_customers'].sum()
                previous_customers = previous_period['new_customers'].sum()
                customer_change = ((recent_customers - previous_customers) / previous_customers * 100) if previous_customers > 0 else 0
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Recent vs Previous Week</h4>
                    <p><strong>CAC Change:</strong> {cac_change:+.1f}%</p>
                    <p><strong>Customer Growth:</strong> {customer_change:+.1f}%</p>
                    <p><strong>Current CAC:</strong> ${recent_cac:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💰 Revenue & Efficiency Metrics")
        
        # Calculate customer lifetime value indicators
        if len(filtered_combined) > 1:
            avg_order_value = filtered_combined['aov'].mean() if 'aov' in filtered_combined.columns else (filtered_combined['total_revenue'].sum() / filtered_combined['orders'].sum())
            total_customers = filtered_combined['new_customers'].sum()
            total_revenue = filtered_combined['total_revenue'].sum()
            
            # Estimated customer value metrics
            revenue_per_customer = total_revenue / total_customers if total_customers > 0 else 0
            marketing_efficiency = total_revenue / filtered_marketing['spend'].sum() if filtered_marketing['spend'].sum() > 0 else 0
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>💎 Customer Value Metrics</h4>
                <p><strong>Avg Order Value:</strong> ${avg_order_value:.2f}</p>
                <p><strong>Revenue per Customer:</strong> ${revenue_per_customer:.2f}</p>
                <p><strong>Marketing Efficiency:</strong> {marketing_efficiency:.2f}x</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Channel efficiency comparison
            channel_efficiency = filtered_marketing.groupby('channel').agg({
                'spend': 'sum',
                'attributed_revenue': 'sum'
            })
            channel_efficiency['efficiency'] = channel_efficiency['attributed_revenue'] / channel_efficiency['spend']
            best_channel_eff = channel_efficiency['efficiency'].idxmax()
            best_efficiency = channel_efficiency['efficiency'].max()
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>⚡ Channel Efficiency</h4>
                <p><strong>{best_channel_eff}</strong> is most efficient</p>
                <p>Efficiency: {best_efficiency:.2f}x revenue per dollar</p>
                <p>Focus budget on high-efficiency channels</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Growth opportunities
            low_efficiency_channels = channel_efficiency[channel_efficiency['efficiency'] < channel_efficiency['efficiency'].median()]
            
            if len(low_efficiency_channels) > 0:
                worst_channel = low_efficiency_channels['efficiency'].idxmin()
                improvement_potential = (best_efficiency - low_efficiency_channels.loc[worst_channel, 'efficiency']) / low_efficiency_channels.loc[worst_channel, 'efficiency'] * 100
                
                st.markdown(f"""
                <div class="insight-card">
                    <h4>🚀 Improvement Opportunity</h4>
                    <p><strong>{worst_channel}</strong> has {improvement_potential:.0f}% improvement potential</p>
                    <p>Optimize targeting and creative for better efficiency</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📊 Need more data for detailed customer metrics")
    
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