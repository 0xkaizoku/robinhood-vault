const puppeteer = require('puppeteer-core');
const path = require('path');

(async () => {
  try {
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const htmlPath = path.join(__dirname, 'report.html');
    const pdfPath = path.join(__dirname, 'Robinhood_Chain_Research_and_Strategy_Report.pdf');

    const browser = await puppeteer.launch({
      executablePath: chromePath,
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`, {
      waitUntil: 'networkidle0'
    });

    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: {
        top: '15mm',
        right: '15mm',
        bottom: '15mm',
        left: '15mm'
      }
    });

    await browser.close();
    console.log(`PDF successfully created at: ${pdfPath}`);
  } catch (err) {
    console.error('Error generating PDF:', err);
    process.exit(1);
  }
})();
