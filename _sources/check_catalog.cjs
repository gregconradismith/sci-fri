const { chromium } = require('/Users/greg/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path = require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try {
  const page=await browser.newPage({viewport:{width:1280,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.resolve('00-START-HERE.html')).href);
  await page.screenshot({path:'_build/catalog-desktop.png'});
  const all=await page.locator('.card:visible').count();
  if(all!==26)throw Error('Expected 26 source cards, got '+all);
  await page.locator('#quickonly').check();
  const short=await page.locator('.card:visible').count();
  if(!(short>0 && short<all))throw Error('Short-visit filter failed');
  await page.locator('#search').fill('Mobius');
  if(await page.locator('.card:visible').count()!==1)throw Error('Mobius search failed');
  await page.locator('#search').fill('no-such-activity-9842');
  if(await page.locator('.card:visible').count()!==0)throw Error('Empty search failed');
  await page.locator('#clear').click();
  if(await page.locator('.card:visible').count()!==all)throw Error('Clear filter failed');
  await page.setViewportSize({width:390,height:844});await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:'_build/catalog-mobile.png'});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
  if(overflow)throw Error('Mobile layout overflows');
  if(errors.length)throw Error(errors.join('\n'));
  console.log(JSON.stringify({sourceCards:all,quickVisitCards:short,search:true,reset:true,mobileOverflow:overflow,pageErrors:errors}));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
