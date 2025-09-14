import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """
    Handles data loading, cleaning, and preparation for the marketing intelligence dashboard
    """
    
    def __init__(self, data_path="data/"):
        self.data_path = data_path
        self.marketing_data = None
        self.business_data = None
        self.combined_data = None
        
    def load_data(self):
        """Load all CSV files and perform initial validation"""
        try:
            # Load marketing data
            facebook_df = pd.read_csv(f"{self.data_path}Facebook.csv")
            google_df = pd.read_csv(f"{self.data_path}Google.csv")
            tiktok_df = pd.read_csv(f"{self.data_path}TikTok.csv")
            
            # Add channel identifier
            facebook_df['channel'] = 'Facebook'
            google_df['channel'] = 'Google'
            tiktok_df['channel'] = 'TikTok'
            
            # Combine marketing data
            self.marketing_data = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
            
            # Load business data
            self.business_data = pd.read_csv(f"{self.data_path}Business.csv")
            
            print(f"✅ Data loaded successfully!")
            print(f"Marketing data: {len(self.marketing_data)} rows")
            print(f"Business data: {len(self.business_data)} rows")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error loading data: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def clean_marketing_data(self):
        """Clean and standardize marketing data"""
        if self.marketing_data is None:
            raise ValueError("Marketing data not loaded. Call load_data() first.")
        
        # Convert date column
        self.marketing_data['date'] = pd.to_datetime(self.marketing_data['date'])
        
        # Clean numeric columns
        numeric_cols = ['impressions', 'clicks', 'spend', 'attributed_revenue']
        for col in numeric_cols:
            if col in self.marketing_data.columns:
                self.marketing_data[col] = pd.to_numeric(self.marketing_data[col], errors='coerce').fillna(0)
        
        # Handle missing values
        text_cols = ['tactic', 'state', 'campaign']
        for col in text_cols:
            if col in self.marketing_data.columns:
                self.marketing_data[col] = self.marketing_data[col].fillna('Unknown')
        
        # Create derived metrics
        self.marketing_data['ctr'] = np.where(
            self.marketing_data['impressions'] > 0,
            self.marketing_data['clicks'] / self.marketing_data['impressions'] * 100,
            0
        )
        
        self.marketing_data['cpc'] = np.where(
            self.marketing_data['clicks'] > 0,
            self.marketing_data['spend'] / self.marketing_data['clicks'],
            0
        )
        
        self.marketing_data['roas'] = np.where(
            self.marketing_data['spend'] > 0,
            self.marketing_data['attributed_revenue'] / self.marketing_data['spend'],
            0
        )
        
        print("✅ Marketing data cleaned and enriched")
        
    def clean_business_data(self):
        """Clean and standardize business data"""
        if self.business_data is None:
            raise ValueError("Business data not loaded. Call load_data() first.")
        
        # Convert date column
        self.business_data['date'] = pd.to_datetime(self.business_data['date'])
        
        # Clean numeric columns
        numeric_cols = ['orders', 'new_orders', 'new_customers', 'total_revenue', 'gross_profit', 'cogs']
        for col in numeric_cols:
            if col in self.business_data.columns:
                self.business_data[col] = pd.to_numeric(self.business_data[col], errors='coerce').fillna(0)
        
        # Create derived metrics
        self.business_data['aov'] = np.where(
            self.business_data['orders'] > 0,
            self.business_data['total_revenue'] / self.business_data['orders'],
            0
        )
        
        self.business_data['gross_margin'] = np.where(
            self.business_data['total_revenue'] > 0,
            self.business_data['gross_profit'] / self.business_data['total_revenue'] * 100,
            0
        )
        
        self.business_data['repeat_orders'] = (
            self.business_data['orders'] - self.business_data['new_orders']
        )
        
        print("✅ Business data cleaned and enriched")
    
    def aggregate_marketing_data(self):
        """Aggregate marketing data by date for joining with business data"""
        daily_marketing = self.marketing_data.groupby('date').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'spend': 'sum',
            'attributed_revenue': 'sum'
        }).reset_index()
        
        # Recalculate metrics at daily level
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
        
        return daily_marketing
    
    def combine_data(self):
        """Combine marketing and business data"""
        daily_marketing = self.aggregate_marketing_data()
        
        # Merge on date
        self.combined_data = pd.merge(
            self.business_data,
            daily_marketing,
            on='date',
            how='left'
        )
        
        # Fill NaN values for days with no marketing activity
        marketing_cols = ['impressions', 'clicks', 'spend', 'attributed_revenue', 'ctr', 'cpc', 'roas']
        for col in marketing_cols:
            self.combined_data[col] = self.combined_data[col].fillna(0)
        
        # Create additional metrics
        self.combined_data['marketing_efficiency'] = np.where(
            self.combined_data['spend'] > 0,
            self.combined_data['total_revenue'] / self.combined_data['spend'],
            0
        )
        
        self.combined_data['cpa'] = np.where(
            self.combined_data['new_customers'] > 0,
            self.combined_data['spend'] / self.combined_data['new_customers'],
            0
        )
        
        print("✅ Data combined successfully")
        print(f"Combined dataset: {len(self.combined_data)} rows")
        
    def get_channel_summary(self):
        """Get summary statistics by channel"""
        if self.marketing_data is None:
            return None
            
        channel_summary = self.marketing_data.groupby('channel').agg({
            'impressions': ['sum', 'mean'],
            'clicks': ['sum', 'mean'],
            'spend': ['sum', 'mean'],
            'attributed_revenue': ['sum', 'mean'],
            'ctr': 'mean',
            'cpc': 'mean',
            'roas': 'mean'
        }).round(2)
        
        return channel_summary
    
    def get_date_range(self):
        """Get the date range of the data"""
        if self.combined_data is not None:
            return self.combined_data['date'].min(), self.combined_data['date'].max()
        return None, None
    
    def process_all(self):
        """Execute the complete data processing pipeline"""
        print("🚀 Starting data processing pipeline...")
        
        if not self.load_data():
            return False
            
        self.clean_marketing_data()
        self.clean_business_data()
        self.combine_data()
        
        print("✅ Data processing completed successfully!")
        return True

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    if processor.process_all():
        print("\n📊 Data Summary:")
        print(f"Date range: {processor.get_date_range()}")
        print("\n🎯 Channel Performance:")
        print(processor.get_channel_summary())