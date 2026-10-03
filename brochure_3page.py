"""
PQS Company Profile — 3-Page Premium Brochure
Modern Corporate Design
"""

import fitz  # PyMuPDF
import os
import re
from PIL import Image

# ─── PATHS ───────────────────────────────────────────────────────────────────
BASE       = r"C:\Users\Noman Traders\OneDrive\Desktop\PQS"
IMG_DIR    = os.path.join(BASE, "brochure_images")
ASSETS     = os.path.join(BASE, "pqs-website", "public")

LOGO_GOLD  = os.path.join(ASSETS, "pqs_3letter_gold.png")
BANNER     = os.path.join(BASE, "golden_banner.png")
CONTACT_BG = os.path.join(BASE, "contact_bg.jpg")
STAMP_WM   = os.path.join(BASE, "stamp_watermark.png")

IMG_THREADS    = os.path.join(IMG_DIR, "threads.jpg")
IMG_COTTON     = os.path.join(IMG_DIR, "cotton.jpg")
IMG_EMBROIDERY = os.path.join(IMG_DIR, "embroidery.jpg")
IMG_LAB        = os.path.join(IMG_DIR, "lab_inspector.jpg")
IMG_MACHINES   = os.path.join(IMG_DIR, "machines.jpg")

OUT_PATH   = os.path.join(BASE, "PQS_Brochure_Final_v8.pdf")

# ─── COLORS ──────────────────────────────────────────────────────────────────
NAVY       = (10/255, 30/255, 53/255)
GOLD       = (200/255, 169/255, 81/255)
WHITE      = (1, 1, 1)
LIGHT_GRAY = (0.75, 0.75, 0.75)
DARK_GRAY  = (0.35, 0.35, 0.35)
OFFWHITE   = (0.96, 0.96, 0.94)

# A4 dimensions in points
W, H = 595.28, 841.89

doc = fitz.open()

def crop_image_to_ratio(img_path, target_ratio, inset=15):
    img = Image.open(img_path)
    # Crop inward to remove any AI-generated grey borders
    img = img.crop((inset, inset, img.width - inset, img.height - inset))
    img_w, img_h = img.size
    img_ratio = img_w / img_h
    
    if img_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) / 2
        img = img.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) / 2
        img = img.crop((0, top, img_w, top + new_h))
    return img

def insert_framed_image(page, rect, img_path, border_width=2.0):
    target_ratio = rect.width / rect.height
    temp_path = img_path + "_cropped.jpg"
    cropped = crop_image_to_ratio(img_path, target_ratio)
    if cropped.mode == "RGBA":
        cropped = cropped.convert("RGB")
    cropped.save(temp_path, quality=95)
    
    page.insert_image(rect, filename=temp_path, keep_proportion=False)
    if border_width > 0:
        page.draw_rect(rect, color=GOLD, width=border_width)

def insert_rich_text(page, rect, segments, fontsize, leading):
    x0, y0, x1, y1 = rect
    max_w = x1 - x0
    cx, cy = x0, y0 + fontsize
    
    for text, fontname, color in segments:
        font = fitz.Font(fontname)
        tokens = re.split(r'( )', text)
        for token in tokens:
            if not token: continue
            token_w = font.text_length(token, fontsize=fontsize)
            if token == " ":
                if cx + token_w <= x1:
                    cx += token_w
            else:
                if cx + token_w > x1 and cx > x0:
                    cx = x0
                    cy += leading
                page.insert_text(fitz.Point(cx, cy), token, fontname=fontname, fontsize=fontsize, color=color)
                cx += token_w
    return cy

def add_footer(page, page_num, banner_path, is_dark=True):
    bg_color = NAVY if is_dark else OFFWHITE
    text_color = LIGHT_GRAY if is_dark else DARK_GRAY
    page.draw_rect(fitz.Rect(0, H-57, W, H), color=bg_color, fill=bg_color)
    page.insert_image(fitz.Rect(30, H-38, 195, H-20), filename=banner_path)
    page.insert_text(
        fitz.Point(220, H-22),
        "TEXTILE TRAINING | CONSULTANCY | TROUBLESHOOTING",
        fontname="helv", fontsize=7.5, color=text_color
    )
    page.insert_text(
        fitz.Point(W-50, H-22),
        f"0{page_num}",
        fontname="hebo", fontsize=9, color=GOLD
    )


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — COVER (Ultra-Premium Mosaic Bleed + V24 Dark Theme)
# ═════════════════════════════════════════════════════════════════════════════
p1 = doc.new_page(width=W, height=H)

# 1. Background for the bottom half (Textured Navy)
p1.insert_image(p1.rect, filename=IMG_MACHINES, keep_proportion=False)
shape = p1.new_shape()
shape.draw_rect(p1.rect)
shape.finish(color=NAVY, fill=NAVY, fill_opacity=0.82)
shape.commit()

