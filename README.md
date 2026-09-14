# Exam Grader — Phase 1 MVP Tutorial

This builds a simple web app: you upload a photo of a student's handwritten
answer, Google Gemini reads and grades it against your marking scheme, and
the result is saved to a database.

Project layout:
```
exam-grader/
  backend/       -> Python FastAPI server
  frontend/      -> plain HTML/JS upload page
  database/      -> SQL schema reference
  .gitignore
  README.md
```

---

## Step 1: GitHub repo + local project

1. On GitHub, create a new empty repository, e.g. `exam-grader`.
2. On your computer, open a terminal and clone it:
   ```
   git clone https://github.com/YOUR_USERNAME/exam-grader.git
   cd exam-grader
   ```
3. Copy all the files from this project into that folder (keeping the same
   `backend/`, `frontend/`, `database/` structure).
4. Open the folder in VS Code:
   ```
   code .
   ```
5. Commit and push what you have so far:
   ```
   git add .
   git commit -m "Initial project structure"
   git push
   ```

---

## Step 2: Get a Gemini API key and set up the backend

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and create a
   free API key.
2. In `backend/`, copy `.env.example` to a new file named `.env`:
   ```
   cd backend
   cp .env.example .env
   ```
3. Open `.env` and paste your key:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```
   (Leave `DATABASE_URL` for Step 3.)
4. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate      # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. `main.py` is your grading server. Its one important endpoint is
   `POST /grade`, which takes an image + question + marking scheme, sends
   them to Gemini, and returns a score, transcribed answer, and feedback as
   JSON. Read through it — the prompt sent to Gemini is fully visible and
   editable, so you can adjust grading instructions/tone later.

---

## Step 3: Set up a free relational database

1. Go to [Supabase](https://supabase.com) (or [Neon](https://neon.tech)) and
   create a free account + a new project.
2. Once created, find your **connection string** (Supabase: Project Settings
   → Database → Connection string → URI). It looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres
   ```
3. Paste it into `backend/.env` as `DATABASE_URL`.
4. Optional: open the SQL editor in Supabase/Neon and run the contents of
   `database/schema.sql` to create the `results` table manually. (The
   backend also creates it automatically the first time it starts, so this
   step is just for visibility.)

---

## Step 4: Run the backend and test it

1. From the `backend/` folder, with your virtual environment active:
   ```
   uvicorn main:app --reload
   ```
2. Visit `http://localhost:8000` in your browser — you should see
   `{"status": "ok"}`.
3. Visit `http://localhost:8000/docs` — FastAPI gives you an interactive
   test page. Try the `/grade` endpoint there: upload a photo of a
   handwritten answer, fill in a question, a marking scheme, and a max
   score, and run it. Check that a row appears in your `results` table in
   Supabase/Neon (Table Editor).

---

## Step 5: Run the frontend

1. Open `frontend/index.html` directly in your browser (double-click it, or
   use VS Code's "Live Server" extension for auto-reload).
2. Fill in the form and upload a handwritten answer photo. It calls your
   local backend at `http://localhost:8000/grade` and displays the score,
   transcription, and feedback.
3. This is deliberately plain — no framework, no build step — so you can see
   the whole request/response flow in one file (`frontend/index.html`).

---

## Step 6: Deploy for free with auto-redeploy from GitHub

**Backend (Render, free tier):**
1. Push your code to GitHub (`git push`).
2. On [Render](https://render.com), create a new **Web Service**, connect
   your GitHub repo, and set:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add your `GEMINI_API_KEY` and `DATABASE_URL` as environment variables in
   Render's dashboard (never commit `.env` — it's already in `.gitignore`).
4. Deploy. Render gives you a public URL like
   `https://exam-grader-backend.onrender.com`.

**Frontend (Vercel or Netlify, free tier):**
1. On [Vercel](https://vercel.com), import the same GitHub repo, set the
   root directory to `frontend`, and deploy.
2. In `frontend/index.html`, change `API_URL` to your Render backend URL,
   commit, and push.

From here on, every `git push` to your main branch automatically redeploys
both the backend and frontend — matching your VS Code → GitHub → live site
workflow.

---

## What's next (Phase 2 — not built yet)

Once this MVP works end-to-end for one student and one question:
- Add `students` and `questions` tables (already sketched, commented out,
  in `database/schema.sql`) so you can tag each question with a topic.
- Support uploading a whole class's scripts in one batch.
- Add a simple dashboard page that runs SQL queries for class averages,
  per-question difficulty, and each student's weak topics over time.
