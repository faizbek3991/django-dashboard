# 🏭 Factory Dashboard

A modern Django-based factory production dashboard with real-time data visualization, analytics, and predictive analytics.

## ✨ Features

- **🔐 Secure Authentication**: Login system with session-based authentication
  - Username: `faiz`
  - Password: `abcd123!`
- **📊 KPI Dashboard**: Real-time key performance indicators
  - Total Output, Average OEE, Defect Rate, Machine Status
- **📈 Advanced Charts**: Interactive production visualizations
  - Daily Output (Bar Chart)
  - OEE Trend (Line Chart with target indicators)
  - Quality Distribution (Pie Chart)
- **📂 Data Management**: Production data table with statistical analysis
  - View detailed production records
  - Statistical summaries (avg, min, max output)
- **🤖 Defect Prediction**: ML-based defect rate prediction
  - Input: Temperature, Humidity, Machine Age, Speed, Vibration
  - Output: Predicted defect rate with risk level
- **🎨 Dark/Light Theme**: Toggle theme with persistent storage
  - Auto-saves preference to localStorage
  - Applies across all pages
- **📱 Responsive Design**: Works on all screen sizes
- **🚪 Easy Logout**: Secure logout with navigation back to login

## 🛠 Tech Stack

- **Backend**: Django 6.0.5
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite3
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Machine Learning**: Scikit-learn
- **Python**: 3.12+

## 📋 Requirements

```
Django==6.0.5
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
scikit-learn>=1.3
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/faizbek3991/django-dashboard.git
cd django-dashboard
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd factory_dashboard
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start Server
```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

## 🔑 Login Credentials

| Field | Value |
|-------|-------|
| Username | `faiz` |
| Password | `abcd123!` |

## 📖 User Guide

### 📊 Dashboard (Home)
- View 4 key KPI cards
- Monitor real-time statistics
- Quick navigation to all sections

### 📂 Data View
- Browse production data in table format
- View statistics: total rows, average output, min/max values
- Filter and analyze historical data

### 📈 Charts View
1. **Daily Output** - Bar chart of production per day
2. **OEE (Overall Equipment Efficiency)** - Trend line with 85% target indicator
3. **Quality Distribution** - Pie chart of defects vs good units

*All charts have white backgrounds for clarity*

### 🤖 Prediction Model
Input parameters:
- 🌡️ **Temperature** (°C): 22-42°C range
- 💧 **Humidity** (%): 40-85% range
- ⚙️ **Machine Age** (years): 1-10 years
- 🔧 **Speed** (RPM): 800-1800 RPM
- 📳 **Vibration** (mm/s): 0.5-5 mm/s

Output:
- Predicted defect rate percentage
- Risk level indicator (🟢 Low / 🟡 Medium / 🔴 High)

### 🎨 Theme Control
- Click the button in top-right corner (🌙/☀️)
- Switch between dark and light themes
- Preference auto-saves in browser storage
- Applies instantly across all pages

## 📁 Project Structure

```
django-dashboard/
├── README.md
├── factory_dashboard/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   ├── dashboard/
│   │   ├── views.py          # Core application logic
│   │   ├── urls.py           # URL routing
│   │   ├── models.py         # Database models
│   │   ├── admin.py          # Django admin configuration
│   │   ├── migrations/       # Database migrations
│   │   ├── data/
│   │   │   └── production.csv # Sample data (28 days)
│   │   └── templates/
│   │       ├── login.html    # Login page with theme toggle
│   │       ├── home.html     # Dashboard/KPI view
│   │       ├── data.html     # Data table view
│   │       ├── charts.html   # Charts visualization
│   │       └── predict.html  # Prediction form
│   └── factory_dashboard/
│       ├── settings.py       # Django settings
│       ├── urls.py           # Main URL configuration
│       ├── wsgi.py
│       └── asgi.py
```

## 🔐 Authentication Flow

1. **First Visit**: Redirected to `/login/`
2. **Login**: Enter credentials (faiz / abcd123!)
3. **Session Created**: User session stored in database
4. **Access Dashboard**: All pages protected except login
5. **Logout**: Clears session, redirects to login page

## 📊 Sample Data

Production data includes 28 days of:
- Daily output (250-400 units)
- OEE percentages (70-95%)
- Defect counts (5-25 per day)
- Downtime minutes (0, 15, 30, 60, or 90 min)

Located in: `dashboard/data/production.csv`

## 🎯 Navigation

From any page, access:
- 📊 **Dashboard** - Home KPI view
- 📂 **Data** - Production data table
- 📈 **Charts** - Visualizations
- 🤖 **Predict** - ML prediction tool
- 🚪 **Logout** - Exit and return to login

## 🔧 Configuration

### Add Data
Update `dashboard/data/production.csv` with new production data

### Change Login Credentials
Edit in `dashboard/views.py`:
```python
if username == 'faiz' and password == 'abcd123!':
    # Change these values
```

### Customize Dashboard Metrics
Edit `home()` function in `dashboard/views.py`:
```python
context = {
    'total_output': 12450,      # Update these
    'avg_oee': 83.6,
    'defect_rate': 1.8,
    'machines_online': 8,
}
```

## 📈 ML Model Details

The defect prediction model uses:
- **Algorithm**: Linear Regression
- **Training**: 200 synthetic samples with randomized parameters
- **Features**: Temperature, Humidity, Machine Age, Speed, Vibration
- **Output**: Defect rate (%)

Risk levels:
- 🟢 **Low Risk**: < 5% defects
- 🟡 **Medium Risk**: 5-10% defects
- 🔴 **High Risk**: > 10% defects

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No such table: django_session" | Run `python manage.py migrate` |
| Charts not showing | Install matplotlib: `pip install matplotlib` |
| Theme not persisting | Enable localStorage in browser |
| Login page shows error | Ensure database is migrated |
| CSV file not found | Check `dashboard/data/production.csv` exists |

## ⚠️ Production Checklist

- [ ] Change default login credentials
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` in settings.py
- [ ] Use a production database (PostgreSQL recommended)
- [ ] Set up HTTPS/SSL
- [ ] Use environment variables for sensitive data
- [ ] Configure proper static files handling

## 📄 License

Open source project - MIT License

## 👨‍💻 Author

**faizbek3991**

Feel free to contribute, report issues, or suggest improvements!

---

**Created with ❤️ using Django**