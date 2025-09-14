# 📊 Marketing Intelligence Dashboard

A comprehensive BI dashboard that transforms marketing campaign data into actionable business insights. This tool helps marketing leaders understand how their campaigns across Facebook, Google, and TikTok drive business outcomes.

## 🎯 Problem Statement

E-commerce businesses need to:
- Connect marketing activities with business outcomes
- Optimize budget allocation across channels
- Track ROI and attribution accurately
- Make data-driven decisions quickly
- Understand customer acquisition efficiency

## ✨ Features

### 📈 Executive Dashboard
- **Key Performance Indicators**: Revenue, spend, ROAS, customer acquisition cost
- **Trend Analysis**: Daily revenue vs. marketing spend visualization
- **Channel Comparison**: Performance metrics across all marketing channels

### 🔍 Interactive Analysis
- **Date Range Filtering**: Analyze specific time periods
- **Channel Deep Dive**: Individual platform performance analysis
- **Campaign Performance**: Detailed campaign-level metrics and comparison

### 💡 Automated Insights
- **Top Performer Identification**: Automatically identifies best performing channels
- **Marketing Efficiency Analysis**: Revenue generated per marketing dollar spent
- **Growth Trend Detection**: Tracks business momentum over time
- **Optimization Recommendations**: Data-driven suggestions for improvement

### 📊 Key Metrics Tracked
- **ROAS (Return on Ad Spend)**: Revenue attributed per dollar spent
- **CPA (Cost Per Acquisition)**: Cost to acquire each new customer
- **CTR (Click-Through Rate)**: Engagement efficiency
- **Marketing Efficiency**: Total revenue per marketing dollar
- **Customer Lifetime Value indicators**

## 🚀 Quick Start

### Option 1: Local Development
```bash
# Clone the repository
git clone [repository-url]
cd BI_Dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run main.py
```

### Option 2: Use Sample Data
```bash
# Run with built-in sample data (for testing)
streamlit run main.py
```

### Option 3: Deploy to Streamlit Cloud
1. Fork this repository
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy with main file: `main.py`

## 📁 Data Requirements

The dashboard expects four CSV files in the `data/` directory:

### Marketing Data (Facebook.csv, Google.csv, TikTok.csv)
```csv
date,tactic,state,campaign,impressions,clicks,spend,attributed_revenue
2024-01-01,Video,CA,FB_Brand_Awareness,5000,75,60.50,240.00
```

### Business Data (Business.csv)
```csv
date,orders,new_orders,new_customers,total_revenue,gross_profit,cogs
2024-01-01,150,105,98,12750.00,5100.00,7650.00
```

*Note: The dashboard includes sample data generation for testing purposes.*

## 🏗️ Technical Architecture

### Core Components
- **Data Processor**: Handles data loading, cleaning, and preparation
- **Metrics Calculator**: Computes KPIs and business metrics
- **Visualization Engine**: Creates interactive charts and dashboards
- **Insight Generator**: Produces automated insights and recommendations

### Technology Stack
- **Frontend**: Streamlit for interactive web interface
- **Data Processing**: Pandas and Numpy for data manipulation
- **Visualizations**: Plotly for interactive charts
- **Deployment**: Streamlit Cloud for hosting

## 📊 Dashboard Pages

### 1. Executive Summary
- High-level KPIs and trends
- Channel performance comparison
- Automated insights and recommendations

### 2. Campaign Analysis
- Detailed campaign performance metrics
- Campaign comparison tools
- Optimization opportunities

### 3. Attribution Analysis
- Revenue attribution across channels
- Customer journey insights
- Multi-touch attribution modeling

## 💼 Business Value

### For Marketing Leaders
- **ROI Visibility**: Clear understanding of marketing effectiveness
- **Budget Optimization**: Data-driven allocation recommendations
- **Performance Monitoring**: Real-time tracking of key metrics

### For Executive Teams
- **Strategic Insights**: Connect marketing activities to business outcomes
- **Growth Tracking**: Monitor business momentum and trends
- **Investment Justification**: Demonstrate marketing's business impact

### For Data Teams
- **Automated Reporting**: Reduce manual reporting overhead
- **Scalable Architecture**: Easy to extend with additional data sources
- **Best Practices**: Implements data visualization and storytelling principles

## 🔧 Customization

### Adding New Channels
1. Update data loading in `scripts/data_processor.py`
2. Add channel-specific logic in `scripts/metrics_calculator.py`
3. Update visualization in `main.py`

### Custom Metrics
1. Define new calculations in `MetricsCalculator` class
2. Add visualization components
3. Update insight generation logic

## 📈 Sample Insights Generated

- "Facebook is the Top Performing Channel with 4.2x ROAS"
- "Every $1 spent on marketing generates $5.40 in total revenue"
- "Revenue trend is increasing by 15.3% over the period"
- "Customer acquisition cost is 0.8x the average order value"

## 🧪 Testing

Run the setup validation:
```bash
python test_setup.py
```

## 📚 Documentation

- **DEPLOYMENT.md**: Complete deployment guide
- **Sample Data**: Built-in data generation for testing
- **Code Comments**: Comprehensive inline documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- Real-time data connections
- Advanced attribution modeling
- Predictive analytics
- A/B testing framework
- Mobile-responsive design
- User authentication
- Export capabilities

---

**Built with ❤️ for data-driven marketing teams**

*Transform your marketing data into actionable insights today!*