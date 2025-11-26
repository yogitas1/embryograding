#!/usr/bin/env python3
"""
Extract embryo images from the verification_report.html file.
This script extracts base64-encoded images and saves them as JPG files.
"""

import re
import base64
from pathlib import Path


def extract_images_from_html(html_file, output_dir):
    """
    Extract base64-encoded images from HTML file and save them.

    Args:
        html_file: Path to the HTML file containing embedded images
        output_dir: Directory to save extracted images
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find all base64-encoded images
    # Pattern: data:image/jpeg;base64,<base64_data>
    pattern = r'data:image/jpeg;base64,([A-Za-z0-9+/=]+)'
    matches = re.findall(pattern, html_content)

    print(f"Found {len(matches)} embedded images in {html_file}")

    # Extract image filenames from the CSV data in HTML
    # Look for pattern like: D5_368.jpg,1,3AA
    filename_pattern = r'(D[35]_\d+\.jpg)'
    filenames = re.findall(filename_pattern, html_content)

    # Remove duplicates while preserving order
    seen = set()
    unique_filenames = []
    for fn in filenames:
        if fn not in seen:
            seen.add(fn)
            unique_filenames.append(fn)

    if len(unique_filenames) != len(matches):
        print(f"Warning: Found {len(unique_filenames)} filenames but {len(matches)} images")
        print("Using generic naming for missing filenames")

    # Save each image
    saved_count = 0
    for i, base64_data in enumerate(matches):
        try:
            # Decode base64 data
            image_data = base64.b64decode(base64_data)

            # Determine filename
            if i < len(unique_filenames):
                filename = unique_filenames[i]
            else:
                filename = f"embryo_{i+1:02d}.jpg"

            # Save image
            output_file = output_path / filename
            with open(output_file, 'wb') as f:
                f.write(image_data)

            print(f"Saved: {output_file} ({len(image_data)} bytes)")
            saved_count += 1

        except Exception as e:
            print(f"Error saving image {i+1}: {e}")

    print(f"\nSuccessfully extracted {saved_count} images to {output_dir}")
    return saved_count


if __name__ == "__main__":
    html_file = "verification_results/verification_report.html"
    output_dir = "extracted_images"

    print("=" * 60)
    print("Embryo Image Extraction Tool")
    print("=" * 60)

    extract_images_from_html(html_file, output_dir)

    print("\nDone! Images are ready for grading.")
