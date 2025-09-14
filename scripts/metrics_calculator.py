import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MetricsCalculator:
    """
    Calculates key performance indicators and business metrics for the dashboard
    """
    
    def __init__(self, marketing_data, business_data, combined_data):
        self.marketing_data = marketing_data
        self.business_data = business_data
        self.combined_data = combined_data
    
    def calculate_channel_metrics(self):
        """Calculate key metrics by marketing channel"""
        channel_metrics = self.marketing_data.groupby('channel').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'spend': 'sum',
            'attributed_revenue': 'sum',
            'date': 'count'  # Number of active days
        }).rename(columns={'date': 'active_days'})
        
        # Calculate derived metrics
        channel_metrics['ctr'] = (channel_metrics['clicks'] / channel_metrics['impressions'] * 100).round(2)
        channel_metrics['cpc'] = (channel_metrics['spend'] / channel_metrics['clicks']).round(2)
        channel_metrics['roas'] = (channel_metrics['attributed_revenue'] / channel_metrics['spend']).round(2)
        channel_metrics['avg_daily_spend'] = (channel_metrics['spend'] / channel_metrics['active_days']).round(2)
        
        return channel_metrics
    
    def calculate_campaign_metrics(self):
        """Calculate metrics by campaign"""
        campaign_metrics = self.marketing_data.groupby(['channel', 'campaign']).agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'spend': 'sum',
            'attributed_revenue': 'sum',
            'date': 'count'
        }).rename(columns={'date': 'active_days'})
        
        # Calculate derived metrics
        campaign_metrics['ctr'] = (campaign_metrics['clicks'] / campaign_metrics['impressions'] * 100).round(2)
        campaign_metrics['cpc'] = (campaign_metrics['spend'] / campaign_metrics['clicks']).round(2)
        campaign_metrics['roas'] = (campaign_metrics['attributed_revenue'] / campaign_metrics['spend']).round(2)
        
        return campaign_metrics.reset_index()
    
    def calculate_business_kpis(self):
        """Calculate key business performance indicators"""
        business_summary = {
            'total_revenue': self.business_data['total_revenue'].sum(),
            'total_orders': self.business_data['orders'].sum(),
            'total_new_customers': self.business_data['new_customers'].sum(),
            'avg_aov': self.business_data['total_revenue'].sum() / self.business_data['orders'].sum(),
            'avg_daily_revenue': self.business_data['total_revenue'].mean(),
            'avg_daily_orders': self.business_data['orders'].mean(),
            'total_gross_profit': self.business_data['gross_profit'].sum(),
            'avg_gross_margin': (self.business_data['gross_profit'].sum() / 
                               self.business_data['total_revenue'].sum() * 100)
        }
        
        # Marketing efficiency metrics
        total_marketing_spend = self.marketing_data['spend'].sum()
        total_attributed_revenue = self.marketing_data['attributed_revenue'].sum()
        
        business_summary.update({
            'total_marketing_spend': total_marketing_spend,
            'overall_roas': total_attributed_revenue / total_marketing_spend if total_marketing_spend > 0 else 0,
            'marketing_efficiency': (self.business_data['total_revenue'].sum() / 
                                   total_marketing_spend if total_marketing_spend > 0 else 0),
            'customer_acquisition_cost': (total_marketing_spend / 
                                        self.business_data['new_customers'].sum() 
                                        if self.business_data['new_customers'].sum() > 0 else 0)
        })
        
        return business_summary
    
    def calculate_time_series_metrics(self, period='daily'):
        """Calculate metrics over time"""
        if period == 'daily':
            time_series = self.combined_data.copy()
        elif period == 'weekly':
            time_series = self.combined_data.copy()
            time_series['week'] = time_series['date'].dt.isocalendar().week
            time_series = time_series.groupby('week').agg({
                'total_revenue': 'sum',
                'orders': 'sum',
                'new_customers': 'sum',
                'spend': 'sum',
                'attributed_revenue': 'sum',
                'impressions': 'sum',
                'clicks': 'sum'
            })
        
        # Calculate rolling averages
        time_series['revenue_7d_avg'] = time_series['total_revenue'].rolling(7).mean()
        time_series['spend_7d_avg'] = time_series['spend'].rolling(7).mean()
        time_series['roas_7d_avg'] = (time_series['attributed_revenue'].rolling(7).sum() / 
                                     time_series['spend'].rolling(7).sum())
        
        return time_series
    
    def identify_top_performers(self):
        """Identify top performing campaigns and channels"""
        # Top campaigns by ROAS
        campaign_metrics = self.calculate_campaign_metrics()
        top_campaigns_roas = campaign_metrics.nlargest(5, 'roas')[['channel', 'campaign', 'roas', 'spend']]
        
        # Top campaigns by revenue
        top_campaigns_revenue = campaign_metrics.nlargest(5, 'attributed_revenue')[
            ['channel', 'campaign', 'attributed_revenue', 'spend']
        ]
        
        # Most efficient campaigns (revenue per spend)
        campaign_metrics['efficiency'] = campaign_metrics['attributed_revenue'] / campaign_metrics['spend']
        top_efficient_campaigns = campaign_metrics.nlargest(5, 'efficiency')[
            ['channel', 'campaign', 'efficiency', 'spend']
        ]
        
        return {
            'top_roas': top_campaigns_roas,
            'top_revenue': top_campaigns_revenue,
            'most_efficient': top_efficient_campaigns
        }
    
    def calculate_correlation_analysis(self):
        """Analyze correlations between marketing and business metrics"""
        correlation_data = self.combined_data[[
            'spend', 'impressions', 'clicks', 'attributed_revenue',
            'total_revenue', 'orders', 'new_customers', 'gross_profit'
        ]].corr()
        
        # Key correlations to highlight
        key_correlations = {
            'spend_vs_revenue': correlation_data.loc['spend', 'total_revenue'],
            'spend_vs_orders': correlation_data.loc['spend', 'orders'],
            'impressions_vs_revenue': correlation_data.loc['impressions', 'total_revenue'],
            'attributed_revenue_vs_actual_revenue': correlation_data.loc['attributed_revenue', 'total_revenue']
        }
        
        return correlation_data, key_correlations
    
    def generate_insights(self):
        """Generate automated insights based on data analysis"""
        insights = []
        
        # Channel performance insights
        channel_metrics = self.calculate_channel_metrics()
        best_channel = channel_metrics['roas'].idxmax()
        best_roas = channel_metrics['roas'].max()
        
        insights.append({
            'type': 'channel_performance',
            'title': f'{best_channel} is the Top Performing Channel',
            'description': f'{best_channel} delivers the highest ROAS at {best_roas:.2f}x',
            'metric': 'ROAS',
            'value': best_roas
        })
        
        # Spend efficiency insight
        total_spend = self.marketing_data['spend'].sum()
        total_revenue = self.business_data['total_revenue'].sum()
        overall_efficiency = total_revenue / total_spend
        
        insights.append({
            'type': 'efficiency',
            'title': 'Marketing Efficiency',
            'description': f'Every $1 spent on marketing generates ${overall_efficiency:.2f} in total revenue',
            'metric': 'Revenue per $ spent',
            'value': overall_efficiency
        })
        
        # Growth trend insight
        recent_data = self.combined_data.tail(30)  # Last 30 days
        early_data = self.combined_data.head(30)   # First 30 days
        
        recent_avg_revenue = recent_data['total_revenue'].mean()
        early_avg_revenue = early_data['total_revenue'].mean()
        revenue_growth = ((recent_avg_revenue - early_avg_revenue) / early_avg_revenue) * 100
        
        trend_direction = "increasing" if revenue_growth > 0 else "decreasing"
        insights.append({
            'type': 'trend',
            'title': f'Revenue Trend is {trend_direction.title()}',
            'description': f'Daily revenue has changed by {revenue_growth:.1f}% over the period',
            'metric': 'Revenue Growth',
            'value': revenue_growth
        })
        
        # Customer acquisition insight
        avg_cac = self.calculate_business_kpis()['customer_acquisition_cost']
        avg_aov = self.calculate_business_kpis()['avg_aov']
        cac_to_aov_ratio = avg_cac / avg_aov
        
        insights.append({
            'type': 'customer_acquisition',
            'title': 'Customer Acquisition Efficiency',
            'description': f'Customer acquisition cost (${avg_cac:.2f}) is {cac_to_aov_ratio:.1f}x the average order value',
            'metric': 'CAC to AOV Ratio',
            'value': cac_to_aov_ratio
        })
        
        return insights
    
    def get_all_metrics(self):
        """Get comprehensive metrics summary"""
        return {
            'channel_metrics': self.calculate_channel_metrics(),
            'campaign_metrics': self.calculate_campaign_metrics(),
            'business_kpis': self.calculate_business_kpis(),
            'time_series': self.calculate_time_series_metrics(),
            'top_performers': self.identify_top_performers(),
            'correlations': self.calculate_correlation_analysis(),
            'insights': self.generate_insights()
        }