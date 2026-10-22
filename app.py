import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM students ORDER BY name;")
    names = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("index.html", names=names)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
