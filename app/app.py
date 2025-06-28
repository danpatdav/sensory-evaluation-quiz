from flask import Flask, render_template, request, jsonify
import sqlite3, json

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('guesses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            aroma_number INTEGER,
            guess TEXT,
            correct BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Load correct aromas
with open('aromas.json') as f:
    aromas = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        name = request.form['name']
        conn = sqlite3.connect('guesses.db')
        cursor = conn.cursor()

        score = 0
        for number in range(1, 36):
            guess = request.form.get(f'aroma_{number}', '').strip().lower()
            correct_answer = aromas.get(str(number), '').lower()
            correct = guess == correct_answer
            score += correct

            cursor.execute('INSERT INTO guesses (name, aroma_number, guess, correct) VALUES (?, ?, ?, ?)',
                           (name, number, guess, correct))

            results.append({
                'number': number,
                'your_guess': guess.title(),
                'correct_answer': correct_answer.title(),
                'correct': correct
            })

        conn.commit()

        cursor.execute('SELECT name, SUM(correct) as total_score FROM guesses GROUP BY name ORDER BY total_score DESC')
        leaderboard = cursor.fetchall()

        conn.close()

        return render_template('results.html', results=results, score=score, leaderboard=leaderboard)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