# 2. Top 5-Image Mosaic Grid (y=0 to 500)
y_split = 220
y_bottom = 500

r1 = fitz.Rect(0, 0, 280, y_split)
r2 = fitz.Rect(280, 0, W, y_split)
r3 = fitz.Rect(0, y_split, 170, y_bottom)
r4 = fitz.Rect(170, y_split, 420, y_bottom)
r5 = fitz.Rect(420, y_split, W, y_bottom)

insert_framed_image(p1, r1, IMG_MACHINES, 0)
insert_framed_image(p1, r2, IMG_COTTON, 0)
insert_framed_image(p1, r3, IMG_THREADS, 0)
insert_framed_image(p1, r4, IMG_LAB, 0)
insert_framed_image(p1, r5, IMG_EMBROIDERY, 0)

# 3. Gold Seams (4px width)
p1.draw_line(fitz.Point(280, 0), fitz.Point(280, y_split), color=GOLD, width=4)
p1.draw_line(fitz.Point(170, y_split), fitz.Point(170, y_bottom), color=GOLD, width=4)
p1.draw_line(fitz.Point(420, y_split), fitz.Point(420, y_bottom), color=GOLD, width=4)
p1.draw_line(fitz.Point(0, y_split), fitz.Point(W, y_split), color=GOLD, width=4)

# 4. Main Separator (y=500)
p1.draw_rect(fitz.Rect(0, y_bottom, W, y_bottom + 6), color=GOLD, fill=GOLD)
p1.draw_rect(fitz.Rect(0, y_bottom + 6, W, y_bottom + 8), color=WHITE, fill=WHITE)

# 5. Bottom Typography (Left Aligned, Modern)
start_y = y_bottom + 60
left_x = 50

logo_size = 110
p1.insert_image(fitz.Rect(left_x, start_y, left_x + logo_size, start_y + logo_size), filename=LOGO_GOLD, keep_proportion=True)

wm_w = 340
wm_h = wm_w * (478.5 - 428.25) / (541.5 - 54.0)
wm_y = start_y + (logo_size - wm_h) / 2 + 5
p1.insert_image(fitz.Rect(left_x + logo_size + 15, wm_y, left_x + logo_size + 15 + wm_w, wm_y + wm_h), filename=BANNER, keep_proportion=True)

title_y = start_y + logo_size + 70
p1.insert_text(fitz.Point(left_x, title_y), "COMPANY PROFILE", fontname="hebo", fontsize=38, color=WHITE)

p1.draw_rect(fitz.Rect(left_x, title_y + 18, left_x + 60, title_y + 21), color=GOLD, fill=GOLD)
tag_text = "Textile Training  -  Consultancy  -  Troubleshooting"
p1.insert_text(fitz.Point(left_x, title_y + 48), tag_text, fontname="helv", fontsize=13, color=LIGHT_GRAY)

# PAGE 2 — WHO WE ARE / MISSION / VISION / TRAINING
# ═════════════════════════════════════════════════════════════════════════════
p2 = doc.new_page(width=W, height=H)

# Header
header_h = 52
p2.draw_rect(fitz.Rect(0, 0, W, header_h), color=NAVY, fill=NAVY)
p2.insert_text(fitz.Point(40, 35), "WHO WE ARE", fontname="hebo", fontsize=18, color=WHITE)
p2.insert_text(fitz.Point(W - 60, 35), "02", fontname="hebo", fontsize=14, color=GOLD)

# Background (Offwhite + Large Stamp Watermark entering from Left)
p2.draw_rect(fitz.Rect(0, header_h, W, H - 57), color=OFFWHITE, fill=OFFWHITE)
stamp_w = 900
stamp_x = -300  # Entering from left
stamp_y = 100
p2.insert_image(fitz.Rect(stamp_x, stamp_y, stamp_x + stamp_w, stamp_y + stamp_w), filename=STAMP_WM, keep_proportion=True)

# Who We Are Text (Left side) with BOLD inline text
body_y = header_h + 40
margin = 40
text_w = W - 2*margin - 200 # Leave room for image on right
rich_segments = [
    ("PRECISION QUALITY SERVICES ", "hebo", NAVY),
    ("(PQS) is a specialized textile consultancy and training company focused on helping textile organizations improve quality, productivity, process control, and operational performance.", "helv", DARK_GRAY)
]
end_y1 = insert_rich_text(p2, fitz.Rect(margin, body_y, margin + text_w, body_y + 100), rich_segments, 10.5, 16)

