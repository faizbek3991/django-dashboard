from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import random
import os
from functools import wraps

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Required for Django (no display)
import matplotlib.pyplot as plt
import io, base64
import numpy as np
from sklearn.linear_model import LinearRegression

# Create your views here.

def require_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.session.get('authenticated'):
        return redirect('home')

    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if username == 'faiz' and password == 'abcd123!':
            request.session['authenticated'] = True
            request.session['username'] = username
            return redirect('home')

        error = 'Invalid username or password.'

    return render(request, 'login.html', {
        'title': 'Login',
        'error': error,
    })


def logout_view(request):
    request.session.flush()
    return redirect('home')
 
@require_login
def home(request):
    context = {
        'title': 'Factory Dashboard',
        'total_output': 12450,
        'avg_oee': 83.6,
        'defect_rate': 1.8,
        'machines_online': 8,
        'total_machines': 10,
        'username': request.session.get('username'),
    }
    return render(request, 'home.html', context)


@require_login
def data_view(request):
    csv_path = os.path.join(
        os.path.dirname(__file__), 'data', 'production.csv')

    try:
        df = pd.read_csv(csv_path)

        table_html = df.to_html(classes='data-table', index=False)

        stats = {
            'total_rows': len(df),
            'avg_output': f"{df['Total_Output'].mean():.0f}",
            'max_output': f"{df['Total_Output'].max()}",
            'min_output': f"{df['Total_Output'].min()}",
        }
        error = None
    except FileNotFoundError:
        table_html = None
        stats = {}
        error = 'CSV not found'

    return render(request, 'data.html', {
        'table': table_html,
        'stats': stats,
        'error': error,
        'title': 'Data',
        'username': request.session.get('username'),
    })

@require_login
def charts_view(request):
    '''Generate matplotlib charts and embed in HTML'''
    csv_path = os.path.join(
        os.path.dirname(__file__), 'data', 'production.csv')
   
    try:
        df = pd.read_csv(csv_path)
    except:
        return render(request, 'charts.html',
            {'error': 'CSV not found!', 'title': 'Charts'})
   
    charts = []
   
    # Chart 1: Daily Output Bar Chart (Day 4 skill!)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(len(df)), df['Total_Output'], color='#3498db')
    ax.set_title('Daily Production Output', fontweight='bold')
    ax.set_xlabel('Day'); ax.set_ylabel('Units')
    ax.grid(axis='y', alpha=0.3); plt.tight_layout()
    charts.append(fig_to_base64(fig))
   
    # Chart 2: OEE Trend Line (Day 5 skill!)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(len(df)), df['OEE_Pct'], marker='o',
            markersize=3, color='#2ecc71')
    ax.axhline(y=85, color='red', linestyle='--', label='Target 85%')
    ax.fill_between(range(len(df)), df['OEE_Pct'], 85,
        where=df['OEE_Pct'] < 85, alpha=0.2, color='red')
    ax.set_title('OEE Trend', fontweight='bold')
    ax.legend(); ax.grid(True, alpha=0.3); plt.tight_layout()
    charts.append(fig_to_base64(fig))
   
    # Chart 3: Defects Pie Chart (Day 4 skill!)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie([df['Total_Defects'].sum(), df['Total_Output'].sum()],
           labels=['Defects', 'Good Units'], autopct='%1.1f%%',
           colors=['#e74c3c', '#2ecc71'])
    ax.set_title('Quality Distribution'); plt.tight_layout()
    charts.append(fig_to_base64(fig))
   
    return render(request, 'charts.html',
        {'charts': charts, 'title': 'Charts',
         'username': request.session.get('username')})
 
def fig_to_base64(fig):
    '''Convert matplotlib figure to base64 string for HTML'''
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor='white')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'data:image/png;base64,{img_str}'

@require_login
def predict_view(request):
    '''ML prediction form — predict defect rate'''
    prediction = None
    risk_level = None
    input_data = {}
   
    if request.method == 'POST':
        # Get form data (Day 3: input handling!)
        try:
            temp = float(request.POST.get('temperature', 30))
            humidity = float(request.POST.get('humidity', 60))
            age = float(request.POST.get('machine_age', 5))
            speed = float(request.POST.get('speed', 1200))
            vibration = float(request.POST.get('vibration', 2))
           
            input_data = {'temperature': temp, 'humidity': humidity,
                'machine_age': age, 'speed': speed, 'vibration': vibration}
           
            # Day 6 skill: Build & use ML model!
            # Train on sample data (in real app, load saved model)
            np.random.seed(42)
            n = 200
            X_train = np.column_stack([
                np.random.uniform(22, 42, n),
                np.random.uniform(40, 85, n),
                np.random.uniform(1, 10, n),
                np.random.uniform(800, 1800, n),
                np.random.uniform(0.5, 5, n),
            ])
            y_train = (0.15*X_train[:,0] + 0.05*X_train[:,1]
                + 0.3*X_train[:,2] + 0.002*X_train[:,3]
                + 1.5*X_train[:,4] + np.random.normal(0, 1, n))
           
            model = LinearRegression()
            model.fit(X_train, y_train)
           
            # Predict!
            user_input = np.array([[temp, humidity, age, speed, vibration]])
            prediction = round(model.predict(user_input)[0], 2)
           
            if prediction < 5:
                risk_level = ('🟢 Low Risk', '#2ecc71')
            elif prediction < 10:
                risk_level = ('🟡 Medium Risk', '#f39c12')
            else:
                risk_level = ('🔴 High Risk', '#e74c3c')
               
        except ValueError:
            prediction = 'Error: Invalid input!'
            risk_level = ('❌ Error', '#e74c3c')
   
    return render(request, 'predict.html', {
        'title': 'Defect Prediction',
        'prediction': prediction,
        'risk_level': risk_level,
        'input_data': input_data,
        'username': request.session.get('username'),
    })
 