const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    headless: true,
    args: ['--force-device-scale-factor=1', '--no-sandbox']
  }).catch(async (e) => {
    return await puppeteer.launch({
      executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
      headless: true,
      args: ['--force-device-scale-factor=1', '--no-sandbox']
    });
  });

  const page = await browser.newPage();
  
  const htmlPath = 'file:///' + path.resolve('PQS_Company_Profile.html').replace(/\\/g, '/');
  const pdfPath = path.resolve('PQS_Company_Profile_4Pages.pdf');
  
  await page.goto(htmlPath, { waitUntil: 'networkidle0' });
  
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' }
  });
  
  await browser.close();
  console.log('PDF generated successfully!');
})();
