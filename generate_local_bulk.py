import json, random, subprocess, shutil, time
from pathlib import Path

# --- Configuration ---
MODEL = "gemma3:4b"                     # Use the model you pulled in Ollama
TOTAL = 1100                            # >1000 as requested
OUTPUT = "attractions_local.json"       # Output file
OLLAMA_PATH = shutil.which("ollama") or r"C:\Users\kilic\AppData\Local\Programs\Ollama\ollama.exe"

# Years within last 5 years
YEARS = [2021, 2022, 2023, 2024, 2025]

# Minimal prompt – forces strict JSON and coordinates as "lat,lon"
BASE_INSTRUCTIONS = (
    "Return STRICT JSON ONLY, no markdown fences, no extra text. "
    'Fields: "name", "city", "description", "coordinates". '
    'The "coordinates" must be a string "latitude,longitude". '
    "The description MUST contain the exact phrase: Opened in {year}."
)

def call_ollama(prompt: str) -> str:
    """Call Ollama CLI with the given prompt and return raw text output."""
    result = subprocess.run(
        [OLLAMA_PATH, "run", MODEL, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    return (result.stdout or "").strip()

def extract_json(text: str) -> dict | None:
    """Extract first JSON object from text and parse it safely."""
    try:
        # Some models may sometimes add text around JSON. Get first {...}
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            return None
        return json.loads(text[start:end])
    except Exception:
        return None

def valid_record(rec: dict) -> bool:
    """Validate required fields and year phrase."""
    required = ["name", "city", "description", "coordinates"]
    if not all(k in rec and isinstance(rec[k], str) and rec[k].strip() for k in required):
        return False
    # coordinates should look like "lat,lon"
    if "," not in rec["coordinates"]:
        return False
    # Require phrase Opened in 2021–2025
    if "Opened in 202" not in rec["description"]:
        return False
    return True

def make_prompt(year: int) -> str:
    return (
        f"{BASE_INSTRUCTIONS} "
        f'Generate ONE new attraction JSON for any city worldwide, '
        f'with a realistic name and description. Opened in {year}.'
    )

def main():
    if not OLLAMA_PATH:
        raise SystemExit("Ollama executable not found. Add it to PATH or set OLLAMA_PATH.")

    out = []
    seen = set()  # dedupe by (name, city)
    for i in range(1, TOTAL + 1):
        year = random.choice(YEARS)
        prompt = make_prompt(year)
        raw = call_ollama(prompt)
        rec = extract_json(raw)

        if rec and valid_record(rec):
            key = (rec["name"].strip().lower(), rec["city"].strip().lower())
            if key in seen:
                # duplicate – try again on next loop
                i -= 1
            else:
                seen.add(key)
                out.append(rec)
                print(f"[{len(out)}/{TOTAL}] OK  → {rec['name']}  ({rec['city']})")
        else:
            print(f"[?] Retry (invalid JSON or missing fields)")
            i -= 1  # try again

        # tiny pause to keep things stable
        time.sleep(0.05)

        if len(out) >= TOTAL:
            break

    Path(OUTPUT).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(out)} records to {OUTPUT}")

if __name__ == "__main__":
    main()
