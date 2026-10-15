import csv
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
CSV_PATH = os.path.join(os.path.dirname(__file__), "class_dataset.csv")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

SKILL_COLUMNS = (
    "skill_programming",
    "skill_data_stats",
    "skill_frontend_design",
    "skill_business_pitch",
)


def clean(value):
    value = (value or "").strip()
    if value == "" or value == "#NAME?":
        return None
    return value


def split_multi(value):
    value = (value or "").strip()
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cur.execute(f.read())

    tool_ids = {}
    availability_ids = {}

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        cur.execute(
            """
            INSERT INTO students (
                netid, name, school_year, intro_programming,
                skill_programming, skill_data_stats,
                skill_frontend_design, skill_business_pitch,
                working_style, interests, semester_goal, submitted_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (netid) DO NOTHING
            """,
            (
                clean(row["netid"]),
                clean(row["name"]),
                clean(row["school_year"]),
                clean(row["intro_programming"]),
                *(clean(row[col]) for col in SKILL_COLUMNS),
                clean(row["working_style"]),
                clean(row["interests"]),
                clean(row["semester_goal"]),
                clean(row["submitted_at"]),
            ),
        )

        netid = clean(row["netid"])

        for tool in split_multi(row["tools"]):
            if tool not in tool_ids:
                cur.execute(
                    """
                    INSERT INTO tools (name) VALUES (%s)
                    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                    RETURNING tool_id
                    """,
                    (tool,),
                )
                tool_ids[tool] = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO student_tools (netid, tool_id) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (netid, tool_ids[tool]),
            )

        for label in split_multi(row["availability"]):
            if label not in availability_ids:
                cur.execute(
                    """
                    INSERT INTO availability (label) VALUES (%s)
                    ON CONFLICT (label) DO UPDATE SET label = EXCLUDED.label
                    RETURNING availability_id
                    """,
                    (label,),
                )
                availability_ids[label] = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO student_availability (netid, availability_id) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (netid, availability_ids[label]),
            )

    conn.commit()

    for table in ("students", "tools", "student_tools", "availability", "student_availability"):
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]} rows")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
