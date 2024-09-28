from flask import Flask, render_template, request, redirect, url_for, jsonify
from image_sentiment import ImageSentiment
from image_attention import ImageAttention
from visualizer import Visualizer
from goal import Goal
import sqlite3
import time
import base64
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    quote, image = Goal().get_motivation()
    return render_template('index.html', quote=quote, image=image)

@app.route('/capture_image', methods=['POST'])
def capture_image():
    data = request.get_json()
    image_data = data['image_data']

    # Decode the image data
    header, encoded = image_data.split(',', 1)
    image_bytes = base64.b64decode(encoded)

    # Save the image
    timestamp = time.strftime('%Y%m%d%H%M%S')
    image_filename = f'image_{timestamp}.jpg'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)

    # Analyze the image
    sentiment = ImageSentiment(image_path).analyze()
    attention = ImageAttention(image_path).analyze()
    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S')

    # Store in SQLite database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO image (timestamp, image_path, sentiment, attention) VALUES (?, ?, ?, ?)",
              (timestamp_str, image_path, sentiment, attention))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'sentiment': sentiment, 'attention': attention})

@app.route('/set_goal_ajax', methods=['POST'])
def set_goal_ajax():
    goal = request.form['goal']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO goals (date, goal) VALUES (?, ?)", (time.strftime('%Y-%m-%d'), goal))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/journal_ajax', methods=['POST'])
def journal_ajax():
    entry = request.form['journal_entry']
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO journal (timestamp, entry) VALUES (?, ?)", (timestamp, entry))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/report')
def report():
    try:
        # Fetch data from database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Get sentiment data
        c.execute("SELECT timestamp, sentiment FROM image")
        sentiment_data = c.fetchall()

        # Get attention data
        c.execute("SELECT timestamp, attention FROM image")
        attention_data = c.fetchall()

        # Get journal entries and goals for word cloud
        c.execute("SELECT entry FROM journal")
        journal_entries = c.fetchall()
        c.execute("SELECT goal FROM goals")
        goals = c.fetchall()
        conn.close()

        # Generate visualizations
        visualizer = Visualizer()
        visualizer.generate_sentiment_graph(sentiment_data)
        visualizer.generate_attention_graph(attention_data)
        text_data = ' '.join([entry[0] for entry in journal_entries]) + ' ' + ' '.join([goal[0] for goal in goals])
        visualizer.generate_word_cloud(text_data)

        return render_template('report.html')
    except Exception as e:
        print(f"Error generating report: {e}")
        return render_template('report.html', error="An error occurred while generating the report.")

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
