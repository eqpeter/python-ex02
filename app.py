from flask import Flask, render_template, request, redirect, url_for
from ex_02v1 import Income, save_to_csv, load_csv
import os

app = Flask(__name__)

# 確保資料目錄存在
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(DATA_DIR, 'finance.csv')

@app.route('/')
def index():
    load_csv(CSV_FILE)
    return render_template('index.html', records=Income.all)

@app.route('/add', methods=['POST'])
def add():
    try:
        year = request.form['year']
        sales = request.form['sales']
        profit = request.form['profit']
        
        if all(val.strip().isdigit() for val in [year, sales, profit]):
            Income(year, sales, profit)
            save_to_csv(CSV_FILE)
            
    except Exception as e:
        print(f"錯誤: {e}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))