import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


def run(cur, label, sql):
    print(f"\n-- {label} --")
    cur.execute(sql)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    print(colnames)
    for row in rows:
        print(row)


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    run(cur, "total student count", "SELECT count(*) FROM students;")

    run(cur, "sample students", "SELECT name, school_year FROM students LIMIT 5;")

    run(
        cur,
        "students per tool",
        """
        SELECT t.name, COUNT(*) AS n_students
        FROM student_tools st
        JOIN tools t ON st.tool_id = t.tool_id
        GROUP BY t.name
        ORDER BY n_students DESC;
        """,
    )

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
