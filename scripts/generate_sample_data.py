import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample data for testing the dashboard"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate 120 days of data
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(120)]
    
    # Campaign names and tactics
    facebook_campaigns = ['FB_Brand_Awareness', 'FB_Conversion', 'FB_Retargeting', 'FB_Lookalike']
    google_campaigns = ['Google_Search_Brand', 'Google_Search_Generic', 'Google_Display', 'Google_Shopping']
    tiktok_campaigns = ['TT_Video_Ads', 'TT_Spark_Ads', 'TT_Brand_Takeover']
    
    tactics = ['Video', 'Image', 'Carousel', 'Text', 'Shopping']
    states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'MI', 'GA', 'NC']
    
    # Generate Facebook data
    facebook_data = []
    for date in dates:
        for campaign in facebook_campaigns:
            # Skip some days randomly to simulate real-world gaps
            if random.random() < 0.1:
                continue
                
            impressions = np.random.exponential(5000)
            ctr = np.random.normal(0.015, 0.005)  # 1.5% average CTR
            clicks = int(impressions * max(0.001, ctr))
            cpc = np.random.normal(0.8, 0.3)  # $0.80 average CPC
            spend = clicks * max(0.1, cpc)
            
            # Revenue attribution (ROAS varies by campaign type)
            if 'Conversion' in campaign:
                roas = np.random.normal(4.0, 1.0)
            elif 'Retargeting' in campaign:
                roas = np.random.normal(6.0, 1.5)
            else:
                roas = np.random.normal(2.5, 0.8)
            
            attributed_revenue = spend * max(0.5, roas)
            
            facebook_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'tactic': random.choice(tactics),
                'state': random.choice(states),
                'campaign': campaign,
                'impressions': int(impressions),
                'clicks': clicks,
                'spend': round(spend, 2),
                'attributed_revenue': round(attributed_revenue, 2)
            })
    
    # Generate Google data
    google_data = []
    for date in dates:
        for campaign in google_campaigns:
            if random.random() < 0.1:
                continue
                
            impressions = np.random.exponential(3000)
            ctr = np.random.normal(0.025, 0.008)  # Higher CTR for search
            clicks = int(impressions * max(0.001, ctr))
            
            # CPC varies by campaign type
            if 'Search' in campaign:
                cpc = np.random.normal(1.2, 0.4)
            else:
                cpc = np.random.normal(0.6, 0.2)
                
            spend = clicks * max(0.1, cpc)
            
            # Google typically has higher ROAS
            if 'Brand' in campaign:
                roas = np.random.normal(8.0, 2.0)
            elif 'Shopping' in campaign:
                roas = np.random.normal(5.0, 1.5)
            else:
                roas = np.random.normal(3.5, 1.0)
            
            attributed_revenue = spend * max(0.5, roas)
            
            google_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'tactic': random.choice(tactics),
                'state': random.choice(states),
                'campaign': campaign,
                'impressions': int(impressions),
                'clicks': clicks,
                'spend': round(spend, 2),
                'attributed_revenue': round(attributed_revenue, 2)
            })
    
    # Generate TikTok data
    tiktok_data = []
    for date in dates:
        for campaign in tiktok_campaigns:
            if random.random() < 0.15:  # TikTok has more gaps
                continue
                
            impressions = np.random.exponential(8000)  # Higher impressions
            ctr = np.random.normal(0.02, 0.006)
            clicks = int(impressions * max(0.001, ctr))
            cpc = np.random.normal(0.5, 0.2)  # Lower CPC
            spend = clicks * max(0.1, cpc)
            
            # TikTok ROAS varies more
            roas = np.random.normal(3.0, 1.5)
            attributed_revenue = spend * max(0.5, roas)
            
            tiktok_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'tactic': random.choice(['Video', 'Image']),  # Mainly video platform
                'state': random.choice(states),
                'campaign': campaign,
                'impressions': int(impressions),
                'clicks': clicks,
                'spend': round(spend, 2),
                'attributed_revenue': round(attributed_revenue, 2)
            })
    
    # Generate Business data
    business_data = []
    for i, date in enumerate(dates):
        # Base business metrics with trends and seasonality
        base_orders = 150 + (i * 0.5) + np.random.normal(0, 20)  # Growing trend
        
        # Add weekly seasonality (higher on weekends)
        day_of_week = date.weekday()
        if day_of_week >= 5:  # Weekend
            base_orders *= 1.3
        elif day_of_week == 0:  # Monday
            base_orders *= 0.8
            
        orders = max(50, int(base_orders))
        new_orders_ratio = np.random.uniform(0.6, 0.8)
        new_orders = int(orders * new_orders_ratio)
        
        # New customers (slightly less than new orders)
        new_customers = int(new_orders * np.random.uniform(0.85, 0.95))
        
        # Revenue metrics
        aov = np.random.normal(85, 15)  # $85 average order value
        total_revenue = orders * max(50, aov)
        
        # Profit margins
        gross_margin = np.random.normal(0.4, 0.05)  # 40% margin
        gross_profit = total_revenue * max(0.2, gross_margin)
        cogs = total_revenue - gross_profit
        
        business_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'orders': orders,
            'new_orders': new_orders,
            'new_customers': new_customers,
            'total_revenue': round(total_revenue, 2),
            'gross_profit': round(gross_profit, 2),
            'cogs': round(cogs, 2)
        })
    
    # Save to CSV files
    pd.DataFrame(facebook_data).to_csv('data/Facebook.csv', index=False)
    pd.DataFrame(google_data).to_csv('data/Google.csv', index=False)
    pd.DataFrame(tiktok_data).to_csv('data/TikTok.csv', index=False)
    pd.DataFrame(business_data).to_csv('data/Business.csv', index=False)
    
    print("✅ Sample data generated successfully!")
    print(f"Facebook: {len(facebook_data)} records")
    print(f"Google: {len(google_data)} records")
    print(f"TikTok: {len(tiktok_data)} records")
    print(f"Business: {len(business_data)} records")

if __name__ == "__main__":
    generate_sample_data()