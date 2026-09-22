"""Part 2 -- token measurement using Google Gemini (gemini-3.6-flash).

Counts tokens using the free count_tokens API from Google AI Studio.
Key is safely loaded from .env (GEMINI_API_KEY or GOOGLE_API_KEY).

Usage:
    python part2_measure.py
    python part2_measure.py --call
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv
from google import genai

from texts import CORPUS, LANGUAGES

load_dotenv()

OUTPUT_PATH = Path(__file__).with_name("measurements.json")
DEFAULT_MODEL = "gemini-3.6-flash"
MAX_TOKENS = 2048


def count_tokens(client: genai.Client, model_id: str, text: str) -> int:
    """Return input token count for single text using Gemini tokenizer."""
    response = client.models.count_tokens(
        model=model_id,
        contents=text,
    )
    return response.total_tokens


def count_request_tokens(client: genai.Client, model_id: str, lang: str) -> int:
    """Return input token count for system_prompt + complaint together."""
    response = client.models.count_tokens(
        model=model_id,
        contents=[
            CORPUS["system_prompt"][lang],
            CORPUS["complaint"][lang],
        ],
    )
    return response.total_tokens


def one_real_request(
    client: genai.Client, model_id: str, lang: str
) -> Optional[Dict[str, int]]:
    """Send one real request to Gemini to measure actual output tokens."""
    response = client.models.generate_content(
        model=model_id,
        contents=CORPUS["complaint"][lang],
        config={
            "max_output_tokens": MAX_TOKENS,
            "system_instruction": CORPUS["system_prompt"][lang],
        },
    )

    if not response.text:
        print("  model returned an empty response")
        return None

    print("  --- answer ---")
    print("  " + response.text.replace("\n", "\n  "))

    usage = response.usage_metadata
    in_tok = usage.prompt_token_count or 0
    out_tok = usage.candidates_token_count or 0
    print(f"  billed: {in_tok} in, {out_tok} out")
    return {"input_tokens": in_tok, "output_tokens": out_tok}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"which model to test (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--call",
        action="store_true",
        help="also generate an answer in each language",
    )
    args = parser.parse_args()
    model_id = args.model

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(
            "ERROR: GEMINI_API_KEY or GOOGLE_API_KEY is not set in your .env file!",
            file=sys.stderr,
        )
        return 1

    try:
        client = genai.Client(api_key=api_key)
    except Exception as exc:
        print(f"Could not build Gemini client: {exc}", file=sys.stderr)
        return 1

    counts: Dict[str, Dict[str, int]] = {}
    print(f"counting tokens on Google {model_id} (free, no model run)")

    try:
        for item_id, versions in CORPUS.items():
            counts[item_id] = {
                lang: count_tokens(client, model_id, versions[lang])
                for lang in LANGUAGES
            }
            row = "  ".join(f"{lang}={counts[item_id][lang]}" for lang in LANGUAGES)
            print(f"  {item_id:<14} {row}")

        request_tokens: Dict[str, int] = {
            lang: count_request_tokens(client, model_id, lang) for lang in LANGUAGES
        }
        row = "  ".join(f"{lang}={request_tokens[lang]}" for lang in LANGUAGES)
        print(f"  {'request':<14} {row}  (system + complaint, one call)")

    except Exception as exc:
        print(f"API error: {exc}", file=sys.stderr)
        return 1

    billed: Dict[str, Dict[str, int]] = {}
    if args.call:
        print(f"\nanswering the same complaint on {model_id}, in each language:")
        for lang in LANGUAGES:
            print(f"\n[{lang}]")
            try:
                result = one_real_request(client, model_id, lang)
            except Exception as exc:
                print(f"API error on call: {exc}", file=sys.stderr)
                return 1
            if result is not None:
                billed[lang] = result

    payload = {
        "model": args.model,
        "model_id": model_id,
        "token_counts": counts,
        "request_tokens": request_tokens,
        "one_request_billed": billed or None,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {OUTPUT_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())