"""Second curated set: ages 5-14, drop-in visits of 10-20 minutes."""
import json, concurrent.futures
from pathlib import Path
from download_collection import download
ROOT=Path(__file__).resolve().parent.parent
items=[]
def add(folder,name,url,source,ages,minutes,supplies,note,print_pages,preview=1,kind='Quick station'):
    items.append(dict(file=f'{folder}/{name}.pdf',url=url,source=source,ages=ages,minutes=minutes,supplies=supplies,note=note,print_pages=print_pages,preview_page=preview,session=kind))
add('01-Coloring-and-Symmetry','Hampton-A-Mathematical-Coloring-Book',
    'https://www.d.umn.edu/~mhampton/mathcolor17b.pdf','https://www.d.umn.edu/~mhampton/mathcolor17b.pdf',
    '5-14; choose detail level','10-20','colored pencils',
    '34 mathematical drawings, from tilings and spirals to fractals and higher-dimensional shapes. Children can color without understanding the advanced notes.',
    'Choose individual art pages 2-35. Start with 2, 3, 10, or 24. Leader notes: 36-38.',10)
add('03-Paper-Games','Sangwin-Hex-Boards-and-Rules',
    'https://webhomes.maths.ed.ac.uk/~csangwin/hex/HexCrossBoard.pdf','https://webhomes.maths.ed.ac.uk/~csangwin/hex/index.html',
    '8-14','10-20','two colors of counters or pencils',
    'Connection game. Use the new quick-station pack for a smaller 5-by-5 beginner board. Full-size games can run longer.',
    '1-2: full Hex board and rules. Later pages are variants and strategy.',1,'Challenge / longer game')
add('06-More-Math-Recreations','JRMF-Frogs-and-Toads',
    'https://jrmf.org/wp-content/uploads/Frogs-and-Toads-Activity-Guide.pdf','https://jrmf.org/puzzle/frogs-and-toads/',
    '6-14 with support','10-20','two colors of counters; 6 per board',
    'Swap two groups across a row of spaces. Start with two animals of each kind; add more for a challenge. Cooperative puzzle.',
    'See inspected page ranges in the catalog.',7)
nz='https://www.mathscraftnz.org/resources'
for folder,name,remote,ages,minutes,supplies,note,pages,kind in [
 ('02-Polyhedra-and-Folding','Mobius-Strip','Handout-Mobius_Strip.pdf','5-14 with help','10-20','precut paper strips, tape, marker; scissors for extension','Make and trace one twisted loop. Ages 5-7: trace with a finger. Older children: predict and test a center cut.','1 for making and tracing; 2 for cutting investigations.','Quick station'),
 ('02-Polyhedra-and-Folding','Sonobe-Unit','Handout-Sonobe_Unit.pdf','9-14','10-20','one square of paper per unit','Fold a single module during one visit. Six units are needed for a cube; contribute to a group build or return to finish.','1-2 for the unit.','Quick unit / longer full build'),
 ('02-Polyhedra-and-Folding','Sonobe-Cube','Handout-Sonobe_Cube.pdf','9-14','20-40','six finished Sonobe units','Assembly companion to Sonobe Unit. Use pre-folded units for a short demonstration; allow longer when folding from scratch.','1-2; use with the separate unit guide.','Longer / take-home'),
 ('02-Polyhedra-and-Folding','Square-Flexagon-Template','tetraflexagon_template.pdf','7-14 with help','10-20','scissors, glue or tape','Square flexagon cutout. Pair with the square flexagon instructions; adult help with cutting is useful.','Whole template, single-sided.','Quick station with preparation'),
 ('02-Polyhedra-and-Folding','Square-Flexagon-Instructions','Tetratetraflexagon_instructions.pdf','7-14 with help','10-20','matching template, scissors, glue or tape','Instructions for the square flexagon. The leader should practice a model first.','Whole guide once per table.','Leader / companion'),
 ('01-Coloring-and-Symmetry','Four-Color-Map','Handout-Colouring-Four_Colour_Theorem-wphd.pdf','5-14','10-20','four colors of pencils','Younger children color freely; older children try different colors across shared borders.','1, black and white.','Quick station'),
 ('01-Coloring-and-Symmetry','Pursuit-Curves-Coloring','Handout-Colouring-Pursuit_Curves.pdf','5-14','10-20','colored pencils','Curving patterns made from nested straight-edged shapes; an easy entry into mathematical art.','1, black and white.','Quick station')]:
    add(folder,'Maths-Craft-NZ-'+name,'https://www.mathscraftnz.org/s/'+remote,nz,ages,minutes,supplies,note,pages,1,kind)
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(download,items))
    (ROOT/'_sources/expansion-manifest.json').write_text(json.dumps(results,indent=2)+'\n')
    for r in results:print(r['status'],r['file'],r.get('error',''))
