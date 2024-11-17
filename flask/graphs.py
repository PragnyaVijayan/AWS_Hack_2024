import io
import matplotlib
import matplotlib.pyplot as plt
import requests
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)
CORS(app)

@app.route('/job_salary_trend', methods=['GET'])
def plot_job_salary_trend():
    # get query parameter
    contactPay = float(request.args.get('contract'))

    # call API to get user past job salary
    response = requests.get("http://127.0.0.1:5000/s3_user_read")

    if response.status_code != 200:
        return jsonify({"error": "Failed to get data from s3_user_read"}), 500
    
    jobSalaryData = response.json() 
    pastJobSalaryString = jobSalaryData["pastSalaryInputVal"]
    pastJobSalary = [float(num.strip()) for num in pastJobSalaryString.split(",")] # convert string to array
    pastJobSalary.append(contactPay) # Add new job pay

    # Make graph
    fig, ax = plt.subplots()

    # Make background black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set plot titles
    ax.set_title('Your Salary Trend', color='white', fontdict={'fontsize': 20, 'fontweight': 'bold', 'family': 'arial'})
    ax.set_xlabel('Job Number', color='white', fontweight='bold') 
    ax.set_ylabel('Salary ($ per hour)', color='white', fontweight='bold')

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
    x = list(range(1, len(pastJobSalary) + 1))
    ax.plot(x, pastJobSalary, "o-", color='#AFE692', linewidth = 3, markersize=8)

    # Label last point (new contract)
    ax.annotate('New',
        xy=(x[-1], pastJobSalary[-1]), 
        xytext=(x[-1], pastJobSalary[-1] + 1.5),
        textcoords='data',
        fontsize=14, color='white',
        fontweight='bold', 
        ha='center', va='bottom',
        bbox=dict(facecolor='#E69292', alpha=1, boxstyle="round,pad=0.3")) 

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
        return jsonify({"error": "No salary data could be found for the provided occuptation and location"}), 500
    
    jobSalaryData = response.json() 

    # read salary percitile data from api
    pct10 = float(jobSalaryData["Pct10"])
    pct25 = float(jobSalaryData["Pct25"])
    median = float(jobSalaryData["Median"])
    pct75 = float(jobSalaryData["Pct75"])
    pct90 = float(jobSalaryData["Pct90"])

    # Convert api values to data
    y = [pct10, pct25, median, pct75, pct90, contactPay]
    x = [1, 2, 3, 4, 5, 6]
    labels = ["pct10", "pct25", "median", "pct75", "pct90", "contract"]

    if(jobSalaryData["RateType"] == "Annual"):
        y = [curY / 2080 for curY in y[:-1]] + [y[-1]] # divide by 40 hours * 52 week
        
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
