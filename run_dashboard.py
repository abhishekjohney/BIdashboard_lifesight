"""
Simplified Dashboard Runner for Testing
This version checks dependencies and provides setup instructions
"""

import sys
import os

def check_python_setup():
    """Check Python environment and provide setup instructions"""
    print("🔍 Checking Python Environment...")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check if we can import basic modules
    try:
        import json
        print("✅ Standard library working")
    except ImportError:
        print("❌ Standard library issue")
        return False
    
    # Try to import required packages
    missing_packages = []
    required_packages = ['streamlit', 'pandas', 'numpy', 'plotly']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Missing packages: {', '.join(missing_packages)}")
        print("\n📋 Setup Instructions:")
        print("1. Install Python from python.org (if needed)")
        print("2. Install packages:")
        print("   py -m pip install --user streamlit pandas numpy plotly")
        print("   OR")
        print("   python -m pip install --user streamlit pandas numpy plotly")
        print("3. Run the dashboard:")
        print("   py -m streamlit run main.py")
        return False
    
    return True

def create_basic_html_dashboard():
    """Create a basic HTML dashboard as fallback"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketing Intelligence Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .metric-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
            border-left: 4px solid #3498db;
            display: inline-block;
            width: 200px;
            vertical-align: top;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        .metric-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .setup-section {
            background: #e8f6f3;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #27ae60;
        }
        .code {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Marketing Intelligence Dashboard</h1>
            <h3>Sample Marketing Metrics (Demo Data)</h3>
        </div>
        
        <div style="text-align: center;">
            <div class="metric-card">
                <div class="metric-value">$127,350</div>
                <div class="metric-label">Total Revenue (120 days)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$23,450</div>
                <div class="metric-label">Marketing Spend</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">5.43x</div>
                <div class="metric-label">Overall ROAS</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">$38.50</div>
                <div class="metric-label">Customer Acq. Cost</div>
            </div>
        </div>
        
        <div class="setup-section">
            <h3>🚀 To Run the Full Interactive Dashboard:</h3>
            <p><strong>1. Install Required Packages:</strong></p>
            <div class="code">py -m pip install --user streamlit pandas numpy plotly</div>
            
            <p><strong>2. Run the Dashboard:</strong></p>
            <div class="code">py -m streamlit run main.py</div>
            
            <p><strong>3. Alternative (if py doesn't work):</strong></p>
            <div class="code">python -m pip install --user streamlit pandas numpy plotly<br>
python -m streamlit run main.py</div>
        </div>
        
        <div style="margin-top: 30px;">
            <h3>📈 Dashboard Features (When Fully Running):</h3>
            <ul>
                <li><strong>Interactive Charts:</strong> Revenue trends, channel performance</li>
                <li><strong>Real-time Filtering:</strong> Date ranges, channels, campaigns</li>
                <li><strong>Automated Insights:</strong> Top performers, efficiency metrics</li>
                <li><strong>Multi-Channel Analysis:</strong> Facebook, Google, TikTok</li>
                <li><strong>Business Intelligence:</strong> ROI, attribution, customer metrics</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
            <p>Built for Marketing Intelligence Assessment | Streamlit + Python</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open("dashboard_preview.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Created dashboard_preview.html as a fallback")
    print("💡 Open 'dashboard_preview.html' in your browser to see a preview")

def main():
    print("🚀 Marketing Intelligence Dashboard - Setup Check")
    print("=" * 60)
    
    if check_python_setup():
        print("\n🎉 All dependencies available! Running dashboard...")
        try:
            # Try to run streamlit
            import subprocess
            result = subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"], 
                                  capture_output=False)
        except Exception as e:
            print(f"❌ Error running dashboard: {e}")
            create_basic_html_dashboard()
    else:
        print("\n🔧 Creating HTML preview while you set up dependencies...")
        create_basic_html_dashboard()
        
        print("\n📋 Next Steps:")
        print("1. Fix Python package installation")
        print("2. Install required packages")
        print("3. Run: py -m streamlit run main.py")
        print("4. Or open dashboard_preview.html for a preview")

if __name__ == "__main__":
    main()