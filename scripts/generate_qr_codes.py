"""Generate one PNG per book containing its QR code and title.

Output: ../qr_codes/<id>_<sanitized_title>.png

The QR payload is `ISULIB:BOOK:<id>` so the in-app scanner picks up the right
book.  Run from the repo root: `python3 scripts/generate_qr_codes.py`.
"""
import os
import re
import sys

import qrcode
from PIL import Image, ImageDraw, ImageFont

BOOKS = [
    (1, "Clean Code", "Robert C. Martin"),
    (2, "Data Structures and Algorithms", "Alfred V. Aho"),
    (3, "Database System Concepts", "Abraham Silberschatz"),
    (4, "Introduction to Algorithms", "Thomas H. Cormen"),
    (5, "Engineering Mechanics", "J.L. Meriam"),
    (6, "The Great Gatsby", "F. Scott Fitzgerald"),
    (7, "Physics for Scientists", "Raymond A. Serway"),
    (8, "Calculus: Early Transcendentals", "James Stewart"),
    (9, "The Art of War", "Sun Tzu"),
    (10, "Business Strategy", "Michael Porter"),
]

QR_BOX_SIZE = 12
QR_BORDER = 2
LABEL_PADDING = 30
TITLE_FONT_SIZE = 32
AUTHOR_FONT_SIZE = 22
PAYLOAD_FONT_SIZE = 18

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "qr_codes"
)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def sanitize(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9 ]", "", name)
    name = re.sub(r"\s+", "_", name).strip("_")
    return name


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if text_size(draw, candidate, font)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]


def make_card(book_id: int, title: str, author: str) -> Image.Image:
    payload = f"ISULIB:BOOK:{book_id}"
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=QR_BOX_SIZE,
        border=QR_BORDER,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_w, qr_h = qr_img.size

    title_font = load_font(TITLE_FONT_SIZE)
    author_font = load_font(AUTHOR_FONT_SIZE)
    payload_font = load_font(PAYLOAD_FONT_SIZE)

    canvas_width = max(qr_w, 600) + LABEL_PADDING * 2

    scratch = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(scratch)
    title_lines = wrap(draw, title, title_font, canvas_width - LABEL_PADDING * 2)
    title_line_h = text_size(draw, "Ag", title_font)[1] + 6
    title_block_h = title_line_h * len(title_lines)
    author_h = text_size(draw, author, author_font)[1] + 6
    payload_h = text_size(draw, payload, payload_font)[1]

    canvas_height = (
        LABEL_PADDING
        + qr_h
        + LABEL_PADDING
        + title_block_h
        + author_h
        + LABEL_PADDING // 2
        + payload_h
        + LABEL_PADDING
    )

    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    qr_x = (canvas_width - qr_w) // 2
    canvas.paste(qr_img, (qr_x, LABEL_PADDING))

    draw = ImageDraw.Draw(canvas)
    y = LABEL_PADDING + qr_h + LABEL_PADDING
    for line in title_lines:
        line_w = text_size(draw, line, title_font)[0]
        draw.text(((canvas_width - line_w) // 2, y), line, fill="black",
                  font=title_font)
        y += title_line_h

    author_text = f"by {author}"
    author_w = text_size(draw, author_text, author_font)[0]
    draw.text(((canvas_width - author_w) // 2, y), author_text,
              fill="#374151", font=author_font)
    y += author_h + LABEL_PADDING // 2

    payload_w = text_size(draw, payload, payload_font)[0]
    draw.text(((canvas_width - payload_w) // 2, y), payload,
              fill="#1B5E20", font=payload_font)

    return canvas


def main() -> int:
    print(f"Output folder: {OUTPUT_DIR}")
    for book_id, title, author in BOOKS:
        card = make_card(book_id, title, author)
        filename = f"{book_id:02d}_{sanitize(title)}.png"
        path = os.path.join(OUTPUT_DIR, filename)
        card.save(path, "PNG")
        print(f"  wrote {filename}")
    print(f"Done — {len(BOOKS)} files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
