"""Original Science Friday worksheets. Requires reportlab; US Letter, vector art."""
from pathlib import Path
from math import sin, cos, pi, sqrt, comb
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'00-Science-Friday-Starter-Pack.pdf'
c=canvas.Canvas(str(OUT),pagesize=(612,792))
c.setTitle('Science Friday - Coloring, Paper Games, and Conway Life')
c.setAuthor('Original worksheets prepared with Codex for Science Friday')

def text(x,y,s,size=11,bold=False):
    c.setFillColor(colors.black);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def lines(y,ss,size=11):
    for s in ss:text(42,y,s,size);y-=16
    return y
def page(title,tag,num):
    c.setStrokeColor(colors.black);c.setLineWidth(.7)
    text(42,752,'SCIENCE FRIDAY  /  '+tag.upper(),9,True)
    text(42,720,title,24,True)
    c.line(42,707,570,707)
    text(42,28,'Original worksheet | Print single-sided on US Letter | 2026-10-01',8)
    text(548,28,str(num),9)
def end():c.showPage()
def poly(pts):
    p=c.beginPath();p.moveTo(*pts[0])
    for q in pts[1:]:p.lineTo(*q)
    p.close();c.drawPath(p)
def grid(x,y,n=9,s=16,live=None,label=''):
    # x,y is bottom left; live coordinates count from upper left.
    if label:text(x,y+n*s+12,label,10,True)
    c.setFillColor(colors.HexColor('#414141'))
    for r,col in live or []:c.rect(x+col*s,y+(n-1-r)*s,s,s,stroke=0,fill=1)
    c.setStrokeColor(colors.HexColor('#666666'));c.setLineWidth(.55)
    for i in range(n+1):
        c.line(x+i*s,y,x+i*s,y+n*s);c.line(x,y+i*s,x+n*s,y+i*s)
    c.setStrokeColor(colors.black)
def step(live):
    counts=Counter((r+dr,q+dq) for r,q in live for dr in [-1,0,1] for dq in [-1,0,1] if dr or dq)
    return {p for p,n in counts.items() if n==3 or (n==2 and p in live)}
block={(3,3),(3,4),(4,3),(4,4)}
blink={(4,3),(4,4),(4,5)}
glider={(2,3),(3,4),(4,2),(4,3),(4,4)}
assert step(block)==block and step(step(blink))==blink
states=[glider]
for _ in range(4):states.append(step(states[-1]))
assert states[4]=={(r+1,q+1) for r,q in glider}

page('Color a turning rosette','Ages 6+ | 10-20 minutes',1)
lines(685,['Choose a color pattern for one slice. Repeat it all the way around.',
           'Can you color the design so it looks the same after a quarter-turn?',
           'Try another copy with a different turning symmetry.'])
cx,cy=306,376
for rad in [44,83,124,165,208]:c.circle(cx,cy,rad)
for j in range(12):
    a=j*pi/6;c.line(cx,cy,cx+208*cos(a),cy+208*sin(a))
for j in range(12):
    a=(j+.5)*pi/6
    pts=[(cx+r*cos(a+d),cy+r*sin(a+d)) for r,d in [(83,0),(124,-pi/12),(165,0),(124,pi/12)]]
    poly(pts)
lines(115,['My design matches after a turn of __________ degrees.',
           'Can you find a mirror line? Draw it lightly with a ruler.'])
end()

page('Make a square kaleidoscope','Ages 7+ | 15-25 minutes',2)
lines(685,['Color one triangular sector. Reflect its colors across each dashed mirror.',
           'Keep going until the whole square is colored. A tracing sheet can help.',
           'Challenge: make a second coloring that keeps quarter-turns but loses mirrors.'])
x,y,s=72,168,468
c.setLineWidth(.6)
for i in range(13):
    c.line(x+i*39,y,x+i*39,y+s);c.line(x,y+i*39,x+s,y+i*39)
