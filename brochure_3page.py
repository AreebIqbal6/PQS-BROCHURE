"""
PQS Company Profile — 3-Page Premium Brochure
===============================================
Page 1: Cover — Photo mosaic + logo + tagline
Page 2: Who We Are / Mission / Vision / Training
Page 3: Contact (from original PDF)
"""

import fitz  # PyMuPDF
import os

# ─── PATHS ───────────────────────────────────────────────────────────────────
BASE       = r"C:\Users\Noman Traders\OneDrive\Desktop\PQS"
IMG_DIR    = os.path.join(BASE, "brochure_images")
ASSETS     = os.path.join(BASE, "pqs-website", "public")

LOGO_GOLD  = os.path.join(ASSETS, "pqs_3letter_gold.png")
BANNER     = os.path.join(BASE, "golden_banner.png")
CONTACT_BG = os.path.join(BASE, "contact_bg.jpg")
ORIGINAL   = r"C:\Users\Noman Traders\Downloads\PQS_Company_Profile (1).pdf"

IMG_THREADS    = os.path.join(IMG_DIR, "threads.jpg")
IMG_COTTON     = os.path.join(IMG_DIR, "cotton.jpg")
IMG_EMBROIDERY = os.path.join(IMG_DIR, "embroidery.jpg")
IMG_LAB        = os.path.join(IMG_DIR, "lab_inspector.jpg")
IMG_MACHINES   = os.path.join(IMG_DIR, "machines.jpg")

OUT_PATH   = os.path.join(BASE, "PQS_Brochure_3Page.pdf")

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

# ─── HELPER: Insert wrapped text ────────────────────────────────────────────
def insert_wrapped_text(page, text, rect, fontname, fontsize, color, align=0, leading=None):
    if leading is None:
        leading = fontsize * 1.35
    
    words = text.split()
    x0, y0, x1, y1 = rect
    max_w = x1 - x0
    
    line = ""
    cy = y0 + fontsize
    font = fitz.Font(fontname)
    
    for word in words:
        test = (line + " " + word).strip()
        tw_test = font.text_length(test, fontsize=fontsize)
        if tw_test > max_w and line:
            line_w = font.text_length(line, fontsize=fontsize)
            if align == 1:
                lx = x0 + (max_w - line_w) / 2
            elif align == 2:
                lx = x1 - line_w
            else:
                lx = x0
            page.insert_text(fitz.Point(lx, cy), line, fontname=fontname, fontsize=fontsize, color=color)
            cy += leading
            line = word
        else:
            line = test
    
    if line:
        line_w = font.text_length(line, fontsize=fontsize)
        if align == 1:
            lx = x0 + (max_w - line_w) / 2
        elif align == 2:
            lx = x1 - line_w
        else:
            lx = x0
        page.insert_text(fitz.Point(lx, cy), line, fontname=fontname, fontsize=fontsize, color=color)
        cy += leading
    
    return cy


def add_footer(page, page_num, banner_path):
    page.draw_rect(fitz.Rect(0, H-57, W, H), color=NAVY, fill=NAVY)
    page.insert_image(fitz.Rect(30, H-38, 195, H-20), filename=banner_path)
    page.insert_text(
        fitz.Point(220, H-22),
        "TEXTILE TRAINING | CONSULTANCY | TROUBLESHOOTING",
        fontname="helv", fontsize=7.5, color=LIGHT_GRAY
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
p1.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)

margin = 40
gap = 6
img_top = 50
grid_w = W - 2*margin

# Top row: 2 images
top_h = 150
half_w = (grid_w - gap) / 2
p1.insert_image(fitz.Rect(margin, img_top, margin + half_w, img_top + top_h),
                filename=IMG_THREADS, keep_proportion=False)
p1.insert_image(fitz.Rect(margin + half_w + gap, img_top, margin + grid_w, img_top + top_h),
                filename=IMG_COTTON, keep_proportion=False)

# Bottom row: 3 images
bot_top = img_top + top_h + gap
bot_h = 120
third_w = (grid_w - 2*gap) / 3
p1.insert_image(fitz.Rect(margin, bot_top, margin + third_w, bot_top + bot_h),
                filename=IMG_EMBROIDERY, keep_proportion=False)
