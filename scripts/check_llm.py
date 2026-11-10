"""Smoke test for your LLM API key (standard library only).

Usage, from the repository root:
    python scripts/check_llm.py deepseek
    python scripts/check_llm.py qwen

Reads DEEPSEEK_* / QWEN_* values from .env (copy .env.example first).
Prints the model's reply and token usage; never prints your key.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROVIDERS = {
    "deepseek": ("DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"),
    "qwen": ("QWEN_API_KEY", "QWEN_BASE_URL", "QWEN_MODEL"),
}


def load_env(path: str = ".env") -> None:
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "deepseek"
    if name not in PROVIDERS:
        sys.exit(f"Unknown provider '{name}'. Choose one of: {', '.join(PROVIDERS)}")
    load_env()
    key_var, base_var, model_var = PROVIDERS[name]
    key = os.environ.get(key_var, "")
    base = os.environ.get(base_var, "").rstrip("/")
    model = os.environ.get(model_var, "")
    if not (key and base and model):
        sys.exit(f"Set {key_var}, {base_var} and {model_var} in .env (copy .env.example first).")

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with the single word OK."}],
        "max_tokens": 5,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    except Exception as e:  # network down, DNS, timeout
        sys.exit(f"Request failed: {e}")

    print("Reply:", data["choices"][0]["message"]["content"].strip())
    print("Tokens used:", data.get("usage", {}).get("total_tokens", "n/a"))


if __name__ == "__main__":
    main()
