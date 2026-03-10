#!/usr/bin/env python3
"""
Instagram Video Analyzer using Google Gemini multimodal API.

Supports 4 analysis modes: design extraction, content analysis,
competitor analysis, and transcription. All modes output structured JSON.

Usage:
    GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \\
      python3 analyze_video.py --mode design --file video.mp4 --output design.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed", file=sys.stderr)
    print("Install with: pip install google-genai", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# ---------------------------------------------------------------------------
# Mode configuration
# ---------------------------------------------------------------------------

MODE_DEFAULTS = {
    "design": {"model": "gemini-2.5-pro", "lang": "en"},
    "content": {"model": "gemini-2.5-flash", "lang": "de"},
    "competitor": {"model": "gemini-2.5-flash", "lang": "de"},
    "transcribe": {"model": "gemini-2.5-flash", "lang": "en"},
}

PROMPTS = {
    "design": (
        "Analyze this video frame-by-frame and extract the exact design system. "
        "Respond in JSON only.\n\n"
        "Extract these 10 specific data points:\n"
        "1. background_color: Exact HEX value of the primary background\n"
        "2. colors: Array of all distinct colors used, each as {hex, usage, area_percentage}\n"
        "3. typography: Array of text elements, each as {text, font_family_guess, weight, style, size_relative_to_frame, color_hex}\n"
        "4. layout: {padding_top_pct, padding_bottom_pct, padding_left_pct, padding_right_pct, content_alignment}\n"
        "5. elements: Ordered array of visual elements from top to bottom, each as {type, position_y_pct, width_pct, description}\n"
        "6. animations: Array of {element_index, type, direction, duration_seconds, delay_seconds, easing}\n"
        "7. spacing: Array of gaps between consecutive elements in pixels (estimated for 1080x1920)\n"
        "8. images: Array of {position, size_pct, shape, has_shadow, description}\n"
        "9. text_content: All readable text in the video, in order of appearance\n"
        "10. duration_seconds: Total video duration"
    ),
    "content": (
        "Analysiere dieses Video und bewerte die Content-Struktur. "
        "Antworte ausschließlich in JSON.\n\n"
        "Analysiere diese 8 spezifischen Datenpunkte:\n"
        "1. hook: {type, text_if_any, visual_technique, duration_seconds, attention_score_1_to_10}\n"
        "2. scenes: Array von {start_seconds, end_seconds, description, transition_type}\n"
        "3. text_overlays: Array von {text, appear_seconds, disappear_seconds, position, style}\n"
        "4. audio: {has_music, has_voiceover, silence_segments, music_energy}\n"
        "5. pacing: {cuts_per_minute, information_density, rhythm_consistency}\n"
        "6. cta: {text, timestamp_seconds, type, visual_style} oder null\n"
        "7. watch_time_prediction: {predicted_retention_pct, reasoning, strongest_element, weakest_element}\n"
        '8. format_category: einer von [talking_head, b_roll, text_on_screen, split_screen, slideshow, mixed]'
    ),
    "competitor": (
        "Analysiere dieses Instagram-Video eines Competitors. "
        "Antworte ausschließlich in JSON.\n\n"
        "Analysiere diese 7 spezifischen Datenpunkte:\n"
        "1. hook_category: einer von [correction, identity_trigger, bold_claim, curiosity_gap, pain_point, other]\n"
        "2. hook_details: {opening_text, visual_technique, estimated_stop_scroll_power_1_to_10}\n"
        "3. format: {primary_format, secondary_elements, production_complexity_1_to_5}\n"
        "4. content_pillars: Array von Themen die angesprochen werden\n"
        "5. cta: {type, placement_seconds, text, visual_integration}\n"
        "6. differentiators: Array von {element, description, replicable_boolean}\n"
        "7. benchmark_signals: {estimated_save_worthiness_1_to_10, estimated_share_worthiness_1_to_10, controversy_level_1_to_5}"
    ),
    "transcribe": (
        "Transcribe this video with precise timestamps. Respond in JSON only.\n\n"
        "Return:\n"
        "1. language: detected language code (e.g., \"de\", \"en\")\n"
        "2. segments: Array of {start_seconds, end_seconds, text, speaker_id}\n"
        "3. non_speech: Array of {start_seconds, end_seconds, type, description}\n"
        "   (type: one of [music, sound_effect, silence, ambient])\n"
        "4. full_text: Complete transcription as a single string"
    ),
}


# ---------------------------------------------------------------------------
# Utilities (copied from ai-multimodal/scripts/gemini_batch_process.py)
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    """Log to stderr."""
    print(msg, file=sys.stderr)


def find_api_key() -> Optional[str]:
    """Find Gemini API key. Priority: env > skill .env > skills .env > .claude .env."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    if load_dotenv:
        script_dir = Path(__file__).parent
        skill_dir = script_dir.parent
        skills_dir = skill_dir.parent
        claude_dir = skills_dir.parent

        for env_dir in [skill_dir, skills_dir, claude_dir]:
            env_file = env_dir / ".env"
            if env_file.exists():
                load_dotenv(env_file)
                api_key = os.getenv("GEMINI_API_KEY")
                if api_key:
                    return api_key

    return None


def get_mime_type(file_path: str) -> str:
    """Determine MIME type from file extension."""
    ext = Path(file_path).suffix.lower()
    mime_types = {
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".avi": "video/x-msvideo",
        ".webm": "video/webm",
        ".mkv": "video/x-matroska",
        ".flv": "video/x-flv",
        ".wmv": "video/x-ms-wmv",
        ".3gpp": "video/3gpp",
        ".mpeg": "video/mpeg",
        ".mpg": "video/mpeg",
        ".m4a": "audio/mp4",
    }
    return mime_types.get(ext, "application/octet-stream")


