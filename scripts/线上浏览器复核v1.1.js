/* 教学新写检查工具，非原始制作记录。需要维护者环境中的Playwright和Chrome。 */
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const base = process.env.COURSE_TEST_URL || 'https://tuanziding.github.io/comic-companion-course/';
const evidence = path.join(root, 'docs', '证据');
const spec = JSON.parse(fs.readFileSync(path.join(evidence, '课程结构v1.0.json'), 'utf8'));
const encodePath = name => name.split('/').map(encodeURIComponent).join('/');
const routes = ['index.html', ...spec.lessons.map(x => x.file)];
const sizes = [375, 768, 1280];
const rgb = text => (text.match(/[\d.]+/g) || []).slice(0,3).map(Number);
const luminance = values => values.map(v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((a,v,i) => a + v * [.2126,.7152,.0722][i],0);
const ratio = (a,b) => { const values=[luminance(rgb(a)),luminance(rgb(b))].sort((x,y)=>y-x); return (values[0]+.05)/(values[1]+.05); };
async function main() {
  const browser = await chromium.launch({headless:true,executablePath:process.env.COURSE_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  const context = await browser.newContext({viewport:{width:1280,height:900},reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
  const page = await context.newPage(); const errors=[]; const failedRequests=[]; const layouts=[]; const contrasts=[]; const screenshots=[];
  page.on('pageerror',error=>errors.push(String(error)));
  page.on('console',msg=>{if(msg.type()==='error')errors.push(msg.text());});
  page.on('response',response=>{if(response.status()>=400)failedRequests.push(response.url()+': '+response.status());});
  await context.route('**/*',route=>{ if(new URL(route.request().url()).origin!==new URL(base).origin) return route.abort(); return route.continue(); });
  for (const width of sizes) {
    await page.setViewportSize({width,height:width===375?812:900});
    for (const route of routes) {
      await page.goto(base+encodePath(route),{waitUntil:'networkidle'});
      await page.evaluate(()=>document.querySelectorAll('img[loading]').forEach(img=>img.loading='eager'));
      await page.waitForFunction(()=>[...document.querySelectorAll('img:not(.dialog-image)')].every(img=>img.complete&&img.naturalWidth>0));
      for (const theme of ['light','dark']) {
        await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;},theme);
        const check=await page.evaluate(()=>({body:document.body.scrollWidth,viewport:innerWidth,clipped:[...document.querySelectorAll('h1,h2,h3,p,pre,label,.course-card')].filter(el=>el.getClientRects().length&&el.scrollWidth>el.clientWidth+2).map(el=>el.tagName+': '+el.textContent.slice(0,50))}));
        layouts.push({route,width,theme,...check});
        if(check.body>width+1||check.clipped.length)throw new Error('Overflow '+JSON.stringify(layouts.at(-1)));
        if(route==='index.html' && theme==='light' && [375,1280].includes(width)){
          const label=route==='index.html'?'首页':route===spec.lessons[6].file?'第06课':'第10课';
          const file=`Pages${label}${width}${theme==='light'?'浅色':'深色'}v1.1.png`;
          await page.screenshot({path:path.join(evidence,file),fullPage:true});screenshots.push(file);
        }
      }
    }
    console.log(`Layout passed at ${width}px for 13 routes and two themes.`);
  }
  await page.goto(base+encodePath(spec.lessons[0].file));
  await page.locator('[data-copy]').click();await page.waitForFunction(()=>document.querySelector('[data-copy]').textContent==='已复制');
  const expected=await page.locator('pre#prompt-00').textContent(); const copied=await page.evaluate(()=>navigator.clipboard.readText());
  if(copied!==expected)throw new Error('Clipboard content mismatch');
  await page.screenshot({path:path.join(evidence,'Pages复制反馈v1.1.png')});
  await page.locator('[data-complete]').check();
  if(!await page.locator('[data-progress-text]').textContent().then(t=>t.startsWith('1 / 12')))throw new Error('Progress failed');
  await page.reload();if(!await page.locator('[data-complete]').isChecked())throw new Error('Progress persistence failed');
  await page.locator('[data-theme-toggle]').click();const theme=await page.evaluate(()=>document.documentElement.dataset.theme);await page.reload();if(theme!==await page.evaluate(()=>document.documentElement.dataset.theme))throw new Error('Theme persistence failed');
  await page.locator('[data-enlarge]').first().click();if(!await page.locator('dialog').evaluate(x=>x.open))throw new Error('Gallery failed');
  if(!await page.locator('dialog').evaluate(x=>x.contains(document.activeElement)))throw new Error('Gallery focus did not enter');
  for(const key of ['Tab','Shift+Tab','Tab']){await page.keyboard.press(key);if(!await page.locator('dialog').evaluate(x=>x.contains(document.activeElement)))throw new Error('Gallery tab focus escaped');}
  await page.keyboard.press('Escape');if(await page.locator('dialog').evaluate(x=>x.open))throw new Error('Gallery keyboard close failed');
  if(!await page.locator('[data-enlarge]').first().evaluate(x=>x===document.activeElement))throw new Error('Gallery focus did not return');
  await page.setViewportSize({width:375,height:812});await page.reload();
  await page.evaluate(()=>{window.clipboardBeforeFallback=navigator.clipboard;Object.defineProperty(navigator,'clipboard',{value:undefined,configurable:true});});
  await page.locator('[data-copy]').click();await page.waitForFunction(()=>document.querySelector('[data-copy]').textContent==='已复制');
  const fallbackCopied=await page.evaluate(()=>window.clipboardBeforeFallback.readText());
  if(fallbackCopied!==expected)throw new Error('Fallback clipboard content mismatch');
  await page.screenshot({path:path.join(evidence,'Pages手机复制反馈v1.1.png')});
  await page.goto(base);
  for(const themeName of ['light','dark']){
    const palette=await page.evaluate(themeName=>{
      document.documentElement.dataset.theme=themeName;const css=getComputedStyle(document.documentElement);
      const token=name=>{const probe=document.createElement('span');probe.style.color=css.getPropertyValue('--'+name);document.body.append(probe);const value=getComputedStyle(probe).color;probe.remove();return value;};
      return ['ink','paper','surface','muted','primary','on-primary','honey','on-honey','todo','on-todo','code','on-code'].reduce((a,n)=>{a[n]=token(n);return a;},{});
    },themeName);
    for(const [fg,bg] of [['ink','paper'],['ink','surface'],['muted','paper'],['muted','surface'],['primary','paper'],['primary','surface'],['on-primary','primary'],['on-honey','honey'],['on-todo','todo'],['on-code','code']]){
      const value=ratio(palette[fg],palette[bg]);contrasts.push({theme:themeName,foregroundToken:fg,backgroundToken:bg,foreground:palette[fg],background:palette[bg],ratio:value});if(value<4.5)throw new Error('Contrast failed '+JSON.stringify(contrasts.at(-1)));
    }
  }
  if(errors.length||failedRequests.length)throw new Error('Runtime errors '+JSON.stringify({errors,failedRequests}));
  fs.writeFileSync(path.join(evidence,'Pages浏览器检查v1.1.json'),JSON.stringify({browser:await browser.version(),base,viewports:sizes,routes,layouts,contrasts,screenshots,errors,failedRequests,clipboardDesktop:true,clipboardMobileFallback:true,galleryKeyboardClose:true,themePersistence:true,progressPersistence:true,network:'All external requests blocked; all local page assets loaded.'},null,2));
  await browser.close();console.log('Chrome interactions, layout, contrast and console checks passed.');
}
main().catch(error=>{console.error(error);process.exit(1);});
