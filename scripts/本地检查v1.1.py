#!/usr/bin/env python3
"""教学新写的本地检查工具，非原始制作记录。检查环境需html5lib、pypdf和Pillow。"""
import argparse
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote, quote
from urllib.request import build_opener, ProxyHandler
import html5lib
from pypdf import PdfReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
LOCAL_HTTP=build_opener(ProxyHandler({}))
PRIVATE_PATTERNS=(r'7\s*岁的儿子',r'7\s*岁儿子',r'Bruce'+r' Ding','丁'+'海祥',r'\b\d{17}[0-9Xx]\b',r'住院号[：:]\s*\d',r'手机号[：:]\s*\d',r'已'+r'全面验收')


class RefParser(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if values.get('id'):self.ids.append(values['id'])
        for key in ('href','src'):
            if values.get(key):self.refs.append(values[key])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8875/')
    parser.add_argument('--publication',action='store_true',help='核对已明确的公开文件范围，允许独立Git仓库')
    args=parser.parse_args(); failures=[];records=[];html_errors=[];privacy=[]
    paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts)
    if args.publication:
        paths=[p for p in paths if not (p.parent==ROOT/'books' and p.name.endswith('v1.0.pdf'))]
        if (ROOT/'.git').exists():
            tracked=subprocess.check_output(['git','-C',str(ROOT),'ls-files','-z']).decode().split('\0')
            if any(name.startswith('../') for name in tracked):failures.append('Parent project leaked into repository')
    pages=sorted(ROOT.glob('course/*.html'))+sorted(ROOT.glob('*.html'))
    anchors={}
    for page in pages:
        text=page.read_text();refs=RefParser();refs.feed(text);anchors[page.resolve()]=set(refs.ids)
        if len(set(refs.ids))!=len(refs.ids):failures.append(str(page.relative_to(ROOT))+': duplicate ids')
        hp=html5lib.HTMLParser();hp.parse(text)
        if hp.errors:html_errors.append({'file':page.relative_to(ROOT).as_posix(),'errors':hp.errors})
        if re.search(r'(?:href|src)="[^"\n]*[\u4e00-\u9fff]',text):failures.append(page.name+': unencoded URL')
    for path in paths:
        rel=path.relative_to(ROOT).as_posix()
        if path.stat().st_size>=50_000_000:failures.append(rel+': exceeds 50MB')
        if path.is_symlink():failures.append(rel+': symlink')
        if path.name not in ('index.html','404.html','README.md','LICENSE','.gitignore','.gitattributes','.nojekyll','style.css'):
            if '_' in path.name or not re.fullmatch(r'.+v\d+\.\d+\.[a-zA-Z0-9]+',path.name):failures.append(rel+': filename convention')
        if path.suffix in ('.html','.md','.py','.js','.json','.css','.txt'):
            text=path.read_text()
            for rule,pattern in enumerate(PRIVATE_PATTERNS,1):
                if re.search(pattern,text):privacy.append({'file':rel,'rule':rule})
            if path.suffix in ('.html','.md'):
                if path.suffix=='.html':rp=RefParser();rp.feed(text);refs=rp.refs
                else:refs=re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)',text);rp=RefParser();rp.feed(text);refs+=rp.refs
                for ref in refs:
                    parts=urlsplit(ref)
                    if parts.scheme or parts.netloc:continue
                    if parts.path.startswith('/'):failures.append(rel+': absolute site path');continue
                    target=(path.parent/unquote(parts.path)).resolve() if parts.path else path.resolve()
                    if args.publication and target not in paths:failures.append(rel+': excluded publication target '+ref);continue
                    if not target.is_relative_to(ROOT.resolve()) or not target.is_file():failures.append(rel+': missing '+ref);continue
                    if parts.fragment and target.suffix=='.html' and unquote(parts.fragment) not in anchors[target]:failures.append(rel+': missing anchor '+ref)
                    url=urljoin(args.url,quote(target.relative_to(ROOT).as_posix(),safe='/'))
                    try:
                        with LOCAL_HTTP.open(url,timeout=8) as response:status=response.status;response.read(1)
                    except Exception as error:failures.append(rel+': '+str(error));continue
                    records.append({'source':rel,'reference':ref,'url':url,'status':status})
    screenshots=list((ROOT/'course/assets/pages').glob('*.webp'))
    if len(screenshots)!=12:failures.append('Need exactly 12 actual-page screenshots')
    for file in screenshots:
        if file.stat().st_size>=300_000:failures.append(file.name+': exceeds 300KB')
        with Image.open(file) as im:
            if im.size not in ((662,936),(936,662)):failures.append(file.name+': unexpected actual-page dimensions')
    material=json.loads((ROOT/'docs/证据/公开副本核对v1.1.json').read_text())
    for row in material:
        copy=ROOT/row['copy'];source=ROOT/row['source']
        if hashlib.sha256(copy.read_bytes()).hexdigest()!=row['sha256']:failures.append('Publication copy hash differs')
        if source.exists() and hashlib.sha256(source.read_bytes()).hexdigest()!=row['sourceSha256']:failures.append('Source copy hash differs')
        if len(PdfReader(copy).pages)!=row['pages']:failures.append('Publication page count differs')
        if '预览' in copy.name and copy.stat().st_size>=10_000_000:failures.append('Preview exceeds 10MB')
        reader=PdfReader(copy)
        if (reader.metadata or {}).get('/Author')!='Haixiang Ding, MD (adaptation organiser)':failures.append('Missing PDF author disclosure')
        for page in reader.pages:
            if 'AI-assisted adaptation with Hark' not in (page.extract_text() or ''):failures.append('Missing per-page AI disclosure')
    example=ROOT/'examples/输出/五页排版示例v1.1.pdf'
    if len(PdfReader(example).pages)!=5:failures.append('Example not five pages')
    pdf_text_pages=0
    for file in sorted(p for p in paths if p.parent==ROOT/'books' and p.suffix=='.pdf')+[example]:
        for index,page in enumerate(PdfReader(file).pages,1):
            pdf_text_pages+=1
            for rule,pattern in enumerate(PRIVATE_PATTERNS,1):
                if re.search(pattern,page.extract_text() or ''):privacy.append({'file':file.relative_to(ROOT).as_posix(),'page':index,'rule':rule})
    if (ROOT/'.git').exists() and not args.publication:failures.append('Use --publication for the authorised independent repository')
    result={'url':args.url,'htmlPages':len(pages),'htmlErrors':html_errors,'localReferenceChecks':len(records),'links':records,'privacySearchMatches':privacy,'pdfTextPagesScanned':pdf_text_pages,'fileCount':len(paths),'totalBytes':sum(p.stat().st_size for p in paths),'largestFile':max(({'file':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size} for p in paths),key=lambda x:x['bytes']),'actualScreenshots':len(screenshots),'examplePages':5,'failures':failures}
    (ROOT/'docs/证据/本地检查v1.1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if failures or html_errors or privacy:raise SystemExit(json.dumps({'failures':failures,'htmlErrors':html_errors,'privacy':privacy},ensure_ascii=False))
    print(json.dumps({k:v for k,v in result.items() if k not in ('links','htmlErrors','privacySearchMatches')},ensure_ascii=False))


if __name__=='__main__':main()
