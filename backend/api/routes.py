"""API routes for income analysis"""
from flask import jsonify
import io
import base64
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from ..database import Database
from ..visualization import Plotter
from ..config import config

# Initialize database with config settings
db = Database(host=config.DB_HOST, user=config.DB_USER, 
              password=config.DB_PASSWORD, database=config.DB_NAME)

# Load jobs from JSON as fallback
JOBS_FILE = Path(__file__).parent.parent.parent / "jobs.json"

def load_jobs_from_json():
    """Load jobs from JSON file if available"""
    try:
        if JOBS_FILE.exists():
            with open(JOBS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading jobs.json: {e}")
    return None


def register_routes(app):
    """Register all API routes with Flask app"""
    
    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        """Retrieve income statistics from database or JSON"""
        try:
            stats = db.get_statistics()
            
            if stats:
                # Got stats from database
                top_majors = db.get_top_n_majors(10)
                return jsonify({
                    "total_majors": stats['total_majors'],
                    "avg_income": round(float(stats['avg_income']), 2),
                    "max_income": stats['max_income'],
                    "min_income": stats['min_income'],
                    "top_majors": top_majors,
                    "source": "database"
                }), 200
            
            # Fallback to JSON file
            jobs = load_jobs_from_json()
            if jobs:
                incomes = [job['income'] for job in jobs]
                top_10 = sorted(jobs, key=lambda x: x['income'], reverse=True)[:10]
                
                return jsonify({
                    "total_majors": len(jobs),
                    "avg_income": round(sum(incomes) / len(incomes), 2),
                    "max_income": max(incomes),
                    "min_income": min(incomes),
                    "top_majors": top_10,
                    "source": "json"
                }), 200
            
            return jsonify({"error": "No data available"}), 404
        
        except Exception as e:
            # Final fallback to JSON
            jobs = load_jobs_from_json()
            if jobs:
                incomes = [job['income'] for job in jobs]
                top_10 = sorted(jobs, key=lambda x: x['income'], reverse=True)[:10]
                
                return jsonify({
                    "total_majors": len(jobs),
                    "avg_income": round(sum(incomes) / len(incomes), 2),
                    "max_income": max(incomes),
                    "min_income": min(incomes),
                    "top_majors": top_10,
                    "source": "json"
                }), 200
            
            return jsonify({"error": str(e)}), 500

    @app.route('/api/plot', methods=['GET'])
    def get_plot():
        """Generate and return plot as base64 encoded image"""
        try:
            # Try to fetch from database first
            all_majors = db.get_all_majors()
            
            if all_majors:
                jobs = [
                    {"major": major['major'], "income": major['income']}
                    for major in all_majors
                ]
            else:
                # Fallback to JSON
                jobs = load_jobs_from_json()
                if not jobs:
                    return jsonify({"error": "No data available for plotting"}), 404
            
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
