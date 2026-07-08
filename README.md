# Cars Dealership — Full Stack Application Development Capstone Project

A responsive web application for **Cars Dealership**, a national car retailer, where
visitors can browse dealer branches across the US, filter them by state, read reviews
(scored by sentiment), and — once registered/logged in — submit their own dealer
reviews.

## Architecture

| Component | Tech | Folder |
|---|---|---|
| Web app (frontend + backend) | Django + React (embedded SPA) | [`server/`](server) |
| Dealers & reviews microservice | Node.js/Express + MongoDB (Mongoose) | [`database/`](database) |
| Review sentiment analysis microservice | Flask + VADER sentiment | [`server/djangoapp/microservices/`](server/djangoapp/microservices) |

The Django app (`server/`) serves the built React SPA plus two flat static pages
(`server/frontend/static/About.html`, `Contact.html`). It talks to the two
microservices over HTTP using the `BACKEND_URL` and `SENTIMENT_ANALYZER_URL`
settings (see `server/djangoproj/settings.py`), so the same code runs unchanged
locally or in a deployment — only the env vars change.

## Running locally

```bash
# 1. Dealers/reviews microservice (Node + an ephemeral local MongoDB)
cd database
npm install
npm start                    # boots an in-memory MongoDB, seeds it, starts on :3030

# 2. Sentiment analysis microservice (Flask)
cd server
uv sync
uv run python djangoapp/microservices/app.py     # starts on :5050

# 3. Django app (in another terminal)
cd server
uv run python manage.py migrate
uv run python manage.py populate      # seeds CarMake/CarModel demo data
uv run python manage.py createsuperuser
BACKEND_URL=http://localhost:3030 SENTIMENT_ANALYZER_URL=http://localhost:5050 \
  uv run python manage.py runserver 0.0.0.0:8000
```

Then visit `http://localhost:8000/`.

To rebuild the React frontend after changing anything under `server/frontend/src`:

```bash
cd server/frontend
npm install
npm run build   # outputs into server/frontend/static/static/{css,js}
```

## Docker

Each service has its own `Dockerfile`, and `docker-compose.yml` at the repo root
wires all three together plus a real MongoDB container for a one-command local
stack: `docker compose up --build`.

## Deployment

The Django app, the dealers/reviews microservice, and the sentiment analyzer are
each deployed as independent web services. See `deploymentURL` for the live app.

## Submission evidence

All cURL outputs, terminal logs, and screenshots referenced in the course
submission live under [`submission_assets/`](submission_assets), and the
compiled answer sheet is `submission.pdf`.
