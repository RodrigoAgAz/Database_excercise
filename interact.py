import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

SAMPLE_QUERIES = [
    ("Row counts per table", """
        SELECT 'students' AS table_name, count(*) FROM students
        UNION ALL SELECT 'tools', count(*) FROM tools
        UNION ALL SELECT 'student_tools', count(*) FROM student_tools
        UNION ALL SELECT 'availability', count(*) FROM availability
        UNION ALL SELECT 'student_availability', count(*) FROM student_availability;
    """),
    ("Students per school year", """
        SELECT school_year, count(*) AS n_students
        FROM students
        GROUP BY school_year
        ORDER BY n_students DESC;
    """),
    ("Students per tool", """
        SELECT t.name, count(*) AS n_students
        FROM student_tools st
        JOIN tools t ON st.tool_id = t.tool_id
        GROUP BY t.name
        ORDER BY n_students DESC;
    """),
    ("Average skill ratings", """
        SELECT
            round(avg(skill_programming), 2)     AS avg_programming,
            round(avg(skill_data_stats), 2)       AS avg_data_stats,
            round(avg(skill_frontend_design), 2)  AS avg_frontend_design,
            round(avg(skill_business_pitch), 2)   AS avg_business_pitch
        FROM students;
    """),
    ("Students who know Python AND SQL", """
        SELECT s.name
        FROM students s
        WHERE s.netid IN (
            SELECT st.netid FROM student_tools st
            JOIN tools t ON st.tool_id = t.tool_id
            WHERE t.name = 'Python'
        )
        AND s.netid IN (
            SELECT st.netid FROM student_tools st
            JOIN tools t ON st.tool_id = t.tool_id
            WHERE t.name = 'SQL'
        );
    """),
    ("Most common availability slots", """
        SELECT a.label, count(*) AS n_students
        FROM student_availability sa
        JOIN availability a ON sa.availability_id = a.availability_id
        GROUP BY a.label
        ORDER BY n_students DESC;
    """),
]


def print_results(cur):
    rows = cur.fetchall()
    if cur.description:
        colnames = [desc[0] for desc in cur.description]
        print(colnames)
    for row in rows:
        print(row)
    if not rows:
        print("(no rows)")


def main():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    print("Connected. Sample queries:")
    for i, (label, _) in enumerate(SAMPLE_QUERIES, start=1):
        print(f"  {i}. {label}")
    print("Type a number to run a sample query, or type any SQL directly.")
    print("Type 'quit' or 'exit' to leave.\n")

    while True:
        try:
            user_input = input("sql> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break

        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(SAMPLE_QUERIES):
                label, sql = SAMPLE_QUERIES[idx]
                print(f"-- {label} --")
                try:
                    cur.execute(sql)
                    print_results(cur)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("No such sample query number.")
            continue

        try:
            cur.execute(user_input)
            if cur.description:
                print_results(cur)
            else:
                print("OK.")
        except Exception as e:
            print(f"Error: {e}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
