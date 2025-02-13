from flask import Flask, request, jsonify
import subprocess
import os
import json
import requests
import sys
from datetime import datetime
import re
import pytesseract
from PIL import Image
import sqlite3
import re
from PIL import Image
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
AIPROXY_TOKEN =os.environ.get("AIPROXY_TOKEN", "")
DATA_DIR = "/data"
USER_EMAIL = "22f3001851@ds.study.iitm.ac.in"
DATAGEN_URL = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
TMP_DIR = "C:\\temp\\" if sys.platform == "win32" else "/tmp/"
SCRIPT_PATH = os.path.join(TMP_DIR, "datagen.py")

# Helper function to ensure paths stay within /data
def safe_path(filename):
    return os.path.join(DATA_DIR, os.path.basename(filename))

def install_missing_package(package):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to install {package}: {e}"}, 500
    return None

def handle_task_a1():
    try:
        subprocess.run(["pip", "install", "uv"], check=True)
        os.makedirs(TMP_DIR, exist_ok=True)
        response = requests.get(DATAGEN_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download datagen.py"}), 500
        with open(SCRIPT_PATH, "wb") as f:
            f.write(response.content)
        error = install_missing_package("faker")
        if error:
            return jsonify(error)
        python_cmd = sys.executable
        result = subprocess.run([python_cmd, SCRIPT_PATH, USER_EMAIL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return jsonify({"error": f"Script failed: {result.stderr}"}), 500
        return jsonify({"message": "Task A1 completed successfully"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Command failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import subprocess

import subprocess

def run_prettier():
    try:
        file_path = "D:/padhai/TDS-PROJECT-1/llm-automation-agent/data/format.md"

        # Run Prettier using `npx`
        result = subprocess.run(["npx", "prettier", "--write", file_path], capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            return jsonify({"message": "File formatted successfully"})
        else:
            return jsonify({"error": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
def count_wednesdays():
    input_file = safe_path("dates.txt")
    output_file = safe_path("dates-wednesdays.txt")
    count = 0
    with open(input_file, 'r') as f:
        for line in f:
            try:
                date_obj = datetime.strptime(line.strip(), "%Y-%m-%d")
                if date_obj.strftime("%A") == "Wednesday":
                    count += 1
            except ValueError:
                continue
    with open(output_file, 'w') as f:
        f.write(str(count))
    return jsonify({"message": "Wednesdays counted", "count": count})

def sort_contacts():
    input_file = safe_path("contacts.json")
    output_file = safe_path("contacts-sorted.json")
    with open(input_file, 'r') as f:
        contacts = json.load(f)
    contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
    with open(output_file, 'w') as f:
        json.dump(contacts, f, indent=4)
    return jsonify({"message": "Contacts sorted successfully"})

def extract_recent_logs():
    logs_dir = os.path.join(DATA_DIR, "logs")
    output_file = safe_path("logs-recent.txt")
    log_files = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith(".log")]
    log_files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    recent_lines = []
    for log_file in log_files[:10]:
        with open(log_file, 'r') as f:
            first_line = f.readline().strip()
            if first_line:
                recent_lines.append(first_line)
    with open(output_file, 'w') as f:
        f.write("\n".join(recent_lines))
    return jsonify({"message": "Recent logs extracted"})
# Task A6: Markdown Indexing
def index_markdown():
    docs_path = "/data/docs/"
    index = {}
    
    for filename in os.listdir(docs_path):
        if filename.endswith(".md"):
            with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("# "):
                        index[filename] = line.strip("# ").strip()
                        break
    
    with open("/data/docs/index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)
    return jsonify({"message": "Markdown index created"})

# Task A7: Extract Email Sender
import openai

openai.api_key = AIPROXY_TOKEN

import openai

client = openai.Client(api_key=AIPROXY_TOKEN)  # Correct way to initialize in v1.0.0+

def extract_email_sender():
    with open("/data/email.txt", "r", encoding="utf-8") as f:
        email_content = f.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract sender email from the following email content and provide only the email address."},
            {"role": "user", "content": email_content}
        ],
        max_tokens=20
    )

    sender_email = response.choices[0].message.content.strip()

    with open("/data/email-sender.txt", "w", encoding="utf-8") as f:
        f.write(sender_email)

    return {"message": "Email sender extracted"}



# Task A8: Extract Credit Card Number from Image
def extract_credit_card():
    
    image = Image.open("data/credit-card.png")
    extracted_text = pytesseract.image_to_string(image)
    
    match = re.search(r"\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}", extracted_text)
    if match:
        card_number = match.group().replace(" ", "").replace("-", "")
        with open("/data/credit-card.txt", "w", encoding="utf-8") as f:
            f.write(card_number)
        return jsonify({"message": "Credit card number extracted"})
    return jsonify({"error": "Could not extract credit card number"}), 400

# Task A9: Find Most Similar Comments
def find_similar_comments():
    with open("/data/comments.txt", "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines()]
    
    client = OpenAI(api_key=AIPROXY_TOKEN)
    embeddings = [client.Embedding.create(input=comment, model="text-embedding-ada-002")["data"][0]["embedding"] for comment in comments]
    similarity_matrix = cosine_similarity(np.array(embeddings))
    
    max_sim = 0
    pair = (None, None)
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            if similarity_matrix[i][j] > max_sim:
                max_sim = similarity_matrix[i][j]
                pair = (comments[i], comments[j])
    
    with open("/data/comments-similar.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(pair))
    return jsonify({"message": "Most similar comments found"})

# Task A10: Calculate Total Sales for Gold Tickets
def calculate_gold_ticket_sales():
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0
    conn.close()
    
    with open("/data/ticket-sales-gold.txt", "w", encoding="utf-8") as f:
        f.write(str(total_sales))
    return jsonify({"message": "Total sales calculated", "total_sales": total_sales})

@app.route("/run", methods=["POST"])
def run_task():
    task = request.args.get("task", "").lower()
    try:
        if "datagen" in task:
            return handle_task_a1()
        elif "format" in task and "prettier" in task:
            return run_prettier()
        elif "count" in task and "wednesdays" in task:
            return count_wednesdays()
        elif "sort" in task and "contacts" in task:
            return sort_contacts()
        elif "logs" in task and "recent" in task:
            return extract_recent_logs()
        elif "index" in task and "markdown" in task:
            return index_markdown()
        elif "email" in task and "sender" in task:
            return extract_email_sender()
        elif "credit card" in task:
            return extract_credit_card()
        elif "comments" in task and "similar" in task:
            return find_similar_comments()
        elif "gold" in task and "sales" in task:
            return calculate_gold_ticket_sales()
        else:
            return jsonify({"error": "Unknown task"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
