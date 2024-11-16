import io
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, send_file

matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)

@app.route('/plot')
def plot_graph():
    # Create a Matplotlib graph
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30], label="Line 1")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
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
