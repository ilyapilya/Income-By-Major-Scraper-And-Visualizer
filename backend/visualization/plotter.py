import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, jobs):
        self.jobs = jobs
        self.lower_income_bound = None
        self.upper_income_bound = None
    
    def set_income_bounds(self, lower: int, upper: int):
        self.lower_income_bound = lower
        self.upper_income_bound = upper

    def plot_major_vs_income(self):
        if not self.upper_income_bound or not self.lower_income_bound:
            print("Income bounds must be set first")
            return
        
        # Filtering based on range
        filtered_jobs = [
            job for job in self.jobs
            if self.lower_income_bound <= job['income'] <= self.upper_income_bound
        ]

        if not filtered_jobs:
            print("No jobs found in the specified income range")
            return
        
        majors = [job['major'] for job in filtered_jobs]
        incomes = [job['income'] for job in filtered_jobs]

                
        # Sort by income descending
        filtered_jobs.sort(key=lambda x: x['income'], reverse=True)
        
        # Extract data for plotting
        majors = [job['major'] for job in filtered_jobs]
        incomes = [job['income'] for job in filtered_jobs]
        
        # Create figure and plot
        plt.figure(figsize=(14, 8))
        plt.barh(majors, incomes, color='steelblue')
        plt.xlabel('Median Income ($)', fontsize=12)
        plt.ylabel('Major', fontsize=12)
        plt.title(f'College Majors by Income (${self.lower_income_bound:,} - ${self.upper_income_bound:,})', fontsize=14)
        plt.gca().invert_yaxis()  # Highest income at top
        
        # Format x-axis as currency
        ax = plt.gca()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        plt.show()

    def save_plot(self, save_path : str = "plot.png"):
        plt.savefig(save_path)
        print(f"Plot saved to: {save_path}")
