"""
Quick test to verify the real data loading works correctly
"""
import pandas as pd
import sys
import os

def test_data_loading():
    print("🧪 Testing Real Data Loading...")
    
    try:
        # Load Facebook data
        facebook_df = pd.read_csv('data/Facebook.csv')
        print(f"✅ Facebook data loaded: {len(facebook_df)} rows")
        print(f"📊 Facebook columns: {list(facebook_df.columns)}")
        print(f"📅 Facebook date range: {facebook_df['date'].min()} to {facebook_df['date'].max()}")
        
        # Load Google data
        google_df = pd.read_csv('data/Google.csv')
        print(f"✅ Google data loaded: {len(google_df)} rows")
        print(f"📊 Google columns: {list(google_df.columns)}")
        
        # Load TikTok data
        tiktok_df = pd.read_csv('data/TikTok.csv')
        print(f"✅ TikTok data loaded: {len(tiktok_df)} rows")
        print(f"📊 TikTok columns: {list(tiktok_df.columns)}")
        
        # Load Business data
        business_df = pd.read_csv('data/business.csv')
        print(f"✅ Business data loaded: {len(business_df)} rows")
        print(f"📊 Business columns: {list(business_df.columns)}")
        
        # Test data processing
        # Standardize column names
        marketing_column_mapping = {
            'impression': 'impressions',
            'attributed revenue': 'attributed_revenue'
        }
        
        for df in [facebook_df, google_df, tiktok_df]:
            df.rename(columns=marketing_column_mapping, inplace=True)
        
        # Add channel identifier
        facebook_df['channel'] = 'Facebook'
        google_df['channel'] = 'Google'
        tiktok_df['channel'] = 'TikTok'
        
        # Combine marketing data
        marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        print(f"✅ Combined marketing data: {len(marketing_df)} rows")
        
        # Check for required columns
        required_cols = ['date', 'channel', 'campaign', 'impressions', 'clicks', 'spend', 'attributed_revenue']
        missing_cols = [col for col in required_cols if col not in marketing_df.columns]
        if missing_cols:
            print(f"⚠️  Missing columns: {missing_cols}")
        else:
            print("✅ All required columns present")
        
        # Sample statistics
        total_spend = marketing_df['spend'].sum()
        total_revenue = marketing_df['attributed_revenue'].sum()
        overall_roas = total_revenue / total_spend if total_spend > 0 else 0
        
        print(f"\n📈 Key Metrics:")
        print(f"💰 Total Spend: ${total_spend:,.2f}")
        print(f"💰 Total Attributed Revenue: ${total_revenue:,.2f}")
        print(f"📊 Overall ROAS: {overall_roas:.2f}x")
        print(f"📅 Date Range: {marketing_df['date'].min()} to {marketing_df['date'].max()}")
        
        # Channel breakdown
        print(f"\n🎯 Channel Breakdown:")
        channel_summary = marketing_df.groupby('channel').agg({
            'spend': 'sum',
            'attributed_revenue': 'sum'
        })
        channel_summary['roas'] = channel_summary['attributed_revenue'] / channel_summary['spend']
        
        for channel in channel_summary.index:
            spend = channel_summary.loc[channel, 'spend']
            revenue = channel_summary.loc[channel, 'attributed_revenue']
            roas = channel_summary.loc[channel, 'roas']
            print(f"  {channel}: ${spend:,.0f} spend → ${revenue:,.0f} revenue (ROAS: {roas:.2f}x)")
        
        print(f"\n🎉 Data loading test successful! Your dashboard is ready with real data.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_data_loading()