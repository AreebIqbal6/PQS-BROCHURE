const fs = require('fs');

let html = fs.readFileSync('orig_utf8.html', 'utf8');

// Fix paths first
html = html.replace(/file:\/\/\/C%3A\/Users\/Noman%20Traders\/OneDrive\/Desktop\/PQS\/pqs-website\/public\//g, './');
html = html.replace(/file:\/\/\/C:\/Users\/Noman%20Traders\/Desktop\/PQS\/pqs-website\/public\//g, './');

// Increase stamp size on contact page (make it super big as requested previously)
html = html.replace(/\.contact \.stamp-contact \{ width: 120px; height: 120px; object-fit: contain;  opacity: 0.9;  margin-bottom: 60px; \}/g, '.contact .stamp-contact { width: 300px; height: 300px; object-fit: contain; opacity: 0.9; margin-bottom: 30px; }');

const pages = html.split(/<!-- PAGE \d+:.*?-->/);

// Extract the base64 image from Page 2's image tag
const p2_img_match = pages[2].match(/src="(data:image\/[^"]+)"/);
const p2_base64 = p2_img_match ? p2_img_match[1] : '';

// Create the CSS rule for .page2-bg and watermark
const customCss = `
.page2-bg {
  background: linear-gradient(160deg, rgba(10,30,53,0.92) 0%, rgba(10,30,53,0.85) 100%), url('${p2_base64}');
  background-size: cover;
  background-position: center;
  position: relative;
}
.watermark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  opacity: 0.08;
  pointer-events: none;
  z-index: 0;
}
.page-content {
  position: relative;
  z-index: 1;
}
.collage {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 150px 150px;
  gap: 10px;
  margin: 20px 0;
  width: 80%;
}
.collage img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid var(--gold);
}
`;

// Insert the new CSS into the <style> section
html = html.replace('</style>', customCss + '\n</style>');

const bodyStart = html.indexOf('<body>') + 6;
const bodyEnd = html.indexOf('</body>');

// PAGE 1: COVER
// We need to inject the "Who We Are" text and the collage into the Cover page.
// The cover page is pages[1]
let coverHtml = `
<div class="page cover" style="background: linear-gradient(160deg, rgba(10,30,53,0.95) 0%, rgba(10,30,53,0.90) 100%), url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEBLAEsAAD/6xeGSlAAAQAAAAEAABd8anVtYgAAAB5qdW1kYzJwYQA'); background-size: cover; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: #fff; padding: 15mm; box-sizing: border-box;">
  <img src="./pqs_3letter_gold.png" class="cover-banner" alt="Precision Quality Services" style="width: 80%; max-width: 500px; margin-bottom: 20px;">
  
  <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0; max-width: 600px; margin-bottom: 20px; text-align: left;">
    <h3 style="color: var(--gold); font-size: 16pt; margin-bottom: 8px;">Who We Are</h3>
    <p style="font-size: 11pt; line-height: 1.5; color: #eee; font-family: 'Lato', sans-serif;">Specialized textile consultancy and training company helping organizations improve quality, productivity, and process control. Our work is rooted in the real challenges of the factory floor.</p>
  </div>

  <div class="collage">
    <img src="./loom.jpg">
    <img src="./threads.jpg">
    <img src="./inspector.jpg">
    <img src="./microscope.jpg">
  </div>
  
  <div style="margin-top: auto;">
    <h3 class="tag" style="color: #fff; font-size: 14pt; font-weight: 300; letter-spacing: 2px;">TEXTILE CONSULTANCY | TRAINING | TROUBLESHOOTING</h3>
  </div>
</div>
`;


const newBody = `
<!-- PAGE 1: COVER -->
` + coverHtml + `

<!-- PAGE 2: EVERYTHING ELSE -->
<div class="page page2-bg" style="color: #fff; display: flex; flex-direction: column; padding: 15mm; box-sizing: border-box;">
  <img src="./pqs_3letter_gold.png" class="watermark">
  
  <div class="page-content" style="display: flex; flex-direction: column; height: 100%;">
    <div style="background: transparent; padding: 0; margin-bottom: 10mm; display:flex; justify-content:space-between; align-items:center;">
      <h2 style="color:var(--gold); font-size:24pt; margin:0;">Precision Quality Services</h2>
      <img src="./pqs_3letter_gold.png" style="height: 35px;">
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; flex: 1;">
      
      <!-- LEFT COLUMN -->
      <div style="display: flex; flex-direction: column; gap: 6mm;">
        
        <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0;">
          <h3 style="color: var(--gold); font-size: 15pt; margin-bottom: 8px;">Vision & Mission</h3>
          <p style="font-size: 11pt; line-height: 1.5; color: #eee; font-family: 'Lato', sans-serif;">To be a trusted partner delivering practical knowledge, effective solutions, and measurable improvements that strengthen people, processes, and product quality.</p>
        </div>

        <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0;">
          <h3 style="color: var(--gold); font-size: 15pt; margin-bottom: 10px;">Our Approach</h3>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div><strong style="color: #fff; font-size: 11pt;">1. Understand:</strong><br><span style="font-size: 10pt; color:#ccc;">Map processes</span></div>
            <div><strong style="color: #fff; font-size: 11pt;">2. Analyze:</strong><br><span style="font-size: 10pt; color:#ccc;">Examine data</span></div>
            <div><strong style="color: #fff; font-size: 11pt;">3. Identify:</strong><br><span style="font-size: 10pt; color:#ccc;">Root causes</span></div>
            <div><strong style="color: #fff; font-size: 11pt;">4. Improve:</strong><br><span style="font-size: 10pt; color:#ccc;">Corrective actions</span></div>
            <div><strong style="color: #fff; font-size: 11pt;">5. Implement:</strong><br><span style="font-size: 10pt; color:#ccc;">Support execution</span></div>
            <div><strong style="color: #fff; font-size: 11pt;">6. Sustain:</strong><br><span style="font-size: 10pt; color:#ccc;">Long-term controls</span></div>
          </div>
        </div>

        <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0;">
          <h3 style="color: var(--gold); font-size: 15pt; margin-bottom: 8px;">Why Choose PQS</h3>
          <ul style="font-size: 11pt; color: #eee; list-style: none; padding: 0; font-family: 'Lato', sans-serif;">
            <li style="margin-bottom: 5px;"><span style="color:var(--gold);">◆</span> Practical Industry Focus</li>
            <li style="margin-bottom: 5px;"><span style="color:var(--gold);">◆</span> Customized Solutions</li>
            <li style="margin-bottom: 5px;"><span style="color:var(--gold);">◆</span> Quality-Oriented Approach</li>
            <li style="margin-bottom: 5px;"><span style="color:var(--gold);">◆</span> Problem-Solving Mindset</li>
          </ul>
        </div>

      </div>

      <!-- RIGHT COLUMN -->
      <div style="display: flex; flex-direction: column; gap: 6mm;">
        
        <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0;">
          <h3 style="color: var(--gold); font-size: 15pt; margin-bottom: 12px;">Core Services</h3>
          
          <div style="margin-bottom: 12px;">
            <h4 style="color: #fff; font-size: 12pt; margin-bottom: 3px;">Training</h4>
            <p style="font-size: 10pt; color: #ccc; font-family: 'Lato', sans-serif;">Quality management, Defect identification, Process control fundamentals.</p>
          </div>
          <div style="margin-bottom: 12px;">
            <h4 style="color: #fff; font-size: 12pt; margin-bottom: 3px;">Consultancy</h4>
            <p style="font-size: 10pt; color: #ccc; font-family: 'Lato', sans-serif;">Quality system improvement, Process mapping, CAPA implementation.</p>
          </div>
          <div style="margin-bottom: 12px;">
            <h4 style="color: #fff; font-size: 12pt; margin-bottom: 3px;">Troubleshooting</h4>
            <p style="font-size: 10pt; color: #ccc; font-family: 'Lato', sans-serif;">Data & defect analysis, Root cause resolution, Permanent verification.</p>
          </div>
        </div>

        <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0;">
          <h3 style="color: var(--gold); font-size: 15pt; margin-bottom: 8px;">Value Delivered</h3>
          <ul style="font-size: 11pt; color: #eee; list-style: none; padding: 0; font-family: 'Lato', sans-serif;">
            <li style="margin-bottom: 6px;"><strong style="color: #fff;">Improved quality:</strong> Consistent output</li>
            <li style="margin-bottom: 6px;"><strong style="color: #fff;">Reduced defects:</strong> Lower waste and rework</li>
            <li style="margin-bottom: 6px;"><strong style="color: #fff;">Process control:</strong> Stability across stages</li>
            <li style="margin-bottom: 6px;"><strong style="color: #fff;">Employee dev:</strong> Stronger technical capability</li>
          </ul>
        </div>
        
        <div style="background: rgba(255,255,255,0.05); border-left: 4px solid var(--gold); padding: 15px; border-radius: 0 8px 8px 0;">
          <h3 style="color: var(--gold); font-size: 15pt; margin-bottom: 8px;">Who We Serve</h3>
          <p style="font-size: 11pt; color: #ccc; font-family: 'Lato', sans-serif; line-height: 1.6;">Spinning &bull; Weaving &bull; Knitting &bull; Dyeing<br>Finishing &bull; Garments</p>
        </div>

      </div>
    </div>
  </div>
</div>
` + pages[7]; // pages[7] is Contact

const newHtml = html.slice(0, bodyStart) + newBody + html.slice(bodyEnd);
fs.writeFileSync('PQS_Company_Profile.html', newHtml, 'utf8');
fs.copyFileSync('PQS_Company_Profile.html', '../PQS-WEBSITE1/public/all_assets/PQS_Company_Profile.html');
console.log('Condensed successfully with big watermark and new cover layout!');
