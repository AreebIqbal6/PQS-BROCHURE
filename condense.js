const fs = require('fs');

const html = fs.readFileSync('PQS_Company_Profile.html', 'utf8');
const bodyStart = html.indexOf('<body>') + 6;
const bodyEnd = html.indexOf('</body>');

const newBody = `
<!-- PAGE 1: COVER -->
` + html.slice(html.indexOf('<!-- PAGE 1: COVER -->'), html.indexOf('<!-- PAGE 2: WHO WE ARE -->')) + `

<!-- PAGE 2: WHO WE ARE & SERVICES -->
<div class="page">
  <div class="hdr"><h2>Who We Are & Core Services</h2><div style="display:flex; align-items:center; gap: 18px;"><span class="pn">01</span><img src="file:///C%3A/Users/Noman%20Traders/OneDrive/Desktop/PQS/pqs-website/public/pqs_3letter_gold.png" style="height: 20px;"></div></div>
  <div class="gold-line"></div>
  <div class="bg-num">01</div>
  <div class="p2-body" style="padding-top: 15px; padding-bottom: 10px;">
    <div class="intro">
      <p style="margin-bottom: 10px; font-size: 11pt;"><strong>Precision Quality Services (PQS)</strong> is a specialized textile consultancy and training company focused on helping textile organizations improve quality, productivity, process control, and operational performance. We combine technical knowledge with hands-on problem-solving.</p>
    </div>
    <div class="vm-row" style="margin-top: 15px; gap: 15px;">
      <div class="vmbox" style="padding: 15px;">
        <h3 style="font-size: 14pt;">Our Vision & Mission</h3>
        <p style="font-size: 11pt;">To become a trusted partner delivering practical knowledge, effective solutions, and measurable improvements in quality and performance.</p>
      </div>
      <div class="vmbox" style="padding: 15px;">
        <h3 style="font-size: 14pt;">Core Expertise</h3>
        <p style="font-size: 11pt;">Training, Consultancy, and Troubleshooting to strengthen people, processes, and product quality.</p>
      </div>
    </div>
  </div>
  
  <div class="p3-bg" style="flex: 1.5;">
    <div class="svc-grid" style="display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1fr;">
      <div class="svc" style="padding: 15px; flex-direction: column; align-items: flex-start; gap: 10px;">
        <h3 style="font-size: 16pt;">Training</h3>
        <div class="desc" style="font-size: 11pt; margin-bottom: 10px;">Practical programmes for production & quality teams.</div>
        <ul style="display: block;">
          <li style="font-size: 10pt; margin-bottom: 5px;">Quality management</li>
          <li style="font-size: 10pt; margin-bottom: 5px;">Defect identification</li>
          <li style="font-size: 10pt; margin-bottom: 5px;">Process control</li>
        </ul>
      </div>
      <div class="svc" style="padding: 15px; flex-direction: column; align-items: flex-start; gap: 10px;">
        <h3 style="font-size: 16pt;">Consultancy</h3>
        <div class="desc" style="font-size: 11pt; margin-bottom: 10px;">Build effective, practical quality systems.</div>
        <ul style="display: block;">
          <li style="font-size: 10pt; margin-bottom: 5px;">Process mapping</li>
          <li style="font-size: 10pt; margin-bottom: 5px;">Performance improvement</li>
          <li style="font-size: 10pt; margin-bottom: 5px;">CAPA implementation</li>
        </ul>
      </div>
      <div class="svc" style="padding: 15px; flex-direction: column; align-items: flex-start; gap: 10px;">
        <h3 style="font-size: 16pt;">Troubleshooting</h3>
        <div class="desc" style="font-size: 11pt; margin-bottom: 10px;">Resolve recurring issues at the source.</div>
        <ul style="display: block;">
          <li style="font-size: 10pt; margin-bottom: 5px;">Data & defect analysis</li>
          <li style="font-size: 10pt; margin-bottom: 5px;">Root cause analysis</li>
          <li style="font-size: 10pt; margin-bottom: 5px;">Verification of results</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="ftr"><span class="fl">Precision Quality Services</span><span class="fc">Textile Training | Consultancy | Troubleshooting</span><span class="fr">02</span></div>
</div>

<!-- PAGE 3: APPROACH & VALUE -->
<div class="page">
  <div class="hdr"><h2>Our Approach & Value</h2><div style="display:flex; align-items:center; gap: 18px;"><span class="pn">02</span><img src="file:///C%3A/Users/Noman%20Traders/OneDrive/Desktop/PQS/pqs-website/public/pqs_3letter_gold.png" style="height: 20px;"></div></div>
  <div class="gold-line"></div>
  <div class="bg-num">02</div>
  
  <div class="p4-bg" style="flex: 1;">
    <div class="appr-intro" style="font-size: 13pt; padding-top: 10px;">A structured, practical engagement.</div>
    <div class="steps" style="grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1fr 1fr; margin: 10px 15mm; gap: 10px;">
      <div class="step" style="padding: 10px;"><div class="num" style="font-size: 24pt;">01</div><h4 style="font-size: 10pt;">Understand</h4><p style="font-size: 9pt;">Map processes and challenges.</p></div>
      <div class="step" style="padding: 10px;"><div class="num" style="font-size: 24pt;">02</div><h4 style="font-size: 10pt;">Analyze</h4><p style="font-size: 9pt;">Examine data and quality issues.</p></div>
      <div class="step" style="padding: 10px;"><div class="num" style="font-size: 24pt;">03</div><h4 style="font-size: 10pt;">Identify</h4><p style="font-size: 9pt;">Pinpoint root causes.</p></div>
      <div class="step" style="padding: 10px;"><div class="num" style="font-size: 24pt;">04</div><h4 style="font-size: 10pt;">Improve</h4><p style="font-size: 9pt;">Develop corrective actions.</p></div>
      <div class="step" style="padding: 10px;"><div class="num" style="font-size: 24pt;">05</div><h4 style="font-size: 10pt;">Implement</h4><p style="font-size: 9pt;">Support during implementation.</p></div>
      <div class="step" style="padding: 10px;"><div class="num" style="font-size: 24pt;">06</div><h4 style="font-size: 10pt;">Sustain</h4><p style="font-size: 9pt;">Establish long-term controls.</p></div>
    </div>
  </div>
  
  <div class="p5-bg" style="flex: 1.2;">
    <div class="val-grid">
      <div class="val-l" style="padding: 15px 15mm;">
        <h3 style="font-size: 16pt;">Value Delivered</h3>
        <div class="vi" style="margin-bottom: 8px;"><span class="bul">■</span><div><strong style="font-size: 11pt;">Improved quality</strong><span style="font-size: 10pt;">Consistent output</span></div></div>
        <div class="vi" style="margin-bottom: 8px;"><span class="bul">■</span><div><strong style="font-size: 11pt;">Reduced defects</strong><span style="font-size: 10pt;">Lower waste and rework</span></div></div>
        <div class="vi" style="margin-bottom: 8px;"><span class="bul">■</span><div><strong style="font-size: 11pt;">Process control</strong><span style="font-size: 10pt;">Stability across stages</span></div></div>
      </div>
      <div class="val-r" style="padding: 15px 15mm;">
        <h3 style="font-size: 16pt;">Why Choose PQS</h3>
        <div class="wi" style="margin-bottom: 8px;"><h5><span class="dm">◆</span><span style="font-size: 10pt;">Practical Industry Focus</span></h5></div>
        <div class="wi" style="margin-bottom: 8px;"><h5><span class="dm">◆</span><span style="font-size: 10pt;">Customized Solutions</span></h5></div>
        <div class="wi" style="margin-bottom: 8px;"><h5><span class="dm">◆</span><span style="font-size: 10pt;">Quality-Oriented Approach</span></h5></div>
        <div class="wi" style="margin-bottom: 8px;"><h5><span class="dm">◆</span><span style="font-size: 10pt;">Problem-Solving Mindset</span></h5></div>
      </div>
    </div>
  </div>
  
  <div class="serve" style="margin: 10px 15mm; padding: 15px; text-align: center;">
      <h3 style="font-size: 14pt; margin-bottom: 5px;">Who We Serve</h3>
      <div class="tags" style="font-size: 10pt; margin: 5px 0;">Spinning &bull; Weaving &bull; Knitting &bull; Dyeing &bull; Finishing &bull; Garments</div>
  </div>

  <div class="ftr"><span class="fl">Precision Quality Services</span><span class="fc">Textile Training | Consultancy | Troubleshooting</span><span class="fr">03</span></div>
</div>
` + html.slice(html.indexOf('<!-- PAGE 7: CONTACT -->'));

const newHtml = html.slice(0, bodyStart) + newBody + html.slice(bodyEnd);
fs.writeFileSync('PQS_Company_Profile.html', newHtml, 'utf8');
fs.copyFileSync('PQS_Company_Profile.html', '../PQS-WEBSITE1/public/all_assets/PQS_Company_Profile.html');
console.log('Condensed successfully!');
