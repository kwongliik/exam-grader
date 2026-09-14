-- Phase 1: run this in your Supabase / Neon SQL editor.
-- (The backend also creates this automatically on startup, so this file
-- is mainly here so you can see the structure and re-run it manually if needed.)

CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    student_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    score NUMERIC NOT NULL,
    max_score NUMERIC NOT NULL,
    extracted_answer TEXT,
    feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Phase 2 (not needed yet): tables to support performance analytics later,
-- e.g. tagging each question with a topic so you can find class weak spots.
--
-- CREATE TABLE IF NOT EXISTS students (
--     student_id TEXT PRIMARY KEY,
--     name TEXT NOT NULL,
--     class_name TEXT
-- );
--
-- CREATE TABLE IF NOT EXISTS questions (
--     question_id TEXT PRIMARY KEY,
--     exam_name TEXT,
--     topic TEXT,
--     max_score NUMERIC
-- );
