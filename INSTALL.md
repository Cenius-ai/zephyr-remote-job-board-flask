# Zephyr — Installation Guide

## Step 1: Install dependencies

```bash
bash install.sh
```

This will:
- Upgrade pip and install requirements
- Seed the database with 55 realistic remote tech job listings

## Step 2: Run the server

```bash
python3 app.py
```

The server starts on **http://0.0.0.0:5000** (honors `$PORT`).

## Step 3: Verify

Open `http://localhost:5000` in your browser. You should see:

- A list of 55+ remote tech jobs
- Working filter form (title, company, tech stack, remote type, salary)
- A dark mode toggle (sun/moon icon in the top-right or bottom tab)
- Click any job to see its detail page
- Visit `/about` for the about page

## Data

The seed creates:

- **40 technology tags** (Python, React, Docker, Kubernetes, etc.)
- **55 job listings** across 30 companies with realistic descriptions, salary ranges, and remote types
- Jobs posted across the last 30 days (relative to when seed runs)

To re-seed: delete `instance/app.db` and run `python3 seed.py`.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `5000` | Server port |
| `SECRET_KEY` | (dev default) | Flask session secret |
| `DATABASE_URL` | `sqlite:///app.db` | Database connection |