c.setLineWidth(1.6);c.setDash(5,4)
for a,b in [((x,y),(x+s,y+s)),((x+s,y),(x,y+s)),((x+s/2,y),(x+s/2,y+s)),((x,y+s/2),(x+s,y+s/2))]:c.line(*a,*b)
c.setDash();c.setLineWidth(.7)
lines(124,['Every reflection should match colors as well as shapes.',
           'What is the smallest colored piece that tells you the whole design?'])
end()

page('Triangles that tile the page','Ages 6+ | 15-25 minutes',3)
lines(685,['Color a repeating pattern. Try stripes, stars, or large triangles.',
           'Challenge: use only two colors, with different colors across every shared edge.',
           'Where can you slide your pattern so it matches itself?'])
s=42;h=s*sqrt(3)/2;x0=54;y0=160
c.saveState();p=c.beginPath();p.rect(x0,y0,504,12*h);c.clipPath(p,stroke=0)
for r in range(12):
    for k in range(-7,14):
        x=x0+k*s+r*s/2;y=y0+r*h
        poly([(x,y),(x+s,y),(x+s/2,y+h)])
        poly([(x+s,y),(x+1.5*s,y+h),(x+s/2,y+h)])
c.restoreState()
c.rect(x0,y0,504,12*h)
lines(116,['Find a mirror line in the uncolored tiling. Does your coloring keep it?',
           'A finite page ends, but imagine your pattern continuing forever.'])
end()

page('Pascal triangle: color the odd ones','Ages 8+ | 20-30 minutes',4)
lines(685,['Start each row and end each row with 1. Each other box is the sum of',
           'the two boxes just above it. Fill the empty boxes; then color odd numbers.',
           'Leave even numbers white. What shapes appear?'])
s=31
for r in range(16):
    yy=611-r*31
    for j in range(r+1):
        xx=306+(j-r/2)*s-s/2;c.rect(xx,yy,s,29)
        if r<4:
            c.setFont('Helvetica',10);c.drawCentredString(xx+s/2,yy+10,str(comb(r,j)))
lines(98,['Shortcut: odd + odd is even; even + even is even; odd + even is odd.',
          'Use O and E instead of large numbers if you prefer.'])
end()

page('Dots and Boxes','Ages 6+ | Two players | 10-20 minutes',5)
lines(685,['Take turns joining neighboring dots with one horizontal or vertical line.',
           'Complete a small square? Write your initial inside it and take another turn.',
           'When every box is claimed, the player with the most boxes wins. Ties are possible.'])
for index,(xx,yy) in enumerate([(70,388),(336,388),(70,115),(336,115)]):
    text(xx,yy+204,'GAME '+str(index+1),10,True)
    for r in range(5):
        for q in range(5):c.circle(xx+q*45,yy+r*45,2,fill=1)
    text(xx,yy-26,'Scores: ______  /  ______',10)
end()

page('Sprouts: draw the last curve','Ages 10+ | Two players | 15-25 minutes',6)
lines(685,['Start with the dots in a play area. Take turns drawing one curve between two',
           'dots, or from a dot back to itself. Add one NEW dot along your new curve.',
           'Curves cannot cross or touch other curves or dots except at their endpoints.',
           'At most three curve ends may meet any dot. A loop uses two ends at its dot.',
           'If you cannot make a legal move, you lose. Try two dots before three.'])
for k,(yy,num) in enumerate([(365,2),(105,3)]):
    c.roundRect(42,yy,528,222,8);text(57,yy+202,'GAME '+str(k+1)+'  /  '+str(num)+' starting dots',10,True)
    for i in range(num):c.circle(210+i*(180/(num-1)),yy+110+(25 if i==1 and num==3 else 0),3,fill=1)
text(42,64,'Explore: Does the first player always win? Try changing your opening move.',10)
end()