rich_segments2 = [
    ("We combine technical knowledge with hands-on problem-solving and process improvement to help manufacturers achieve consistent quality and sustainable growth. Our work is rooted in the real challenges of the factory floor \u2014 not boardroom theory.", "helv", DARK_GRAY)
]
end_y = insert_rich_text(p2, fitz.Rect(margin, end_y1 + 8, margin + text_w, end_y1 + 200), rich_segments2, 10.5, 16)

# Image on the right of Who We Are
img_right_rect = fitz.Rect(margin + text_w + 30, body_y, W - margin, end_y)
insert_framed_image(p2, img_right_rect, IMG_MACHINES, 2)

quote_y = end_y + 25
quote = (
    '"Better processes create better quality. Better quality creates '
    'satisfied customers. Satisfied customers create sustainable '
    'business growth."'
)
p2.draw_rect(fitz.Rect(margin, quote_y - 4, margin + 3, quote_y + 45), color=GOLD, fill=GOLD)
insert_rich_text(p2, fitz.Rect(margin + 16, quote_y, W - margin, quote_y + 100), [(quote, "heit", NAVY)], 10, 15)

# Mission & Vision Boxes
mv_top = quote_y + 75
box_h = 160
box_gap = 14
box_w = (W - 2*margin - box_gap) / 2

# Mission
m_rect = fitz.Rect(margin, mv_top, margin + box_w, mv_top + box_h)
p2.draw_rect(m_rect, color=NAVY, fill=NAVY)
p2.draw_rect(fitz.Rect(margin, mv_top, margin + box_w, mv_top + 4), color=GOLD, fill=GOLD)
p2.insert_text(fitz.Point(margin + 16, mv_top + 32), "OUR MISSION", fontname="hebo", fontsize=12, color=GOLD)
mission_text = (
    "To support textile organizations through professional training, "
    "technical consultancy, and practical troubleshooting that strengthen "
    "people, processes, and product quality."
)
insert_rich_text(p2, fitz.Rect(margin + 16, mv_top + 45, margin + box_w - 16, mv_top + box_h), [(mission_text, "helv", LIGHT_GRAY)], 9.5, 14.5)

# Vision
v_x = margin + box_w + box_gap
v_rect = fitz.Rect(v_x, mv_top, v_x + box_w, mv_top + box_h)
p2.draw_rect(v_rect, color=NAVY, fill=NAVY)
p2.draw_rect(fitz.Rect(v_x, mv_top, v_x + box_w, mv_top + 4), color=GOLD, fill=GOLD)
p2.insert_text(fitz.Point(v_x + 16, mv_top + 32), "OUR VISION", fontname="hebo", fontsize=12, color=GOLD)
vision_text = (
    "To become a trusted textile industry partner recognized for delivering "
    "practical knowledge, effective solutions, and measurable improvements "
    "in quality and performance."
)
insert_rich_text(p2, fitz.Rect(v_x + 16, mv_top + 45, v_x + box_w - 16, mv_top + box_h), [(vision_text, "helv", LIGHT_GRAY)], 9.5, 14.5)

# Training Section
train_top = mv_top + box_h + 35
p2.draw_rect(fitz.Rect(margin, train_top, margin + 50, train_top + 3), color=GOLD, fill=GOLD)
p2.insert_text(fitz.Point(margin, train_top + 24), "TEXTILE TRAINING", fontname="hebo", fontsize=14, color=NAVY)

train_intro = (
    "Practical, industry-focused training programmes for production teams, "
    "supervisors, and quality personnel."
)
train_y = insert_rich_text(p2, fitz.Rect(margin, train_top + 36, W - margin - 150, train_top + 100), [(train_intro, "helv", DARK_GRAY)], 10.5, 15)

left_topics = [
    "Textile quality management",
    "Quality control & assurance",
    "Defect identification",
    "Root cause analysis",
    "Process control fundamentals",
    "Inspection & testing",
]
right_topics = [
    "Quality system improvement",
    "Process evaluation & mapping",
    "Quality performance improvement",
    "Defect & rejection reduction",
    "Process standardization",
    "CAPA implementation",
]

col_w = (W - 2*margin - 20) / 2
topics_y = train_y + 12

for i, topic in enumerate(left_topics):
    ty = topics_y + i * 18
    p2.draw_rect(fitz.Rect(margin + 6, ty - 6, margin + 10, ty - 2), color=GOLD, fill=GOLD)
    p2.insert_text(fitz.Point(margin + 20, ty), topic, fontname="helv", fontsize=9.5, color=DARK_GRAY)

for i, topic in enumerate(right_topics):
    ty = topics_y + i * 18
    p2.draw_rect(fitz.Rect(margin + col_w + 20 + 6, ty - 6, margin + col_w + 20 + 10, ty - 2), color=GOLD, fill=GOLD)
    p2.insert_text(fitz.Point(margin + col_w + 20 + 20, ty), topic, fontname="helv", fontsize=9.5, color=DARK_GRAY)

