CREATE TABLE students (
    netid                   TEXT PRIMARY KEY,
    name                    TEXT NOT NULL,
    school_year             TEXT,
    intro_programming       TEXT,
    skill_programming       SMALLINT,   -- 1-5
    skill_data_stats        SMALLINT,   -- 1-5
    skill_frontend_design   SMALLINT,   -- 1-5
    skill_business_pitch    SMALLINT,   -- 1-5
    working_style           TEXT,       -- '#NAME?' loaded as NULL
    interests               TEXT,
    semester_goal           TEXT,
    submitted_at            TIMESTAMPTZ
);

CREATE TABLE tools (
    tool_id   SERIAL PRIMARY KEY,
    name      TEXT UNIQUE NOT NULL
);

CREATE TABLE student_tools (
    netid     TEXT REFERENCES students(netid),
    tool_id   INT REFERENCES tools(tool_id),
    PRIMARY KEY (netid, tool_id)
);

CREATE TABLE availability (
    availability_id   SERIAL PRIMARY KEY,
    label              TEXT UNIQUE NOT NULL
);

CREATE TABLE student_availability (
    netid             TEXT REFERENCES students(netid),
    availability_id   INT REFERENCES availability(availability_id),
    PRIMARY KEY (netid, availability_id)
);
