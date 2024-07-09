from flask import Flask, request, jsonify, send_file, send_from_directory, redirect, url_for
from flask_cors import CORS
import pandas as pd
import os
import matplotlib.pyplot as plt
import json

app = Flask(__name__, static_folder='static')
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/result_page')
def result_page():
    return send_from_directory('.', 'result_page.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        uploaded_df = pd.read_csv(file_path, low_memory=False)
        reference_df = pd.read_csv('DrDos_NTP.csv', low_memory=False)

        if set(uploaded_df.columns) == set(reference_df.columns):
            message = "The uploaded file matches the reference file structure. Further analysis would be required to determine if it's a DoS attack."
            plt.figure(figsize=(10, 6))
            plt.plot([1, 2, 3, 4], [10, 20, 25, 30], label='DoS Attacks')
            plt.xlabel('Time')
            plt.ylabel('Number of Attacks')
            plt.title('DoS Attacks Over Time')
            plt.legend()
            graph_path = os.path.join(UPLOAD_FOLDER, 'attack_graph.png')
            plt.savefig(graph_path)
        else:
            message = "The uploaded file does not match the reference file structure."
            graph_path = None

        source_ip = request.remote_addr
        result = {'message': message, 'source_ip': source_ip}
        if graph_path:
            result['graph_path'] = graph_path

        with open(os.path.join(UPLOAD_FOLDER, 'result.json'), 'w') as f:
            json.dump(result, f)

    except Exception as e:
        return jsonify({'message': f'Error processing file: {str(e)}'}), 500

    return jsonify(result)

@app.route('/get_results', methods=['GET'])
def get_results():
    try:
        with open(os.path.join(UPLOAD_FOLDER, 'result.json')) as f:
            result = json.load(f)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'Error fetching results: {str(e)}'}), 500

@app.route('/graph')
def get_graph():
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, 'attack_graph.png'), mimetype='image/png')
    except Exception as e:
        return jsonify({'message': f'Error sending graph: {str(e)}'}), 500

@app.route('/model_accuracy', methods=['GET'])
def get_model_accuracy():
    accuracy = 0.95  # Example accuracy, replace with your actual value
    return jsonify({'accuracy': accuracy})

if __name__ == '__main__':
    app.run(debug=True)
