from pathlib import Path
import json, html, hashlib, shutil
from urllib.parse import quote
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent.parent
manifest=json.loads((ROOT/'_sources/manifest.json').read_text())
manifest+=json.loads((ROOT/'_sources/expansion-manifest.json').read_text())
downloaded=[r for r in manifest if r['status']=='downloaded']
for r in downloaded:r['pages']=len(PdfReader(ROOT/r['file']).pages)
total=sum(r['pages'] for r in downloaded)+19
pdf_count=len(downloaded)+2
e=html.escape
previews=ROOT/'_sources/previews';previews.mkdir(exist_ok=True)

print_pages={
 'JRMF-Map-Coloring':'6-14 (instructions and student maps); leader answers: 5',
 'JRMF-Color-Triangles':'2-4 to start; 5-6 for extensions. Color printing helpful.',
 'JRMF-Hexaflexagons':'5-8 once per table; 9 per child. Color printing recommended.',
 'JRMF-Chomp':'2 for rules; 3-5 for starting boards and challenges.',
 'JRMF-Sprigs':'7 and 9 to start; 8 is a different variant. Leader answers: 6.',
 'JRMF-Pentominoes':'7-8 for pieces; 9-16 for boards. Leader answers: 5-6.',
 'JRMF-Doodles':'6-12 (instructions and puzzles). Leader answers: 5.',
 'Math-for-Love-Games-to-Play-at-Home':'1 for Nim; 2 for Dots and Boxes; 5 for Blockout (two dice).',
 'Gould-Orbifold-Patterns-and-Matching-Cards':'1-6 matching cards; 7-12 folding patterns. Leader key: 13-15.',
 'Gould-Bringing-Orbifolds-out-of-the-Plane':'Read all 6 pages as leader preparation; folding instructions on PDF p. 4.',
 'Vi-Hart-Orbifold-and-Cut':'Leader reading: 4 pages. Begin with paper symmetry examples on PDF p. 2.'
}
print_pages['JRMF-Frogs-and-Toads']='9 for rules and first puzzle; 11 for reusable lily pads. Leader answers: 5-8. Page 10 changes the jumping rule.'
preview_pages={'JRMF-Map-Coloring':7,'JRMF-Color-Triangles':4,'JRMF-Hexaflexagons':9,
 'JRMF-Chomp':3,'JRMF-Sprigs':7,'JRMF-Pentominoes':7,'JRMF-Doodles':7,
 'Gould-Orbifold-Patterns-and-Matching-Cards':8,'Math-for-Love-Games-to-Play-at-Home':2}

def preview(stem,page=1):
    source=sorted((ROOT/'_build/qa'/stem).glob('page-*.png'))[page-1]
    from PIL import Image
    pic=Image.open(source).convert('RGB');pic.thumbnail((300,380))
    target=previews/(stem+'.jpg');pic.save(target,quality=86)
    return '_sources/previews/'+target.name