p1.insert_image(fitz.Rect(margin + third_w + gap, bot_top, margin + 2*third_w + gap, bot_top + bot_h),
                filename=IMG_LAB, keep_proportion=False)
p1.insert_image(fitz.Rect(margin + 2*third_w + 2*gap, bot_top, margin + grid_w, bot_top + bot_h),
                filename=IMG_MACHINES, keep_proportion=False)

# Thin gold line
grid_bottom = bot_top + bot_h + 20
p1.draw_rect(fitz.Rect(margin + 80, grid_bottom, W - margin - 80, grid_bottom + 1.5), color=GOLD, fill=GOLD)

# Logo (made slightly larger to match original proportions better)
logo_top = grid_bottom + 25
logo_size = 140
logo_x = (W - logo_size) / 2
p1.insert_image(fitz.Rect(logo_x, logo_top, logo_x + logo_size, logo_top + logo_size),
                filename=LOGO_GOLD, keep_proportion=True)

# Wordmark
wm_top = logo_top + logo_size + 15
wm_w = 420
wm_h = wm_w * (478.5 - 428.25) / (541.5 - 54.0)  # Preserve aspect ratio
wm_x = (W - wm_w) / 2
p1.insert_image(fitz.Rect(wm_x, wm_top, wm_x + wm_w, wm_top + wm_h),
                filename=BANNER, keep_proportion=True)

# Gold dash
dash_top = wm_top + wm_h + 15
dash_w = 60
p1.draw_rect(fitz.Rect((W-dash_w)/2, dash_top, (W+dash_w)/2, dash_top + 2), color=GOLD, fill=GOLD)

# "COMPANY PROFILE"
cp_text = "C O M P A N Y   P R O F I L E"
font_cp = fitz.Font("helv")
cp_w = font_cp.text_length(cp_text, fontsize=11)
p1.insert_text(fitz.Point((W - cp_w) / 2, dash_top + 28), cp_text, fontname="helv", fontsize=11, color=WHITE)

tag_text = "Textile Training  ·  Consultancy  ·  Troubleshooting"
tag_w = font_cp.text_length(tag_text, fontsize=9)
p1.insert_text(fitz.Point((W - tag_w) / 2, dash_top + 50), tag_text, fontname="helv", fontsize=9, color=LIGHT_GRAY)

motto = "PRECISION. QUALITY. PERFORMANCE."
font_motto = fitz.Font("hebo")
motto_w = font_motto.text_length(motto, fontsize=9)
p1.insert_text(fitz.Point((W - motto_w) / 2, H - 75), motto, fontname="hebo", fontsize=9, color=GOLD)

add_footer(p1, 1, BANNER)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — WHO WE ARE / MISSION / VISION / TRAINING
# ═════════════════════════════════════════════════════════════════════════════
p2 = doc.new_page(width=W, height=H)

header_h = 52
p2.draw_rect(fitz.Rect(0, 0, W, header_h), color=NAVY, fill=NAVY)
p2.insert_text(fitz.Point(margin, 35), "WHO WE ARE", fontname="hebo", fontsize=18, color=WHITE)
p2.insert_text(fitz.Point(W - 60, 35), "02", fontname="hebo", fontsize=14, color=GOLD)
p2.draw_rect(fitz.Rect(0, header_h, W, H - 57), color=OFFWHITE, fill=OFFWHITE)

body_y = header_h + 35
body_text = (
    "Precision Quality Services (PQS) is a specialized textile consultancy and training "
    "company focused on helping textile organizations improve quality, productivity, "
    "process control, and operational performance."
)
body_text2 = (
    "We combine technical knowledge with hands-on problem-solving and process "
    "improvement to help manufacturers achieve consistent quality and sustainable "
    "growth. Our work is rooted in the real challenges of the factory floor — not "
    "boardroom theory."
)

end_y = insert_wrapped_text(p2, body_text, fitz.Rect(margin, body_y, W-margin, body_y+200),
                             "helv", 10.5, DARK_GRAY, leading=16)
end_y = insert_wrapped_text(p2, body_text2, fitz.Rect(margin, end_y + 8, W-margin, end_y+200),
                             "helv", 10.5, DARK_GRAY, leading=16)

