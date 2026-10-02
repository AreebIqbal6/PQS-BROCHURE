import fitz
import re

pdf_path = r'C:\Users\Noman Traders\Downloads\PQS_Company_Profile (1).pdf'
banner_path = r'C:\Users\Noman Traders\OneDrive\Desktop\PQS\golden_banner.png'
logo_3letter = r'C:\Users\Noman Traders\OneDrive\Desktop\PQS\pqs-website\public\pqs_3letter_gold.png'
bg_path = r'C:\Users\Noman Traders\OneDrive\Desktop\PQS\contact_bg.jpg'
out_path = r'C:\Users\Noman Traders\OneDrive\Desktop\PQS\PQS_Company_Profile_Final_v24.pdf'

doc = fitz.open(pdf_path)

# --- FIX PAGE 0 (Cover Page) ---
page0 = doc[0]
xref0 = page0.get_contents()[0]
cont0 = doc.xref_stream(xref0)

# Remove the white logos from the content stream
cont0 = cont0.replace(b'/X12 Do', b'')
cont0 = cont0.replace(b'/X14 Do', b'')

# We do NOT change the dash to white here. We keep it original (golden gradient)
# as requested by "keep v21 and delete everything else".
doc.update_stream(xref0, cont0)

# Insert the golden logos into the exact same bounding boxes
logo_rect = fitz.Rect(200.25, 213.75, 395.25, 398.25)
page0.insert_image(logo_rect, filename=logo_3letter, keep_proportion=True)
banner_rect = fitz.Rect(54.0, 428.25, 541.5, 478.5)
page0.insert_image(banner_rect, filename=banner_path, keep_proportion=True)


# --- FIX PAGE 4 WITH NATIVE MATRIX SCALING + SPACING ---
page4 = doc[3]
for xref in page4.get_contents():
    cont = doc.xref_stream(xref)
    # Remove the page boundary clipping paths that chopped the text in half
    cont = re.sub(rb'0 0 2480 3507\.8613 re\s+W\*? n', b'0 0 2480 3507.8613 re n', cont)
    
    # Inject split spacing before we apply the global scale
    target1 = b'.0392 .1176 .2078 RG .0392 .1176 .2078 rg\n113 4280 m'
    target2 = b'.0392 .1176 .2078 RG .0392 .1176 .2078 rg\n113 4515 m'
    
    if target1 in cont and target2 in cont:
        # Move top box UP by 10 native units
        cont = cont.replace(target1, b' q 1 0 0 1 0 -10 cm\n' + target1)
        # Close top box shift, open bottom box shift (DOWN by 15 units)
        cont = cont.replace(target2, b' Q\nq 1 0 0 1 0 15 cm\n' + target2)
        # We need to close the bottom box shift at the end of the stream.
        # But wait, we also prepend and append the 0.90 scale!
        # Let's just append the Q for the spacing first.
        cont = cont + b'\nQ\n'
    
    doc.update_stream(xref, cont)

page4.clean_contents()
xref4 = page4.get_contents()[0]
cont4 = doc.xref_stream(xref4)
# 0.90 scale with Top-Left origin translation to natively fit above the footer
cont4 = b'q 0.90 0 0 0.90 29.75 84.2 cm\n' + cont4 + b'\nQ'
doc.update_stream(xref4, cont4)


# --- COLORS ---
navy = (10/255, 30/255, 53/255)
gold = (200/255, 169/255, 81/255)
gray = (180/255, 180/255, 180/255)
white = (1, 1, 1)


# --- PROCESS PAGES 2 TO 6 (Indices 1-5) ---
for i in range(1, 6):
    target_page = doc[i]
    
    # Header: Make number white. (Removes visual gold logo via overlaying navy block)
    blocks = target_page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    text = s['text'].strip()
                    if text in ['01','02','03','04','05'] and s['bbox'][1] < 100:
                        bbox = s['bbox']
                        rect = fitz.Rect(bbox[0]-5, bbox[1]-5, bbox[2]+5, bbox[3]+5)
                        target_page.draw_rect(rect, color=navy, fill=navy)
                        point = fitz.Point(bbox[0], bbox[3] - 2.5) 
                        target_page.insert_text(point, text, fontsize=14, fontname='hebo', color=white)
    
    # Draw Navy Footer
    target_page.draw_rect(fitz.Rect(0, 785, 595, 842), color=navy, fill=navy)
    
    # 1. Golden Banner
    target_page.insert_image(fitz.Rect(30, 802, 205, 820), filename=banner_path)
    
    # 2. Center text
    center_text = "TEXTILE TRAINING | CONSULTANCY | TROUBLESHOOTING"
    target_page.insert_text(fitz.Point(245, 820), center_text, fontname="helv", fontsize=8.5, color=gray)
    
    # 3. Page number
    page_num = f"0{i}"
    target_page.insert_text(fitz.Point(510, 820), page_num, fontname="hebo", fontsize=9, color=gold)


# --- FIX PAGE 6 (Contact) ---
page6 = doc[6]
xref6 = page6.get_contents()[0]
cont6 = doc.xref_stream(xref6)

# Remove ALL original backgrounds
grey_fill = b'.9922 .9882 .9765 RG .9922 .9882 .9765 rg\n/G3 gs\n0 0 794 1123 re\nf\n'
white_fill = b'1 1 1 RG 1 1 1 rg\n/G3 gs\n/NonStruct <</MCID 0 >>BDC\n0 6738 794 1123 re\nf\n'
navy_fill = b'.0392 .1176 .2078 RG .0392 .1176 .2078 rg\n/G3 gs\nEMC\n/NonStruct <</MCID 1 >>BDC\n0 6738 794 1135 re\nf\n'

if grey_fill in cont6: cont6 = cont6.replace(grey_fill, b'')
if white_fill in cont6: cont6 = cont6.replace(white_fill, b'')
if navy_fill in cont6: cont6 = cont6.replace(navy_fill, b'')
if b'/X90 Do' in cont6: cont6 = cont6.replace(b'/X90 Do', b'')

doc.update_stream(xref6, cont6)

# Draw new background
page6.insert_image(page6.rect, filename=bg_path, keep_proportion=False, overlay=False)

# Keep the 3-letter gold logo for the contact page
logo_rect = fitz.Rect(252, 107.5, 342, 152.5)
page6.insert_image(logo_rect, filename=logo_3letter)


doc.save(out_path)
doc.close()
print(f"Saved {out_path}!")
