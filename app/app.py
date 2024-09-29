from flask import Flask, render_template, request, jsonify, url_for
from image_sentiment import ImageSentiment
from image_attention import ImageAttention
from visualizer import Visualizer
from goal import Goal
import sqlite3
import time
import base64
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT goal FROM goals")
    goals = c.fetchall()
    conn.close()

    all_goals_text = "I want to be healthy and peaceful"
    quote, image = Goal().get_motivation(all_goals_text, default=True)

    image_url = url_for('static', filename='images/' + image)
    return render_template('index.html', quote=quote, image_url=image_url)

@app.route('/capture_image', methods=['POST'])
def capture_image():
    attention_analyzer = ImageAttention()
    sentiment_analyzer = ImageSentiment()
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
    try:
        sentiment_result = sentiment_analyzer.analyze(image_path)
    except Exception as e:
        print(f"Error analyzing image sentiment: {e}")
        sentiment_result = 'Neutral'
    try:
        attention_result = attention_analyzer.analyze(image_path)
    except Exception as e:
        print(f"Error analyzing image attention: {e}")
        attention_result = 'Focused'
    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S')

    # Store in SQLite database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO image (timestamp, image_path, sentiment, attention) VALUES (?, ?, ?, ?)",
              (timestamp_str, image_path, sentiment_result, attention_result))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'sentiment': sentiment_result, 'attention': attention_result})

@app.route('/set_goal_ajax', methods=['POST'])
def set_goal_ajax():
    goal = request.form['goal']

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO goals (date, goal) VALUES (?, ?)", (time.strftime('%Y-%m-%d'), goal))
    conn.commit()
    goal_id = c.lastrowid  # Get the ID of the newly inserted goal
    conn.close()

    return jsonify({'status': 'success', 'goal': {'id': goal_id, 'goal': goal}})

@app.route('/get_goals', methods=['GET'])
def get_goals():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, goal FROM goals")
    goals = c.fetchall()
    conn.close()

    # Convert to list of dictionaries
    goals_list = [{'id': row['id'], 'goal': row['goal']} for row in goals]
    return jsonify({'goals': goals_list})

@app.route('/delete_goal', methods=['POST'])
def delete_goal():
    goal_id = request.form['goal_id']

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/update_motivation', methods=['GET'])
def update_motivation():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT goal FROM goals")
    goals = c.fetchall()
    conn.close()

    # Concatenate all goals
    if goals:
        all_goals_text = ' '.join([row['goal'] for row in goals])
        quote, image = Goal().get_motivation(all_goals_text, default=False)
    else:
        all_goals_text = 'I want to be healthy and peaceful'
        quote, image = Goal().get_motivation(all_goals_text, default=True)

    image_url = url_for('static', filename='images/' + image)
    return jsonify({'quote': quote, 'image_url': image_url})

@app.route('/journal_ajax', methods=['POST'])
def journal_ajax():
    entry = request.form['journal_entry']
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO journal (timestamp, entry) VALUES (?, ?)", (timestamp, entry))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/report')
def report():
    try:
        cache_buster = random.randint(1, 10000)
        # Fetch data from database
        conn = get_db_connection()
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
        text_data = ' '.join([entry['entry'] for entry in journal_entries]) + ' ' + ' '.join([goal['goal'] for goal in goals])
        visualizer.generate_word_cloud(text_data)

        return render_template('report.html', cache_buster=cache_buster)
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