def upload_file(client: genai.Client, file_path: str, verbose: bool = False) -> Any:
    """Upload file to Gemini Files API. Polls until processing is done."""
    if verbose:
        _log(f"Uploading {file_path}...")

    myfile = client.files.upload(file=file_path)

    mime_type = get_mime_type(file_path)
    if mime_type.startswith("video/") or mime_type.startswith("audio/"):
        max_wait = 300
        elapsed = 0
        while myfile.state.name == "PROCESSING" and elapsed < max_wait:
            time.sleep(2)
            myfile = client.files.get(name=myfile.name)
            elapsed += 2
            if verbose and elapsed % 10 == 0:
                _log(f"  Processing... {elapsed}s")

        if myfile.state.name == "FAILED":
            raise ValueError(f"File processing failed: {file_path}")
        if myfile.state.name == "PROCESSING":
            raise TimeoutError(f"Processing timeout after {max_wait}s: {file_path}")

    if verbose:
        _log(f"  Uploaded: {myfile.name}")

    return myfile


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze_video(
    client: genai.Client,
    file_path: str,
    mode: str,
    model: str,
    verbose: bool = False,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """Analyze a video file using the specified mode. Returns parsed JSON."""
    prompt = PROMPTS[mode]
    path = Path(file_path)
    file_size = path.stat().st_size
    use_file_api = file_size > 20 * 1024 * 1024

    if verbose:
        _log(f"File: {file_path} ({file_size / 1024 / 1024:.1f} MB)")
        _log(f"Mode: {mode} | Model: {model}")
        _log(f"Upload: {'Files API' if use_file_api else 'inline'}")

    for attempt in range(max_retries):
        try:
            if use_file_api:
                myfile = upload_file(client, file_path, verbose)
                content = [prompt, myfile]
            else:
                with open(path, "rb") as f:
                    file_bytes = f.read()
                mime_type = get_mime_type(file_path)
                content = [
                    prompt,
                    types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                ]

            config = types.GenerateContentConfig(
                response_mime_type="application/json",
            )

            response = client.models.generate_content(
                model=model,
                contents=content,
                config=config,
            )

            result = json.loads(response.text)
            result["_meta"] = {
                "mode": mode,
                "model": model,
                "file": str(path.name),
                "file_size_mb": round(file_size / 1024 / 1024, 1),
            }
            return result

        except json.JSONDecodeError:
            if verbose:
                _log(f"  Warning: Response was not valid JSON, attempt {attempt + 1}")
            if attempt == max_retries - 1:
                return {
                    "error": "Response was not valid JSON",
                    "raw_response": response.text[:2000] if response else "",
                    "_meta": {"mode": mode, "model": model, "file": str(path.name)},
                }

        except Exception as e:
            if attempt == max_retries - 1:
                return {
                    "error": str(e),
                    "_meta": {"mode": mode, "model": model, "file": str(path.name)},
                }
            wait_time = 2 ** attempt
            if verbose:
                _log(f"  Retry {attempt + 1} after {wait_time}s: {e}")
            time.sleep(wait_time)

    return {"error": "Max retries exceeded"}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Instagram Video Analyzer (Gemini API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --mode design --file video.mp4 --output design.json\n"
            "  %(prog)s --mode content --file reel.mp4\n"
            "  %(prog)s --mode transcribe --file story.mp4 --output transcript.json\n"
            "  %(prog)s --mode competitor --file competitor.mp4 --dry-run\n"
            "\n"
            "API Key:\n"
            "  GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) "
            "python3 %(prog)s ...\n"
        ),
    )

    inp = parser.add_argument_group("Input")
    inp.add_argument(
        "--file", "-f", required=True,
        help="Path to video file to analyze",
    )
    inp.add_argument(
        "--mode", "-m", required=True,
        choices=sorted(MODE_DEFAULTS.keys()),
        help="Analysis mode (design, content, competitor, transcribe)",
    )

    mdl = parser.add_argument_group("Model")
    mdl.add_argument(
        "--model",
        help="Gemini model override (default depends on mode: design=gemini-2.5-pro, others=gemini-2.5-flash)",
    )

    out = parser.add_argument_group("Output")
    out.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)",
    )

    dbg = parser.add_argument_group("Debug")
    dbg.add_argument(
        "--verbose", "-v", action="store_true",
        help="Verbose output to stderr",
    )
    dbg.add_argument(
        "--dry-run", action="store_true",
        help="Show prompt and config without making API call",
    )

    return parser


def main() -> int:
    """Entry point. Returns exit code."""
    parser = build_parser()
    args = parser.parse_args()

    # Resolve model default based on mode
    if not args.model:
        args.model = MODE_DEFAULTS[args.mode]["model"]

    # Validate file exists
    if not Path(args.file).exists():
        _log(f"Error: File not found: {args.file}")
        return 1

    # Dry run: show config and prompt, then exit
    if args.dry_run:
        print(json.dumps({
            "mode": args.mode,
            "model": args.model,
            "file": args.file,
            "file_size_mb": round(Path(args.file).stat().st_size / 1024 / 1024, 1),
            "prompt": PROMPTS[args.mode],
        }, indent=2))
        return 0

    # Find API key
    api_key = find_api_key()
    if not api_key:
        _log("Error: No API key found.")
        _log("Set GEMINI_API_KEY environment variable:")
        _log("  GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) python3 ...")
        return 1

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Run analysis
    result = analyze_video(
        client=client,
        file_path=args.file,
        mode=args.mode,
        model=args.model,
        verbose=args.verbose,
    )

    # Output
    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(output_json)
        if args.verbose:
            _log(f"Written to {args.output}")
    else:
        print(output_json)

    # Exit code
    if "error" in result:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
