#!/usr/bin/env python3
"""Generate preview images for image-prompt rules using Gemini/NanoBananaPro."""

import json
import sys
import base64
from pathlib import Path
from google import genai
from google.genai import types

RULES_JSON = Path(__file__).parent.parent / "src" / "data" / "rules.json"
PREVIEW_DIR = Path(__file__).parent.parent / "public" / "previews"
PREVIEW_DIR.mkdir(exist_ok=True)


def load_api_key():
    secrets = Path(__file__).parent.parent.parent / "Moru_workspace" / ".env.secrets"
    if secrets.exists():
        for line in secrets.read_text().splitlines():
            if line.startswith("GOOGLE_GENAI_API_KEY="):
                return line.split("=", 1)[1].strip()
    import os
    return os.environ.get("GOOGLE_GENAI_API_KEY", "")


def extract_prompt(rule):
    """Extract the image generation prompt from JSON content."""
    try:
        data = json.loads(rule["content"])
        series = data.get("food_photography_series", {})
        variations = series.get("variations", [])
        if variations:
            return variations[0].get("prompt", "")
    except (json.JSONDecodeError, KeyError):
        pass
    return rule.get("description", "")


def generate_with_nanobananapro(client, prompt, output_path):
    """Generate image using NanoBananaPro (gemini-3-pro-image-preview)."""
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=f"Generate this image. Only output the image, no text.\n\n{prompt}",
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            # Save as webp
            img_bytes = part.inline_data.data
            output_path.write_bytes(img_bytes)
            print(f"  Saved: {output_path} ({len(img_bytes)//1024}KB)")
            return True

    print("  No image in response")
    return False


def generate_with_imagen(client, prompt, output_path):
    """Fallback: generate image using Imagen 4."""
    response = client.models.generate_images(
        model="imagen-4.0-fast-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="3:4",
            output_mime_type="image/webp",
        ),
    )
    if response.generated_images:
        img = response.generated_images[0]
        output_path.write_bytes(img.image.image_bytes)
        print(f"  Saved: {output_path}")
        return True
    return False


def main():
    api_key = load_api_key()
    if not api_key:
        print("ERROR: GOOGLE_GENAI_API_KEY not found")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    rules = json.loads(RULES_JSON.read_text())
    image_rules = [r for r in rules if r["tool"] == "image-prompt"]

    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        target_id = sys.argv[1]
        image_rules = [r for r in image_rules if r["id"] == target_id]

    print(f"Found {len(image_rules)} image prompt rules")

    for rule in image_rules:
        output = PREVIEW_DIR / f"{rule['id']}.webp"
        if output.exists() and "--force" not in sys.argv:
            print(f"  Skip (exists): {rule['id']}")
            continue

        prompt = extract_prompt(rule)
        if not prompt:
            print(f"  Skip (no prompt): {rule['id']}")
            continue

        print(f"Generating: {rule['title']}")
        print(f"  Prompt: {prompt[:100]}...")

        try:
            generate_with_nanobananapro(client, prompt, output)
        except Exception as e:
            print(f"  NanoBananaPro failed: {e}")
            print(f"  Trying Imagen 4...")
            try:
                generate_with_imagen(client, prompt, output)
            except Exception as e2:
                print(f"  Imagen 4 also failed: {e2}")


if __name__ == "__main__":
    main()
