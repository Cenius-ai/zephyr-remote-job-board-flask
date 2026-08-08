# Usage Guide

Once the development server is running (default: `http://localhost:5000`), you can use the job board through a web browser or by sending HTTP requests.

## Web Interface

### Home — Job Listing (`/`)

- Shows paginated remote tech jobs (12 per page).
- **Filters**: Use the search form to narrow results by:
  - `title` – keyword in job title
  - `company` – company name (select from dropdown)
  - `tech_stack` – desired technology (select from available tags)
  - `remote_type` – e.g., "Remote", "Hybrid"
  - `salary_min` / `salary_max` – integer values
- Click any job title to view its details.

### Job Detail (`/jobs/<id>`)

Displays full information about a single job: company, location, remote type, salary, description, and associated tech tags.

### About (`/about`)

Provides a short description of the Zephyr project.

### Hello (`/hello`)

A minimal health‑check / sanity route that returns the text `Hello`.

## JSON API

All API endpoints are prefixed with `/api` and return JSON.

### List Jobs – `GET /api/jobs`

Accepts the same query parameters as the web home page plus `page` and `per_page` (max 50).

**Example**:

```bash
curl "http://localhost:5000/api/jobs?title=python&remote_type=Remote&page=1"
```

Response contains `jobs`, `page`, `per_page`, `total`, `pages`.

### Single Job – `GET /api/jobs/<id>`

```bash
curl http://localhost:5000/api/jobs/1
```

Returns the job object with its tags, or a 404 error if not found.

### List Companies – `GET /api/companies`

```bash
curl http://localhost:5000/api/companies
```

Returns a JSON array of distinct company names.

### List Tags – `GET /api/tags`

```bash
curl http://localhost:5000/api/tags
```

Returns a JSON array of all technology tag names.

## Seeded Data

On first launch (when the database is empty), the app seeds 55 realistic job postings using `faker`. The data set includes various remote‑tech companies and technical tags. Restarting the app will not overwrite existing data – only a fresh `instance/app.db` triggers re‑seeding.