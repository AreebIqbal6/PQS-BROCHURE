"""
PQS Company Profile — 3-Page Premium Brochure
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
STAMP      = os.path.join(ASSETS, "stamp.png")

IMG_THREADS    = os.path.join(IMG_DIR, "threads.jpg")
IMG_COTTON     = os.path.join(IMG_DIR, "cotton.jpg")
IMG_EMBROIDERY = os.path.join(IMG_DIR, "embroidery.jpg")
IMG_LAB        = os.path.join(IMG_DIR, "lab_inspector.jpg")
IMG_MACHINES   = os.path.join(IMG_DIR, "machines.jpg")

OUT_PATH   = os.path.join(BASE, "PQS_Brochure_Final.pdf")

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

def crop_image_to_ratio(img_path, target_ratio):
    img = Image.open(img_path)
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

def draw_gold_border(page, margin=18, width=2.0):
    rect = fitz.Rect(margin, margin, W - margin, H - margin)
    page.draw_rect(rect, color=GOLD, width=width)

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
#  PAGE 1 — COVER
# ═════════════════════════════════════════════════════════════════════════════
p1 = doc.new_page(width=W, height=H)

# Low opacity background overlay
p1.insert_image(p1.rect, filename=CONTACT_BG)
shape = p1.new_shape()
shape.draw_rect(p1.rect)
shape.finish(color=NAVY, fill=NAVY, fill_opacity=0.88)
shape.commit()

# Dynamic overlapping collage (with gold boundaries)
rect_tl = fitz.Rect(40, 70, 270, 230)
rect_tr = fitz.Rect(330, 60, 560, 210)
rect_bl = fitz.Rect(50, 270, 250, 430)
rect_br = fitz.Rect(340, 260, 550, 410)
rect_main = fitz.Rect(180, 150, 410, 350) # Center piece

insert_framed_image(p1, rect_tl, IMG_MACHINES, 2)
insert_framed_image(p1, rect_tr, IMG_THREADS, 2)
insert_framed_image(p1, rect_bl, IMG_COTTON, 2)
insert_framed_image(p1, rect_br, IMG_EMBROIDERY, 2)
insert_framed_image(p1, rect_main, IMG_LAB, 3) # Thicker border for center image

# Gold line separator
p1.draw_rect(fitz.Rect(100, 480, W - 100, 481.5), color=GOLD, fill=GOLD)

# Logo
logo_top = 510
logo_size = 140
logo_x = (W - logo_size) / 2
p1.insert_image(fitz.Rect(logo_x, logo_top, logo_x + logo_size, logo_top + logo_size),
                filename=LOGO_GOLD, keep_proportion=True)

# Wordmark
wm_top = logo_top + logo_size + 15
wm_w = 420
wm_h = wm_w * (478.5 - 428.25) / (541.5 - 54.0)
wm_x = (W - wm_w) / 2
p1.insert_image(fitz.Rect(wm_x, wm_top, wm_x + wm_w, wm_top + wm_h),
                filename=BANNER, keep_proportion=True)

# Gold dash
dash_top = wm_top + wm_h + 15
dash_w = 60
p1.draw_rect(fitz.Rect((W-dash_w)/2, dash_top, (W+dash_w)/2, dash_top + 2), color=GOLD, fill=GOLD)

cp_text = "C O M P A N Y   P R O F I L E"
font_cp = fitz.Font("helv")
cp_w = font_cp.text_length(cp_text, fontsize=11)
p1.insert_text(fitz.Point((W - cp_w) / 2, dash_top + 30), cp_text, fontname="helv", fontsize=11, color=WHITE)

tag_text = "Textile Training  ·  Consultancy  ·  Troubleshooting"
tag_w = font_cp.text_length(tag_text, fontsize=9)
p1.insert_text(fitz.Point((W - tag_w) / 2, dash_top + 50), tag_text, fontname="helv", fontsize=9, color=LIGHT_GRAY)

add_footer(p1, 1, BANNER, is_dark=True)
draw_gold_border(p1)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — WHO WE ARE / MISSION / VISION / TRAINING
# ═════════════════════════════════════════════════════════════════════════════
p2 = doc.new_page(width=W, height=H)

# Header
header_h = 52
p2.draw_rect(fitz.Rect(0, 0, W, header_h), color=NAVY, fill=NAVY)
p2.insert_text(fitz.Point(40, 35), "WHO WE ARE", fontname="hebo", fontsize=18, color=WHITE)
p2.insert_text(fitz.Point(W - 60, 35), "02", fontname="hebo", fontsize=14, color=GOLD)

# Background (Offwhite + Stamp Watermark)
p2.draw_rect(fitz.Rect(0, header_h, W, H - 57), color=OFFWHITE, fill=OFFWHITE)
stamp_w = 400
stamp_x = (W - stamp_w) / 2
p2.insert_image(fitz.Rect(stamp_x, 200, stamp_x + stamp_w, 200 + stamp_w), filename=STAMP, keep_proportion=True)

# Overlay to fade the stamp
shape = p2.new_shape()
shape.draw_rect(fitz.Rect(0, header_h, W, H - 57))
shape.finish(color=OFFWHITE, fill=OFFWHITE, fill_opacity=0.88)
shape.commit()

# Who We Are Text (Left side) with BOLD inline text
body_y = header_h + 35
margin = 40
text_w = W - 2*margin - 180 # Leave room for image on right
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
img_right_rect = fitz.Rect(margin + text_w + 20, body_y, W - margin, end_y)
insert_framed_image(p2, img_right_rect, IMG_LAB, 2)

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

p3.insert_image(p3.rect, filename=CONTACT_BG, keep_proportion=False)

logo_rect = fitz.Rect((W-110)/2, 60, (W+110)/2, 170)
p3.insert_image(logo_rect, filename=LOGO_GOLD, keep_proportion=True)

commit_text = "O U R   C O M M I T M E N T"
font_h = fitz.Font("hebo")
commit_w = font_h.text_length(commit_text, fontsize=18)
p3.insert_text(fitz.Point((W - commit_w)/2, 220), commit_text, fontname="hebo", fontsize=18, color=WHITE)

p3.draw_rect(fitz.Rect((W-80)/2, 235, (W+80)/2, 237), color=GOLD, fill=GOLD)

commit_lines = [
    "Improve Knowledge.",
    "Improve Processes.",
    "Improve Quality.",
    "Improve Performance.",
]
cy = 275
for line in commit_lines:
    lw = font_h.text_length(line, fontsize=15)
    p3.insert_text(fitz.Point((W - lw)/2, cy), line, fontname="hebo", fontsize=15, color=WHITE)
    cy += 28

cy += 15
promise_title = "Our Promise"
pt_w = font_h.text_length(promise_title, fontsize=14)
p3.insert_text(fitz.Point((W - pt_w)/2, cy), promise_title, fontname="hebo", fontsize=14, color=GOLD)
cy += 10
p3.draw_rect(fitz.Rect((W-40)/2, cy, (W+40)/2, cy + 1.5), color=GOLD, fill=GOLD)
cy += 20

promise_lines = [
    "Precision in Knowledge.  Quality in Processes.",
    "Solutions to Problems.  Performance through Improvement.",
]
font_promise = fitz.Font("helv")
for line in promise_lines:
    lw = font_promise.text_length(line, fontsize=11)
    p3.insert_text(fitz.Point((W - lw)/2, cy), line, fontname="helv", fontsize=11, color=LIGHT_GRAY)
    cy += 20

cy += 40
contact_title = "C O N T A C T   U S"
ct_w = font_h.text_length(contact_title, fontsize=16)
p3.insert_text(fitz.Point((W - ct_w)/2, cy), contact_title, fontname="hebo", fontsize=16, color=WHITE)
cy += 8
p3.draw_rect(fitz.Rect((W-60)/2, cy, (W+60)/2, cy + 1.5), color=GOLD, fill=GOLD)
cy += 35

contact_items = [
    ("PHONE:", "03322673373", "tel:+923322673373"),
    ("EMAIL:", "precisionqualityserviveslabs@gmail.com", "mailto:precisionqualityserviveslabs@gmail.com"),
    ("WEBSITE:", "precisionqualityservices.vercel.app", "https://precisionqualityservices.vercel.app"),
    ("LOCATION:", "R-332/9, Dastagir, F.B Area, Karachi, 75950", None),
    ("LINKEDIN:", "linkedin.com/company/pqs-precision-quality-services", "https://www.linkedin.com/company/pqs-precision-quality-services"),
]
for label, value, uri in contact_items:
    lw = font_h.text_length(label, fontsize=10)
    vw = font_promise.text_length(value, fontsize=10)
    
    # Label in Gold Bold
    lx = (W/2) - lw - 30
    p3.insert_text(fitz.Point(lx, cy), label, fontname="hebo", fontsize=10, color=GOLD)
    
    # Value in Light Gray
    vx = (W/2) - 10
    p3.insert_text(fitz.Point(vx, cy), value, fontname="helv", fontsize=10, color=LIGHT_GRAY)
    
    # Make clickable
    if uri:
        # Define clickable rect
        val_rect = fitz.Rect(vx, cy - 10, vx + vw, cy + 2)
        p3.insert_link({"kind": fitz.LINK_URI, "from": val_rect, "uri": uri})
        
    cy += 24

cy += 30
closing = "Let's Improve Textile Quality Together."
cw = font_h.text_length(closing, fontsize=13)
p3.insert_text(fitz.Point((W - cw)/2, cy), closing, fontname="heit", fontsize=13, color=WHITE)

draw_gold_border(p3)
doc.save(OUT_PATH)
doc.close()
print(f"Saved {OUT_PATH}")



