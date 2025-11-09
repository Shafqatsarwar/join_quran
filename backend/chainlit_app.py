"""
Chainlit app that forwards user messages to an external Gemini (Google Generative AI) client.

Notes:
- This file uses `google-generativeai` (pip package name: `google-generativeai`).
- Set the env var GOOGLE_API_KEY before running.
- Run with: `chainlit run backend/chainlit_app.py --port 8001`

This is a minimal example — adapt prompts, streaming, safety, and error handling for production.
"""
import os
import json
import chainlit as cl
from chainlit.types import Message

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Prefer the official client if available, otherwise we'll fall back to the REST API via httpx.
try:
    import google.generativeai as genai
except Exception:
    genai = None

try:
    import httpx
except Exception:
    httpx = None

if genai and GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception:
        # configure may not exist in some versions; ignore and continue — we'll catch errors later
        pass


async def _call_gemini_via_client(prompt: str) -> str:
    """Try calling Gemini via the google.generativeai client."""
    try:
        # The exact API surface can change between library versions. We attempt a couple of common calls.
        # 1) generate_text
        if hasattr(genai, 'generate_text'):
            res = genai.generate_text(model="models/text-bison-001", input=prompt)
            # Try to extract text robustly
            if isinstance(res, dict):
                return res.get('candidates', [{}])[0].get('content', '') or str(res)
            return getattr(res, 'text', str(res))

        # 2) If client exposes a different method, try the 'chat' pattern
        if hasattr(genai, 'chat'):
            res = genai.chat(model="models/chat-bison-001", messages=[{"role": "user", "content": prompt}])
            if isinstance(res, dict):
                return res.get('candidates', [{}])[0].get('content', '') or str(res)
            return str(res)

        return "[Gemini client available but no known call matched the library version]"
    except Exception as e:
        return f"[Error calling Gemini client] {e}"


async def _call_gemini_via_rest(prompt: str) -> str:
    """Fallback: call the Google Generative Language REST API using httpx.

    Docs: https://developers.generativeai.google
    """
    if not httpx:
        return (
            "[httpx not installed] Cannot call Gemini via REST. Install httpx and set GOOGLE_API_KEY."
        )

    api_key = GOOGLE_API_KEY
    if not api_key:
        return (
            "[No API key] Set GOOGLE_API_KEY in your environment to enable Gemini calls."
        )

    # Example: text generation endpoint (v1beta2). Model name may be different for chat vs text.
    url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate?key={api_key}"
    payload = {
        "prompt": {"text": prompt},
        "temperature": 0.2,
        "maxOutputTokens": 512
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            # Response structure: { "candidates": [ {"output": "..."}, ... ] }
            if isinstance(data, dict):
                candidates = data.get('candidates') or []
                if candidates:
                    # Try a few common keys
                    cand = candidates[0]
                    return cand.get('output') or cand.get('content') or cand.get('text') or str(cand)
                # Some API shapes may put the text under 'output' or 'candidates'
                return data.get('output', str(data))
            return str(data)
    except Exception as e:
        return f"[Error calling Gemini REST API] {e}"


@cl.on_message
async def on_user_message(msg: Message):
    user_text = msg.content

    # Try client first, then REST, then fallback placeholder.
    if genai and GOOGLE_API_KEY:
        reply = await _call_gemini_via_client(user_text)
    elif httpx and GOOGLE_API_KEY:
        reply = await _call_gemini_via_rest(user_text)
    else:
        reply = (
            "[Chainlit placeholder reply] — Gemini is not configured or required packages are missing.\n"
            "Set GOOGLE_API_KEY and install `google-generativeai` (or `httpx`) to enable LLM responses."
        )

    await cl.send_message(reply)
