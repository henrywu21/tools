const puppeteer = require('/usr/local/lib/node_modules/puppeteer');
const fs = require('fs');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getContent(url, outputFile) {
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();

  retries = 0

  while (retries < 2) {
    try {
      const response = await page.goto(url, {waitUntil: 'networkidle0'});
      const status = response._status
    
      if (status == '200') {
        const html = await page.content();
        fs.writeFile(outputFile, html, function (err) {
          if (err) throw err;
        });

        console.info('Success');
        break;
      } else {
        console.error('Fail to load [' + url + '] w/ status code: ' + status);
      }
    } catch (error) {
      console.error('Exception: ' + error)
    }

    console.info('Retrying ' + ++retries);
    await sleep(3000)
  }

  await browser.close();
};

const myArgs = process.argv.slice(2);
const url = myArgs[0]
const outputFile = myArgs[1]

getContent(url, outputFile);