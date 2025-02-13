from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    # Logic to handle task execution goes here...
    return jsonify({"status": "200 OK", "message": "Task executed successfully."})

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    try:
        with open(path, 'r') as file:
            content = file.read()
        return jsonify({"status": "200 OK", "content": content})
    except FileNotFoundError:
        return jsonify({"status": "404 Not Found", "content": ""})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