sections=[]
for folder in sorted({r['file'].split('/')[0] for r in downloaded}):
    cards=[]
    for r in [r for r in downloaded if r['file'].startswith(folder+'/')]:
        stem=Path(r['file']).stem
        title=stem.replace('Mathigon-','Mathigon: ').replace('JRMF-','JRMF: ').replace('-',' ')
        if stem=='JRMF-Frogs-and-Toads':r['preview_page']=11
        if stem=='Hampton-A-Mathematical-Coloring-Book':r['print_pages']='Art pages 2-35. Younger children: 2, 3, 11, or 31. Fractals: 24-25. Leader notes: 36-38.'
        thumb=preview(stem,r.get('preview_page',preview_pages.get(stem,1)))
        r['print_pages']=print_pages.get(stem,r.get('print_pages','1 (whole template).'))
        quick_old={'JRMF-Map-Coloring','JRMF-Color-Triangles','JRMF-Chomp','JRMF-Sprigs','JRMF-Doodles','JRMF-Pentominoes','Math-for-Love-Games-to-Play-at-Home','Mathigon-cube-net','Mathigon-tetrahedron-net'}
        r['session']=r.get('session','Quick station: select one task; precut nets' if stem in quick_old else 'Longer / guided extension')
        quick='1' if r['session'].lower().startswith('quick') else '0'
        cards.append(f'''<article class="card" data-quick="{quick}"><a href="{quote(r['file'])}"><img src="{thumb}" alt="Preview: {e(title)}" loading="lazy"></a><div><h3><a href="{quote(r['file'])}">{e(title)}</a></h3><p class="meta">Ages {e(r['ages'])} · full activity about {r['minutes']} min · {r['pages']} PDF pages</p><p><b>{e(r['session'])}</b></p><p>{e(r['note'])}</p><p><b>Supplies:</b> {e(r['supplies'])}</p><p><b>Print:</b> {e(r['print_pages'])}</p><a href="{e(r['source'])}">Original source</a></div></article>''')
    sections.append('<section class="resource-section" id="'+folder+'"><h2>'+folder[3:].replace('-',' ')+'</h2>'+''.join(cards)+'</section>')

