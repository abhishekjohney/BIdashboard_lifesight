# Marketing Intelligence Dashboard - Deployment Guide

## 🚀 Quick Start

### Option 1: Local Development
1. Clone or download this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Place your data files in the `data/` directory
4. Run: `streamlit run main.py`

### Option 2: Streamlit Cloud Deployment

#### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

#### Steps
1. **Upload to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/marketing-dashboard.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `main.py`
   - Click "Deploy"

## 📊 Data Requirements

### Marketing Data Files
Place these CSV files in the `data/` directory:

#### Facebook.csv
```
date,tactic,state,campaign,impressions,clicks,spend,attributed_revenue
2024-01-01,Video,CA,FB_Brand_Awareness,5000,75,60.50,240.00
```

#### Google.csv
```
date,tactic,state,campaign,impressions,clicks,spend,attributed_revenue
2024-01-01,Text,CA,Google_Search_Brand,3000,90,120.00,480.00
```

#### TikTok.csv
```
date,tactic,state,campaign,impressions,clicks,spend,attributed_revenue
2024-01-01,Video,CA,TT_Video_Ads,8000,160,80.00,240.00
```

#### Business.csv
```
date,orders,new_orders,new_customers,total_revenue,gross_profit,cogs
2024-01-01,150,105,98,12750.00,5100.00,7650.00
```

## 🔧 Configuration

### Environment Variables
No sensitive environment variables required for basic functionality.

### Customization
- Modify `main.py` to adjust dashboard layout
- Update `requirements.txt` for additional packages
- Customize styling in the CSS section of `main.py`

## 📈 Features

### Executive Dashboard
- **Key Metrics**: Revenue, spend, ROAS, CAC
- **Trend Analysis**: Daily revenue and spend tracking
- **Channel Performance**: ROAS comparison and spend distribution

### Interactive Filters
- **Date Range**: Analyze specific time periods
- **Channel Filter**: Focus on individual channels
- **Campaign Filter**: Drill down to campaign level

### Automated Insights
- Top performing channels identification
- Marketing efficiency analysis
- Growth trend detection
- Customer acquisition optimization

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all packages in `requirements.txt` are installed
   - Check Python version compatibility (3.7+)

2. **Data Loading Issues**
   - Verify CSV files are in the `data/` directory
   - Check CSV format matches expected columns
   - Ensure date format is YYYY-MM-DD

3. **Performance Issues**
   - Enable caching with `@st.cache_data` decorators
   - Reduce data size for large datasets
   - Optimize chart rendering

### Support
- Check the GitHub repository for updates
- Review Streamlit documentation for advanced features
- Contact the development team for custom requirements

## 🔄 Updates and Maintenance

### Regular Updates
- Monitor dashboard performance
- Update data sources regularly
- Review and optimize queries
- Add new features based on user feedback

### Scaling Considerations
- For large datasets, consider using a database backend
- Implement user authentication for sensitive data
- Add automated data refresh mechanisms
- Consider professional hosting for production use

## 📋 Checklist for Production

- [ ] Data files uploaded and formatted correctly
- [ ] Dependencies installed and tested
- [ ] Dashboard tested with sample data
- [ ] Styling and branding applied
- [ ] Performance optimized
- [ ] Deployed and accessible
- [ ] User training completed
- [ ] Monitoring and maintenance plan in place

## 🎯 Business Value

This dashboard provides:
- **Data-Driven Decisions**: Clear visualization of marketing ROI
- **Channel Optimization**: Identify best performing channels
- **Budget Allocation**: Data-backed spend recommendations
- **Performance Tracking**: Monitor KPIs in real-time
- **Stakeholder Communication**: Professional reporting interface

---

**Built with ❤️ for data-driven marketing teams**