add_footer(p2, 2, BANNER, is_dark=False)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — CONTACT
# ═════════════════════════════════════════════════════════════════════════════
p3 = doc.new_page(width=W, height=H)

# Full bleed background with Navy overlay
p3.insert_image(p3.rect, filename=IMG_THREADS, keep_proportion=False)
shape = p3.new_shape()
shape.draw_rect(p3.rect)
shape.finish(color=NAVY, fill=NAVY, fill_opacity=0.85)
shape.commit()

# Logo
logo_size = 110
p3.insert_image(fitz.Rect((W-logo_size)/2, 80, (W+logo_size)/2, 80 + logo_size), filename=LOGO_GOLD, keep_proportion=True)

# OUR COMMITMENT
cy = 250
commit_title = "OUR COMMITMENT"
font_title = fitz.Font("hebo")
ct_w = font_title.text_length(commit_title, fontsize=18)
p3.insert_text(fitz.Point((W - ct_w)/2, cy), commit_title, fontname="hebo", fontsize=18, color=WHITE)
cy += 15
p3.draw_rect(fitz.Rect((W-40)/2, cy, (W+40)/2, cy + 2), color=GOLD, fill=GOLD)
cy += 45

commit_lines = [
    "Improve Knowledge.",
    "Improve Processes.",
    "Improve Quality.",
    "Improve Performance.",
]
font_body = fitz.Font("helv")
for line in commit_lines:
    lw = font_body.text_length(line, fontsize=14)
    p3.insert_text(fitz.Point((W - lw)/2, cy), line, fontname="helv", fontsize=14, color=WHITE)
    cy += 26

cy += 35
promise_title = "OUR PROMISE"
pt_w = font_title.text_length(promise_title, fontsize=11)
p3.insert_text(fitz.Point((W - pt_w)/2, cy), promise_title, fontname="hebo", fontsize=11, color=GOLD)
cy += 18

promise_lines = [
    "Precision in Knowledge. Quality in Processes.",
    "Solutions to Problems. Performance through Improvement."
]
font_italic = fitz.Font("heit")
for line in promise_lines:
    lw = font_italic.text_length(line, fontsize=11)
    p3.insert_text(fitz.Point((W - lw)/2, cy), line, fontname="heit", fontsize=11, color=LIGHT_GRAY)
    cy += 20

cy += 50
p3.draw_rect(fitz.Rect((W-100)/2, cy, (W+100)/2, cy + 1), color=GOLD, fill=GOLD)
cy += 45

contact_title = "CONTACT US"
ct_w = font_title.text_length(contact_title, fontsize=15)
p3.insert_text(fitz.Point((W - ct_w)/2, cy), contact_title, fontname="hebo", fontsize=15, color=WHITE)
cy += 35

# Contact Grid: Left aligned in the center
contact_items = [
    ("PHONE", "03322673373", "tel:+923322673373"),
    ("EMAIL", "precisionqualityserviveslabs@gmail.com", "mailto:precisionqualityserviveslabs@gmail.com"),
    ("WEBSITE", "precisionqualityservices.vercel.app", "https://precisionqualityservices.vercel.app"),
    ("LOCATION", "R-332/9, Dastagir, F.B Area, Karachi, 75950", None),
    ("LINKEDIN", "linkedin.com/company/pqs-precision-quality-services", "https://www.linkedin.com/company/pqs-precision-quality-services"),
]

max_label_w = 0
for label, _, _ in contact_items:
    lw = font_title.text_length(label, fontsize=10)
    if lw > max_label_w:
        max_label_w = lw

grid_x = W / 2 - 160  
for label, value, uri in contact_items:
    p3.insert_text(fitz.Point(grid_x, cy), label, fontname="hebo", fontsize=10, color=GOLD)
    
    val_x = grid_x + max_label_w + 30
    vw = font_body.text_length(value, fontsize=10.5)
    p3.insert_text(fitz.Point(val_x, cy), value, fontname="helv", fontsize=10.5, color=WHITE)
    
    if uri:
        val_rect = fitz.Rect(val_x, cy - 10.5, val_x + vw, cy + 2)
        p3.insert_link({"kind": fitz.LINK_URI, "from": val_rect, "uri": uri})
        
    cy += 26

cy += 50
closing = "Let's Improve Textile Quality Together."
cw = font_italic.text_length(closing, fontsize=14)
p3.insert_text(fitz.Point((W - cw)/2, cy), closing, fontname="heit", fontsize=14, color=WHITE)



# Gold Border
p3.draw_rect(fitz.Rect(margin, margin, W - margin, H - margin), color=GOLD, width=1.5)

doc.save(OUT_PATH)
doc.close()
print(f"Saved {OUT_PATH}")