page("Conway's Game of Life",'Ages 9+ | 20-30 minutes',7)
lines(685,['Shade living cells; leave dead cells white. Each cell has EIGHT neighbors:',
           'above, below, left, right, and the four diagonals. Do not count the cell itself.',
           'A living cell survives with 2 or 3 living neighbors; otherwise it dies.',
           'A dead cell becomes living with exactly 3 living neighbors.',
           'All changes happen together. Count on the OLD grid; draw on the NEW grid.',
           'The world continues beyond each grid. Start with all unshown cells dead.'])
for yy,name,seed in [(348,'A. Block',block),(125,'B. Blinker',blink)]:
    text(42,yy+183,name,13,True)
    for j,x in enumerate([42,222,402]):grid(x,yy,live=seed if j==0 else None,label=['Start','Generation 1','Generation 2'][j])
text(42,78,'Which pattern stays still? Which changes and then comes back?',11)
end()

page('Follow a glider','Ages 9+ | 20-30 minutes',8)
lines(685,['Use the rules on page 7. Copy each new generation into the next grid.',
           'Count all eight neighbors using only the previous generation.',
           'After four steps, compare the shape AND its position with the start.'])
for j in range(6):
    grid([42,222,402][j%3],[419,183][j//3],live=glider if j==0 else None,
         label='Start' if j==0 else ('Generation '+str(j) if j<5 else 'Extra: generation 5'))
text(42,122,'What changed? _____________________________________________________',11)
text(42,90,'Prediction: Where will the glider be after eight steps?',11)
end()

page('Invent a Life experiment','Ages 9+ | 15-30 minutes',9)
lines(685,['Start with 3 to 6 living cells near the center of the first grid.',
           'Predict what will happen. Then compute three generations to test your guess.',
           'If the pattern reaches an edge, use more graph paper; do not wrap it around.'])
for j in range(4):grid([61,331][j%2],[394,128][j//2],n=10,s=21,label='My start' if j==0 else 'Generation '+str(j))
text(42,80,'My prediction was ___________________________________________________',11)
text(42,57,'What I noticed _______________________________________________________',11)
end()

page('Leader notes and answer key','Keep this page separate',10)
lines(685,['Coloring: many solutions are possible. Ask children to explain a rule they chose.',
           'p. 1: repeating every third slice preserves a quarter-turn (90 degrees).',
           'p. 2: mirror matching gives fourfold turning symmetry. For the challenge,',
           'place the same small asymmetric motif in four quarter-turn positions.',
           'p. 3: color upward triangles one color and downward triangles another.',
           'p. 4: odd entries form a triangular fractal pattern. The first rows of parity are:'])
for k,ss in enumerate(['O','O O','O E O','O O O O','O E E E O','O O E E O O','O E O E O E O','O O O O O O O O']):
    c.setFont('Courier',10);c.drawCentredString(306,574-k*13,ss)
lines(451,['p. 7: the block stays unchanged. The blinker alternates vertical and horizontal.',
           'p. 8: the glider returns to its shape one cell down and one cell right after 4 steps.',
           'After 8 steps it has moved two cells down and two cells right.'])
for j in range(5):grid(42+j*107,285,n=9,s=10,live=states[j],label='Glider '+str(j))
lines(255,['p. 9: outcomes depend on the chosen seed. Check cells that start dead too!',
           'Common Life mistake: updating one grid in place changes the rules.',
           'For Sprouts, a new dot has two ends already, so it has room for only one more.',
           'These activities introduce examples; they are not classifications or proofs.'])
lines(166,['Rules and further reading:',
           'Conway Life: conwaylife.com/wiki/Rulestring',
           'Sprouts: nrich.maths.org/games/sprouts',
           'Dots and Boxes: mathforlove.com (Games to Play at Home, p. 2)',
           'All worksheet text, layouts, and drawings in this pack were newly prepared.',
           'You may print, adapt, and share this original pack for Science Friday.'],10)
end();c.save()
print(OUT)
