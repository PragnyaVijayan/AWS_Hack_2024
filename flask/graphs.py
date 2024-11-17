import io
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, send_file

matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)

@app.route('/line_graph')
def plot_graph():
    # LINE GRAPH
    fig, ax = plt.subplots()

    # Make background black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set plot titles
    ax.set_title('Awesome Trends', color='white', fontdict={'fontsize': 20, 'fontweight': 'bold'})
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

if __name__ == '__main__':
    app.run(debug=True)
