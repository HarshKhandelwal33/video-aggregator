from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    search_query = request.args.get('q')
    conn = get_db()
    if search_query:
        videos = conn.execute("SELECT * FROM videos WHERE title LIKE ?", ('%' + search_query + '%',)).fetchall()
    else:
        videos = conn.execute("SELECT * FROM videos ORDER BY click_count DESC").fetchall()
    return render_template('index.html', videos=videos)

@app.route('/click/<int:video_id>')
def click(video_id):
    conn = get_db()
    conn.execute("UPDATE videos SET click_count = click_count + 1 WHERE id = ?", (video_id,))
    conn.commit()
    url = conn.execute("SELECT url FROM videos WHERE id = ?", (video_id,)).fetchone()['url']
    return redirect(url)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db()
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        thumbnail = request.form['thumbnail']
        conn.execute("INSERT INTO videos (title, url, thumbnail) VALUES (?, ?, ?)", (title, url, thumbnail))
        conn.commit()
    videos = conn.execute("SELECT * FROM videos ORDER BY id DESC").fetchall()
    return render_template('admin.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)