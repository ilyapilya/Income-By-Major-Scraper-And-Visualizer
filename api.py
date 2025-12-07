from flask import Flask, jsonify
from flask_cors import CORS
from database.database import Database
from statplot import Plotter
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

app = Flask(__name__)
CORS(app)

# Initialize database
db = Database(host="localhost", user="root", database="income_major_db")

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Retrieve income statistics from database"""
    try:
        stats = db.get_statistics()
        
        if not stats:
            return jsonify({"error": "Failed to retrieve statistics"}), 500
        
        # Get additional details - top 10 majors
        top_majors = db.get_top_n_majors(10)
        
        return jsonify({
            "total_majors": stats['total_majors'],
            "avg_income": round(float(stats['avg_income']), 2),
            "max_income": stats['max_income'],
            "min_income": stats['min_income'],
            "top_majors": top_majors
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/plot', methods=['GET'])
def get_plot():
    """Generate and return plot as base64 encoded image"""
    try:
        # Fetch all majors from database
        all_majors = db.get_all_majors()
        
        if not all_majors:
            return jsonify({"error": "No data available for plotting"}), 404
        
        # Convert database results to job format
        jobs = [
            {"major": major['major'], "income": major['income']}
            for major in all_majors
        ]
        
        # Create plotter and set bounds
        plotter = Plotter(jobs)
        
        # Get min and max income for dynamic bounds
        incomes = [job['income'] for job in jobs]
        min_income = min(incomes)
        max_income = max(incomes)
        
        plotter.set_income_bounds(min_income, max_income)
        
        # Create the plot
        filtered_jobs = [
            job for job in jobs 
            if plotter.lower_income_bound <= job['income'] <= plotter.upper_income_bound
        ]
        
        if not filtered_jobs:
            return jsonify({"error": "No jobs in income range"}), 404
        
        # Sort by income descending
        filtered_jobs.sort(key=lambda x: x['income'], reverse=True)
        
        # Extract data
        majors = [job['major'] for job in filtered_jobs]
        incomes_list = [job['income'] for job in filtered_jobs]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.barh(majors, incomes_list, color='steelblue')
        ax.set_xlabel('Median Income ($)', fontsize=12)
        ax.set_ylabel('Major', fontsize=12)
        ax.set_title('College Majors by Income', fontsize=14, fontweight='bold')
        ax.invert_yaxis()  # Highest income at top
        
        # Format x-axis as currency
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        
        # Convert to base64
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return jsonify({
            "image": f"data:image/png;base64,{img_base64}",
            "total_majors": len(filtered_jobs)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
