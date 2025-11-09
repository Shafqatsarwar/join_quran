# Join Quran - Demo (Next.js frontend + Python backend + Chainlit chat)

This repository contains a starter full-stack project that recreates the structure and functionality of a site like joinquran.com for local testing and development.

IMPORTANT: This is a scaffold and demo. The user requested a copy of www.joinquran.com — this repo implements an inspired, minimal reproduction for learning and local testing. Ensure you have the rights or permission to reproduce any protected content before publishing.

## What I added

- `frontend/` — Next.js 13 app (React) with a simple landing page, components and a Chat button that opens Chainlit UI.
- `backend/` — Python FastAPI app (`backend/app/main.py`) that returns site metadata and a contact endpoint. Also a Chainlit app (`backend/chainlit_app.py`) to run a chat UI powered by an external LLM (Gemini).
- `backend/requirements.txt` — Python dependencies list.

## High-level architecture

- Frontend (Next.js) runs on port 3000 (dev) and calls the backend API for site data.
- FastAPI backend serves API endpoints on port 8000 (uvicorn).
- Chainlit runs as a separate service (suggested port 8001) and provides an interactive chat UI. Chainlit will use the Gemini (Google Generative AI) external client when configured with `GOOGLE_API_KEY`.

## Assumptions & notes

- Assumed you have permission to replicate content and styling you need from the original site. If not, replace copyrighted text and assets.
- Gemini client integration uses the `google-generativeai` Python package. The sample code is a minimal example and may require API/client updates depending on library versions.
- Chainlit is set up for local development only. For production, review authentication, rate limits, and hosting choices.

## Environment variables

Create a `.env` file in the `backend/` directory or export env vars in your shell.

- `GOOGLE_API_KEY` — API key for Google Generative AI (Gemini). Required for real LLM responses in Chainlit.
- (Optional) `NEXT_PUBLIC_BACKEND_URL` — point frontend to backend (default: `http://localhost:8000`).
- (Optional) `NEXT_PUBLIC_CHAINLIT_URL` — URL of running Chainlit UI (default: `http://localhost:8001`).

## Local development (Windows cmd examples)

1) Start the backend API (FastAPI)

   cd backend
   python -m pip install -r requirements.txt
   set GOOGLE_API_KEY=your_key_here
   uvicorn backend.app.main:app --reload --port 8000

2) Start Chainlit (chat UI)

   # In another terminal
   cd backend
   set GOOGLE_API_KEY=your_key_here
   # Make sure chainlit is installed (it's included in requirements). Run:
   chainlit run backend/chainlit_app.py --port 8001

   Open the Chainlit UI (http://localhost:8001) and test the chat.

3) Start the frontend (Next.js)

   # In another terminal
   cd frontend
   npm install
   set NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   set NEXT_PUBLIC_CHAINLIT_URL=http://localhost:8001
   npm run dev

   Open http://localhost:3000 to view the site. Click "Open Chat (Chainlit UI)" to open the chat.

## Testing the pieces

- Site data: GET http://localhost:8000/api/site — returns demo site metadata.
- Contact (demo): POST http://localhost:8000/api/contact with JSON {name,email,message}.
- Chainlit chat: Open the Chainlit UI and send messages. If `GOOGLE_API_KEY` is set and `google-generativeai` is installed, messages will be forwarded to Gemini.

## Pushing to GitHub

1) Initialize git (if not already):

   git init
   git add .
   git commit -m "Initial scaffold: Next.js frontend + FastAPI backend + Chainlit chat"
   git remote add origin https://github.com/<your-username>/join_quran.git
   git push -u origin master

Replace `<your-username>` and the repo URL to point to your repository.

## Deployment suggestions

- Frontend: Deploy `frontend/` (Next.js) to Vercel. Connect the GitHub repo and set environment variables in Vercel (NEXT_PUBLIC_BACKEND_URL).
- Backend: Vercel does not natively host long-running Python processes like Chainlit. Options:
  - Deploy the FastAPI backend to Render / Railway / Fly / Heroku and set the deployed URL as `NEXT_PUBLIC_BACKEND_URL` in Vercel.
  - Deploy Chainlit separately (it requires a server that supports long-running websockets). Consider Render/Railway or a VM.

For a simple flow: deploy frontend to Vercel, deploy backend (FastAPI + Chainlit) to Render/Railway, then update env vars in Vercel to point to your backend/chainlit hosts.

## Next steps & improvements

- Flesh out UI components and styling to closely match the original site, ensuring you have permission to copy assets.
- Add authentication, admin pages, class booking flows, database persistence (Postgres), and payments if required.
- Add unit tests, CI (GitHub Actions), and deployment pipelines.

## Verification / quality gates

- Build: run `npm run build` in `frontend/` to test Next.js build (after installing deps).
- Lint/Typecheck: not included in this scaffold — add ESLint/TypeScript if desired.
- Tests: none included in this scaffold; add pytest/unittest for backend and Jest/React Testing Library for frontend.

---

If you'd like, I can:

- Wire up a database and implement an authentication flow.
- Replace the placeholder Gemini calls with a working, tested integration (I will need your Gemini credentials or a sandbox API key).
- Add CI and automatic deploy to Vercel + Render.

Tell me which next step you want me to take and I'll continue.