starter_preview=preview('00-Science-Friday-Starter-Pack')
starter='00-Science-Friday-Starter-Pack.pdf'
pageguide=[('1','Color a turning rosette','6+'),('2','Square kaleidoscope','7+'),('3','Triangular tessellation coloring','6+'),('4','Pascal triangle: odd and even','8+'),('5','Dots and Boxes: four boards','6+'),('6','Sprouts: rules and play areas','10+'),('7','Game of Life: block and blinker','9+'),('8','Game of Life: glider','9+'),('9','Game of Life: experiment grids','9+'),('10','Leader notes and answer key','Leader')]
rows=''.join(f'<tr><td>{p}</td><td><a href="{starter}#page={p}">{name}</a></td><td>{age}</td></tr>' for p,name,age in pageguide)
doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Science Friday | Printable collection</title>
<style>
:root{--ink:#21332f;--accent:#176a59;--paper:#f8f5ed;--line:#d8ded5}*{box-sizing:border-box}body{font:17px/1.55 system-ui,sans-serif;color:var(--ink);background:var(--paper);margin:0}main{max-width:1060px;margin:auto;padding:44px 28px}h1{font:700 52px/1.1 Georgia,serif;margin:10px 0 16px}h2{font:700 29px Georgia,serif;margin:38px 0 18px}h3{font-size:20px;margin:0 0 8px}a{color:var(--accent);text-underline-offset:3px}.eyebrow,.meta{font-size:13px;color:#52635b}.eyebrow{text-transform:uppercase;letter-spacing:2px}.intro{font-size:20px;max-width:800px}.box{background:white;border:1px solid var(--line);border-radius:14px;padding:24px;margin:22px 0}.card{display:flex;gap:26px;background:white;border:1px solid var(--line);padding:22px;border-radius:12px;margin:16px 0}.card img{width:155px;max-height:220px;object-fit:contain}.card p{margin:8px 0;font-size:15px}.card>div{flex:1}nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}nav a,.button{display:inline-block;border:1px solid var(--line);background:white;border-radius:8px;padding:8px 13px;text-decoration:none}.button{background:var(--accent);color:white;font-weight:600}table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;padding:9px;border-bottom:1px solid var(--line)}input{font:inherit;width:100%;padding:12px;border:1px solid #9aada1;border-radius:8px}.quiet{font-size:14px;color:#52635b}li{margin:8px 0}footer{border-top:1px solid var(--line);padding-top:24px;margin-top:40px;font-size:14px}@media(max-width:650px){main{padding:24px 16px}h1{font-size:40px}.card{display:block}.card img{width:130px;float:right;margin-left:14px}.card:after{content:"";display:table;clear:both}}@media print{nav,input,.button{display:none}body{background:white}main{padding:0}.card{break-inside:avoid}a{color:inherit}}
</style></head><body><main>
<div class="eyebrow">A collection for curious kids · October 1, 2026</div><h1>Science Friday</h1>
<p class="intro">Color a pattern. Fold a solid. Find a strategy. Watch a tiny rule create a moving world.</p>
'''
doc+=f'<p><b>{pdf_count} local PDFs · {total} pages</b>, including teacher guides and answer keys. Curated for <b>ages 5–14, about 50 children across the event, and 10–20 minute drop-in visits</b>. All local PDF links work offline. Ages and times are planning estimates; choose by interest and readiness.</p>'
doc+='''<nav><a href="#starter">Start here</a><a href="#01-Coloring-and-Symmetry">Coloring</a><a href="#02-Polyhedra-and-Folding">Folding</a><a href="#03-Paper-Games">Games</a><a href="#life">Game of Life</a><a href="#05-Orbifolds">Orbifolds</a><a href="#06-More-Math-Recreations">More puzzles</a><a href="#plan">Six Fridays</a></nav>
<section class="box" id="starter"><h2 style="margin-top:0">An easy first Friday</h2><p>Set out coloring, games, building, and puzzle stations. Children choose one small activity for a 10–20 minute visit. Four tables with four places each allow 16 children at a time, with places opening as they finish. Offer precut models and large shapes to younger visitors.</p>'''
doc+=f'<p><a class="button" href="{starter}">Open the 10-page starter pack</a></p><table><tr><th>PDF page</th><th>Original printable</th><th>Suggested age</th></tr>{rows}</table><p class="quiet">Print selected student pages 1-9. Keep page 10 for the leader. Newly created text and vector drawings, with editable Python source in _sources/build_starter_pack.py.</p></section>'
doc+='''<section class="box" id="life"><h2 style="margin-top:0">Conway's Game of Life on paper</h2><p>Print starter pages 7-9; keep page 10 as the answer key. Work in pairs: one child counts neighbors on the old grid while the other fills the next grid. Swap roles each generation. The grids show a window into an infinite plane; do not wrap at the edges.</p><p>Begin with the stationary block, then the blinking line, then the moving glider. The original answer key was checked by computing the generations.</p><p>Further exploration: <a href="https://conwaylife.com/wiki/Rulestring">LifeWiki rules</a> · <a href="https://conwaylife.com/book/">Johnston and Greene's free book and pattern collection</a> (advanced reference, not downloaded).</p></section>
<h2>Browse the local printables</h2><label for="search">Filter by topic, age, or supply</label><input id="search" type="search" placeholder="Try: cube, pencils, Mobius, cards…"><p><label><input id="quickonly" type="checkbox" style="width:auto"> Show activities with a 10–20 minute starting task</label> <button type="button" id="clear">Clear filters</button></p><p id="matches" class="quiet" aria-live="polite"></p>
'''+''.join(sections)
doc+='''<section class="box"><h2 style="margin-top:0">Printing and setup</h2><ul>
<li>Page numbers above are <b>PDF viewer page numbers</b>. Some source documents have different printed numbering.</li>
<li>Print one sample first. Use automatic orientation and “Fit” if a source is A4 or extends beyond your printer's margins. The original starter pack is US Letter.</li>
<li>For pentominoes, use the <b>same scale</b> for pieces and boards, ideally 100% if the printer permits it. Check one piece against a board before making class copies.</li>
<li>Print cutouts single-sided. Color polyhedron faces first, cut around the outside including tabs, crease the face boundaries, and glue or tape tabs inside. The cube and tetrahedron are the easiest starts. Physical assembly has not been tested here.</li>
<li>Use ordinary paper for flexagons; thick cardstock is harder to flex. A leader should practice one before the session.</li>
<li>Low-ink choices: starter pack, nets, Map Coloring worksheets, Doodles, and Pentominoes. Color is useful for Color Triangles and the flexagon instructions; the orbifold patterns use substantial ink.</li>
<li>Sprigs and Sprouts are different games. Sprigs limits dots to two ends and does not add a new dot each turn; Sprouts limits them to three and adds a new dot.</li>
</ul></section>
<section id="plan"><h2>Six Fridays to get started</h2><table><tr><th>Session</th><th>Start with</th><th>Go further</th></tr>
<tr><td>1 · Color and play</td><td>Rosette, Dots and Boxes, cube</td><td>Which colors keep a symmetry?</td></tr>
<tr><td>2 · Build a world</td><td>Tetrahedron and octahedron nets</td><td>Count vertices, edges, faces; test V − E + F = 2</td></tr>
<tr><td>3 · Rules make patterns</td><td>Color Triangles; Life block and blinker</td><td>Life glider; invent a starting pattern</td></tr>
<tr><td>4 · Strategy on paper</td><td>Chomp and Sprigs</td><td>Sprouts; explain a winning position</td></tr>
<tr><td>5 · Cut, fold, rearrange</td><td>Pentominoes and hexaflexagons</td><td>Dodecahedron; find all flexagon faces</td></tr>
<tr><td>6 · Mirrors to orbifolds</td><td>Square kaleidoscope; mirror-line hunt</td><td>Gould supplement p. 8 (*333), with paper PDF p. 4</td></tr></table>
<p>These are six themes to reuse across Fridays. For each 10–20 minute visit, choose one small task. Put longer builds on a return-visit or take-home table. For younger children, emphasize drawing, coloring, and folding; reserve orbifold notation and classification for older children or the leader.</p></section>
<section class="box"><h2 style="margin-top:0">More sources to revisit</h2><p>These are web links, not local PDFs:</p><ul>
<li><a href="https://mathequalslove.net/geometric-coloring-pages/">Sarah Carter: 15 geometric coloring pages</a> and <a href="https://mathequalslove.net/penrose-tiling-coloring-page/">Penrose tiling sheet</a>. The pages advertise free PDFs, but their download endpoints returned HTTP 403 during collection. No local copies are claimed.</li>
<li><a href="https://nrich.maths.org/games/sprouts">NRICH: Sprouts</a> for teacher discussion and extensions.</li>
<li><a href="https://mathigon.org/origami">Mathigon's larger net and origami collection</a> for more ambitious builds.</li>
<li><a href="https://jrmf.org/puzzle/">Julia Robinson Math Festival puzzle library</a> for more puzzles, beginner versions, and Spanish editions.</li>
<li><a href="https://www.geometrygames.org/KaleidoTile/index.html.en">Jeff Weeks: KaleidoTile</a> for optional digital exploration of tilings and polyhedra; no software installed.</li>
</ul></section>
<footer><h3>Sources and reuse</h3><p>Downloaded PDFs are preserved unchanged with their attribution. Each card links to its source; The manifests in _sources record download URLs, dates, and SHA-256 checksums. Original worksheets are clearly identified. Availability as a free download does not place third-party work in the public domain.</p><p><a href="https://jrmf.org/puzzle/">JRMF's current resource page</a> permits free personal, educational, and community use and asks that its materials not be used for resale or paid programming. See the notices in each source for other reuse conditions. Gould's workshop explicitly provides its supplementary handouts for personal or classroom use.</p><p>Validation: all local PDF pages rendered successfully; page contact sheets and selected full-size pages were visually reviewed. Life block, blinker, and four-step glider behavior were computed and checked. No physical models were assembled.</p></footer>
<script>const q=document.querySelector('#search'),quick=document.querySelector('#quickonly'),cards=[...document.querySelectorAll('.card')];function filter(){let n=0;for(const c of cards){c.hidden=!c.textContent.toLowerCase().includes(q.value.toLowerCase())||(quick.checked&&c.dataset.quick!=='1');c.style.display=c.hidden?'none':'';if(!c.hidden)n++;}for(const s of document.querySelectorAll('.resource-section')){s.hidden=![...s.querySelectorAll('.card')].some(c=>!c.hidden);}document.querySelector('#matches').textContent=n+' source PDFs shown'+(n===0?'. Try clearing the filters.':'');}q.addEventListener('input',filter);quick.addEventListener('change',filter);document.querySelector('#clear').addEventListener('click',()=>{q.value='';quick.checked=false;filter();});filter();</script>
</main></body></html>'''
quick_doc=(ROOT/'_sources/quick-catalog-section.html').read_text()
doc=doc.replace('<section class="box" id="starter">',quick_doc+'<section class="box" id="starter">')
doc=doc.replace('<footer><h3>Sources and reuse</h3>','<footer><h3>Sources and reuse</h3><p>Maths Craft NZ handouts are saved unchanged for local home/classroom use. Their resource page specifies CC BY-NC-ND 4.0 and asks that the materials not be packaged or redistributed, or their branding used for another event. Share the source links with others; these files are not included in a redistributed bundle.</p>')
(ROOT/'00-START-HERE.html').write_text(doc)
(ROOT/'START-HERE.txt').write_text(f'''SCIENCE FRIDAY - PRINTABLE COLLECTION
Updated 2026-10-01. {pdf_count} local PDFs, {total} pages including teacher material.
Audience: ages 5-14, about 50 visitors across the event, 10-20 minute visits.

NEW: 00-Quick-Stations-Ages-5-14.pdf
Page 1: staffing, supplies, and first print batch.
Pages 2-5: four station signs, each with three levels.
Pages 6-8: mirror drawing, small Hex boards, and fractal coloring.
Page 9: leader notes and answers.

Open 00-START-HERE.html in a browser for the illustrated catalog, print ranges,
suggested ages, supplies, source links, and a six-session plan.

QUICKEST START
Print 00-Science-Friday-Starter-Pack.pdf pages 1 and 5 for coloring and games.
Print 02-Polyhedra-and-Folding/Mathigon-cube-net.pdf for building.
Supplies: colored pencils, paper, scissors, glue stick or tape.

STARTER PACK PAGE GUIDE
'''+''.join(f'{p:>2}  {name} (ages {age})\n' for p,name,age in pageguide)+'''
All local PDF links work offline. The folder categories hold unchanged source PDFs.
The Game of Life sheets are in the starter pack, pages 7-9; answers on page 10.
The coloring source links that failed to download are listed in the HTML catalog.
_sources contains provenance, previews, and the editable original worksheet builder.
_build contains verification renders and extraction files, not classroom handouts.
''')
(ROOT/'04-Game-of-Life/START-HERE.txt').write_text('Print ../00-Science-Friday-Starter-Pack.pdf pages 7-9.\nLeader answer key: page 10.\nRules: https://conwaylife.com/wiki/Rulestring\nAdvanced free book (web link only): https://conwaylife.com/book/\n')
(ROOT/'_sources/catalog.json').write_text(json.dumps(downloaded,indent=2)+'\n')
original=dict(file=starter,pages=10,sha256=hashlib.sha256((ROOT/starter).read_bytes()).hexdigest(),created='2026-10-01',source='_sources/build_starter_pack.py')
(ROOT/'_sources/original-manifest.json').write_text(json.dumps(original,indent=2)+'\n')
quickfile='00-Quick-Stations-Ages-5-14.pdf'
quickrecord=dict(file=quickfile,pages=9,sha256=hashlib.sha256((ROOT/quickfile).read_bytes()).hexdigest(),created='2026-10-01',source='_sources/build_quick_stations.py')
(ROOT/'_sources/quick-original-manifest.json').write_text(json.dumps(quickrecord,indent=2)+'\n')
print(f'Catalog: {pdf_count} PDFs, {total} pages')
