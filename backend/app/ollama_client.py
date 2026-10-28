import httpx

OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "beam:cloud"


class OllamaError(Exception):
    """Raised when communication with Ollama fails."""


async def send_message(message: str) -> str:
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "user", "content": message},
        ],
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json=payload,
            )
            response.raise_for_status()

        data = response.json()
        return data["message"]["content"]

    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise OllamaError("Unable to get a response from Ollama") from exc