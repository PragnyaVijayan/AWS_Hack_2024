import io
import matplotlib
import matplotlib.pyplot as plt
import requests
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)
CORS(app)

@app.route('/line_graph')
def plot_graph():
    # LINE GRAPH
    fig, ax = plt.subplots()

    # Make background black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set plot titles
    ax.set_title('Awesome Trends', color='white', fontdict={'fontsize': 20, 'fontweight': 'bold', 'family': 'arial'})
    ax.set_xlabel('X Axis', color='white') 
    ax.set_ylabel('Y Axis', color='white')

    # Change axis colors
    ax.tick_params(axis='both', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    ax.spines['top'].set_color('white')
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_color('white')
    ax.spines['right'].set_linewidth(2)
    ax.spines['left'].set_color('white')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_color('white')
    ax.spines['bottom'].set_linewidth(2)

    ax.grid(color='white')

    # Plot data
    ax.plot([1, 2, 3, 4], [1, 4, 9, 16], color='#AFE692', linewidth = 3, label="data1")
    ax.plot([1, 2, 3, 4], [1, 8, 3, 15], color='#E69292', linewidth = 3, label="data2")
    plt.legend()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Serve the image as a response
    return send_file(img, mimetype='image/png')

# sample call: http://127.0.0.1:5001/get_salary_plot?location=CA&occupation=Data%20Scientists&contract=50
@app.route('/get_salary_plot', methods=['GET'])
def bar_graph():
    # get query parameter
    location = request.args.get('location')  
    occupation = request.args.get('occupation') 
    contactPay = float(request.args.get('contract'))

    # call API to get job salary data
    response = requests.get(f"http://127.0.0.1:5000/jobSalary?location={location}&occupation={occupation}")

    if response.status_code != 200:
        return jsonify({"error": "Failed to get data from jobSalary"}), 500
    
    jobSalaryData = response.json() 

    # read salary percitile data from api
    pct10 = float(jobSalaryData["Pct10"])
    pct25 = float(jobSalaryData["Pct25"])
    median = float(jobSalaryData["Median"])
    pct75 = float(jobSalaryData["Pct75"])
    pct90 = float(jobSalaryData["Pct90"])
        
    # BAR GRAPH
    fig, ax = plt.subplots()

    # Make background black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set plot titles
    ax.set_title(f'Salary for {occupation}', color='white', fontdict={'fontsize': 20, 'fontweight': 'bold', 'family': 'arial'})
    ax.set_xlabel('Percentile', color='white', fontweight='bold')
    ax.set_ylabel('Rate ($ per hour)', color='white', fontweight='bold')

    # Change axis colors
    ax.tick_params(axis='both', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    ax.spines['top'].set_color('white')
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_color('white')
    ax.spines['right'].set_linewidth(2)
    ax.spines['left'].set_color('white')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_color('white')
    ax.spines['bottom'].set_linewidth(2)

    ax.grid(color='white')

    # Convert api values to data
    y = [pct10, pct25, median, pct75, pct90, contactPay]
    x = [1, 2, 3, 4, 5, 6]
    labels = ["pct10", "pct25", "median", "pct75", "pct90", "contract"]

    # Plot bar graph
    bars = ax.bar(x, y, color='#AFE692', width=0.3, align='center')
    bars[-1].set_color('#E69292') # make contract data a different color

    # Add x labels to each bar
    ax.set_xticks(x)
    ax.set_xticklabels(labels, color='white', fontweight='bold')

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Serve the image as a response
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