quote_y = end_y + 20
quote = (
    '"Better processes create better quality. Better quality creates '
    'satisfied customers. Satisfied customers create sustainable '
    'business growth."'
)
p2.draw_rect(fitz.Rect(margin, quote_y - 4, margin + 3, quote_y + 50), color=GOLD, fill=GOLD)
insert_wrapped_text(p2, quote, fitz.Rect(margin + 16, quote_y, W - margin, quote_y + 100),
                     "heit", 10, NAVY, leading=15)

mv_top = quote_y + 80
box_h = 165
box_gap = 14
box_w = (W - 2*margin - box_gap) / 2

# Mission box
m_rect = fitz.Rect(margin, mv_top, margin + box_w, mv_top + box_h)
p2.draw_rect(m_rect, color=NAVY, fill=NAVY)
p2.draw_rect(fitz.Rect(margin, mv_top, margin + box_w, mv_top + 4), color=GOLD, fill=GOLD)
p2.insert_text(fitz.Point(margin + 16, mv_top + 32), "OUR MISSION", fontname="hebo", fontsize=12, color=GOLD)
mission_text = (
    "To support textile organizations through professional training, "
    "technical consultancy, and practical troubleshooting that strengthen "
    "people, processes, and product quality."
)
insert_wrapped_text(p2, mission_text, fitz.Rect(margin + 16, mv_top + 45, margin + box_w - 16, mv_top + box_h),
                     "helv", 9.5, LIGHT_GRAY, leading=14.5)

# Vision box
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
insert_wrapped_text(p2, vision_text, fitz.Rect(v_x + 16, mv_top + 45, v_x + box_w - 16, mv_top + box_h),
                     "helv", 9.5, LIGHT_GRAY, leading=14.5)


# ── TRAINING SECTION ─────────────────────────────────────────────────────────
train_top = mv_top + box_h + 40
p2.draw_rect(fitz.Rect(margin, train_top, margin + 50, train_top + 3), color=GOLD, fill=GOLD)
p2.insert_text(fitz.Point(margin, train_top + 24), "TEXTILE TRAINING", fontname="hebo", fontsize=14, color=NAVY)

train_intro = (
    "Practical, industry-focused training programmes for production teams, "
    "supervisors, and quality personnel."
)
train_y = insert_wrapped_text(p2, train_intro,
    fitz.Rect(margin, train_top + 36, W - margin, train_top + 100),
    "helv", 10.5, DARK_GRAY, leading=15)

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
    # Draw a small gold square as a bullet
    p2.draw_rect(fitz.Rect(margin + 6, ty - 6, margin + 10, ty - 2), color=GOLD, fill=GOLD)
    p2.insert_text(fitz.Point(margin + 20, ty), topic, fontname="helv", fontsize=9.5, color=DARK_GRAY)

for i, topic in enumerate(right_topics):
    ty = topics_y + i * 18
    p2.draw_rect(fitz.Rect(margin + col_w + 20 + 6, ty - 6, margin + col_w + 20 + 10, ty - 2), color=GOLD, fill=GOLD)
    p2.insert_text(fitz.Point(margin + col_w + 20 + 20, ty), topic, fontname="helv", fontsize=9.5, color=DARK_GRAY)

add_footer(p2, 2, BANNER)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — CONTACT (from original PDF)
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
    ("PHONE:", "[Your Phone Number]"),
    ("EMAIL:", "[Your Email Address]"),
    ("WEBSITE:", "[Your Website]"),
    ("LOCATION:", "[City, Country]"),
    ("LINKEDIN:", "[LinkedIn Profile]"),
]
for label, value in contact_items:
    lw = font_h.text_length(label, fontsize=10)
    p3.insert_text(fitz.Point((W/2) - lw - 10, cy), label, fontname="hebo", fontsize=10, color=GOLD)
    p3.insert_text(fitz.Point((W/2) + 10, cy), value, fontname="helv", fontsize=10, color=LIGHT_GRAY)
    cy += 24

cy += 30
closing = "Let's Improve Textile Quality Together."
cw = font_h.text_length(closing, fontsize=13)
p3.insert_text(fitz.Point((W - cw)/2, cy), closing, fontname="heit", fontsize=13, color=WHITE)

doc.save(OUT_PATH)
doc.close()
print(f"Saved {OUT_PATH}")
