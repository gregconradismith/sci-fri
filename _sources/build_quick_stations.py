"""Original short-visit materials for Science Friday. US Letter, vector PDF."""
from pathlib import Path
from math import sqrt,cos,sin,pi
from reportlab.pdfgen import canvas
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'00-Quick-Stations-Ages-5-14.pdf'
c=canvas.Canvas(str(OUT),pagesize=(612,792))
c.setTitle('Science Friday - Quick Stations, Ages 5-14')
c.setAuthor('Original materials prepared with Codex for Science Friday')
def text(x,y,s,size=12,bold=False):
 c.setFillColor(colors.black);c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def lines(y,ss,size=12,gap=18):
 for s in ss:text(44,y,s,size);y-=gap
 return y
def start(title,sub,num):
 c.setLineWidth(.7);c.setStrokeColor(colors.black)
 text(44,751,'SCIENCE FRIDAY  /  '+sub.upper(),9,True)
 text(44,715,title,25,True);c.line(44,701,568,701)
 text(44,28,'Original material | US Letter | Ages 5-14 | 10-20 minute visits',8)
 text(554,28,str(num),9)
def end():c.showPage()
def box(y,label,ss):
 c.setFillColor(colors.HexColor('#f3f3f3'));c.roundRect(34,y-89,544,126,8,stroke=0,fill=1)
 text(48,y+10,label,17,True)
 for k,s in enumerate(ss):text(48,y-17-k*19,s,12)

start('A drop-in plan for 50 children','Leader setup',1)
lines(676,['Plan for 50 visitors across the event, with several arriving at a time.',
 'Four tables with four places each give 16 simultaneous activity places.',
 'Offer a choice; each child can finish one small activity in 10-20 minutes.',
 'The ages below are starting points. Let children change level or activity.'])
text(44,584,'Four tables',17,True)
lines(558,['COLOR: pattern sheets, mirror drawing, and a four-color challenge.',
 'PLAY: small Hex or Dots and Boxes; partner a younger child with a helper.',
 'BUILD: a twisted paper loop, or a precut cube/tetrahedron net.',
 'PUZZLE: trace a doodle, move frogs and toads, or try one Life generation.'])
text(44,467,'A first print batch',17,True)
lines(441,['10 copies of this pack p. 6 + 10 assorted coloring sheets = 20 art starts.',
 '10 cube/tetrahedron nets + 10 sheets cut into 5 long strips = 60 builds.',
 '4 copies of p. 7 + 4 copies of starter p. 5 = reusable game boards.',
 '4 Doodles sheets + 4 Frogs and Toads boards = reusable puzzles.',
 '1 copy of each station sign, pp. 2-5. Keep p. 9 with the leader.',
 'This is a flexible stock, not a prediction of which table children choose.'])
text(44,307,'Supplies and preparation',17,True)
lines(281,['4 sets of colored pencils; 8 ordinary pencils; 4 rulers; 6 pairs of scissors;',
 '4 glue sticks or tape dispensers; 120 counters in two distinct colors;',
 '16 reusable sleeves if available, plus spare paper and erasers.',
 'Precut some nets and strips. Set out one finished example per build.',
 'Have a helper at BUILD and another available to explain games and puzzles.',
 'For ages 5-7, offer large shapes, short instructions, and help with cutting.'])
text(44,135,'Simple rhythm',17,True)
lines(110,['1-2 min: show a start. 7-15 min: explore. 1-3 min: share and reset.',
 'Ask: "What did you notice?" Record a discovery; avoid giving the trick away.',
 'Sonobe cubes, dodecahedra, and full orbifold lessons are longer projects.'],11)
end()

stations=[
 ('COLOR / draw a pattern','Station 1',[
 ('START HERE  /  ages 5-7',['Pick a large-shape coloring page or the mirror drawing on p. 6.', 'Choose colors and tell a helper where your pattern repeats.']),
 ('TRY THIS  /  ages 8-10',['Use the same colors in matching mirror positions.', 'Or color a map so regions sharing a border have different colors.']),
 ('GO FURTHER  /  ages 11-14',['Keep a turning symmetry while breaking a mirror symmetry.', 'Can you explain exactly which turns still match your coloring?'])],
 ['YOU NEED: colored pencils; ruler or child-safe mirror optional.',
  'LEADER: use this pack pp. 6 or 8, starter pp. 1-3, or a coloring sheet.',
  'RESET: put pencils back; take your art home.']),
 ('PLAY / find a strategy','Station 2',[
 ('START HERE  /  ages 5-7',['Play Dots and Boxes with a partner or helper.', 'When you complete a box, write your initial and play again.']),
 ('TRY THIS  /  ages 8-10',['Play small Hex on p. 7. Connect your two sides of the board.', 'After a game, swap who starts and try another opening.']),
 ('GO FURTHER  /  ages 11-14',['Predict your partner\'s best reply before making your move.', 'Try Chomp or Sprouts. Explain one position where you can force a win.'])],
 ['YOU NEED: two pencils, or counters in two colors and a board.',
  'LEADER: use starter p. 5 or this pack p. 7. Read the rules first.',
  'RESET: clear reusable boards or take a fresh sheet.']),
 ('BUILD / a surprising surface','Station 3',[
 ('START HERE  /  ages 5-7',['Make a loop from a paper strip and tape. Try another with a half-twist.', 'Trace around each loop with your finger. What feels different?']),
 ('TRY THIS  /  ages 8-10',['Draw a line along the middle of the twisted loop until it joins itself.', 'Predict what a cut along that line will make. Ask a helper, then test.']),
 ('GO FURTHER  /  ages 11-14',['Try a fresh loop with a full twist, or start a cut one-third across.', 'Compare the number of loops, their sides, and how they link.'])],
 ['YOU NEED: precut long paper strips, tape, marker, scissors.',
  'LEADER: use the Maths Craft NZ Mobius Strip handout. Practice first.',
  'ALTERNATIVE: color and fold a precut cube or tetrahedron net.']),
 ('PUZZLE / test an idea','Station 4',[
 ('START HERE  /  ages 5-7',['Trace a simple doodle without going over a line twice.', 'Or move two frogs and two toads past each other with a helper.']),
 ('TRY THIS  /  ages 8-10',['Try a harder doodle or add another frog and toad.', 'Pause before each move. If stuck, reset and change one choice.']),
 ('GO FURTHER  /  ages 11-14',['Try a Life blinker or glider: count on the old grid, draw on the new.', 'Explain why the pattern changes, repeats, or moves.'])],
 ['YOU NEED: pencil; puzzle sheet; six counters in two colors.',
  'LEADER: JRMF Doodles / Frogs and Toads; starter pp. 7-8 for Life.',
  'RESET: clear counters and leave the puzzle ready for the next visitor.'])]
for number,(title,sub,levels,foot) in enumerate(stations,2):
 start(title,sub+' | 10-20 minutes',number)
 text(44,673,'Choose a starting point. You can change levels whenever you like.',12)
 for yy,(label,ss) in zip([603,447,291],levels):box(yy,label,ss)
 lines(122,foot,10,19);end()

start('Finish the mirror picture','Color / ages 5+',6)
lines(676,['Copy the left side onto the right. Count grid squares to help.',
 'Then color matching parts alike. The dashed line is your mirror.',
 'On the blank grid, invent a picture with a partner: each draws one half.'])
def mirror_grid(y,draw=False):
 x=66;s=30;n=16;m=7
 c.setStrokeColor(colors.HexColor('#bbbbbb'));c.setLineWidth(.5)
 for i in range(n+1):c.line(x+i*s,y,x+i*s,y+m*s)
 for i in range(m+1):c.line(x,y+i*s,x+n*s,y+i*s)
 c.setStrokeColor(colors.black);c.setLineWidth(1.4);c.setDash(5,4)
 c.line(x+8*s,y,x+8*s,y+m*s);c.setDash()
 if draw:
  # Left half of a symmetric stepped badge, only integer-grid segments.
  pts=[(8,6),(6,6),(6,5),(4,5),(4,4),(2,4),(2,2),(4,2),(4,1),(8,1)]
  c.setLineWidth(2);p=c.beginPath();p.moveTo(x+pts[0][0]*s,y+pts[0][1]*s)
  for a,b in pts[1:]:p.lineTo(x+a*s,y+b*s)
  c.drawPath(p)
mirror_grid(368,True);mirror_grid(90)
text(66,590,'Finish this one.',11,True);text(66,315,'Make your own.',11,True)
end()

start('Small Hex: connect your sides','Play / two players / ages 8+',7)
lines(676,['Player A connects the two solid borders. Player B connects the dashed borders.',
 'Take turns marking ONE empty hexagon with A or B. Marks stay where placed.',
 'Win by making an unbroken chain of your cells between your two borders.',
 'Your cells connect across shared edges. Corner cells touch both adjacent borders.',
 'For your first games, take turns starting. Use a fresh board or reusable counters.'],11,16)
def hexboard(y,label):
 n=5;s=21;x0=185
 text(44,y+163,label,12,True)
 verts=[(s*cos(pi/6+k*pi/3),s*sin(pi/6+k*pi/3)) for k in range(6)]
 directions=[(0,1),(-1,1),(-1,0),(0,-1),(1,-1),(1,0)]
 edges=0
 for r in range(n):
  for q in range(n):
   cx=x0+sqrt(3)*s*(q+r/2);cy=y+1.5*s*r
   for k,(dq,dr) in enumerate(directions):
    a,b=verts[k],verts[(k+1)%6]
    outside=not(0<=q+dq<n and 0<=r+dr<n)
    c.setLineWidth(2.5 if outside else .55)
    c.setDash(4,3) if outside and 0<=q+dq<n else c.setDash()
    c.line(cx+a[0],cy+a[1],cx+b[0],cy+b[1]);edges+=outside
 assert edges==4*(2*n-1)+2 # perimeter edges of rhombus of hex cells
 c.setDash();c.setLineWidth(.7)
 text(x0-55,y+47,'A',17,True);text(x0+sqrt(3)*s*6+29,y+78,'A',17,True)
 text(x0+66,y-42,'B',17,True);text(x0+146,y+169,'B',17,True)
hexboard(396,'GAME 1');hexboard(132,'GAME 2')
text(44,66,'Explore: can you connect your sides while blocking your partner?',11)
end()

start('Triangles inside triangles','Color / ages 5+',8)
lines(676,['Color the biggest upside-down triangle. Use a new color for the next size.',
 'Keep going. Can you find all the triangles of each size?',
 'For a challenge, predict how many holes the next level would add.'])
def triangle(points):
 p=c.beginPath();p.moveTo(*points[0])
 for pt in points[1:]:p.lineTo(*pt)
 p.close();c.drawPath(p)
def sierp(a,b,d,depth):
 if depth==0:return
 ab=tuple((a[i]+b[i])/2 for i in (0,1));bd=tuple((b[i]+d[i])/2 for i in (0,1));da=tuple((d[i]+a[i])/2 for i in (0,1))
 triangle([ab,bd,da])
 sierp(a,ab,da,depth-1);sierp(ab,b,bd,depth-1);sierp(da,bd,d,depth-1)
a=(54,182);b=(558,182);d=(306,182+252*sqrt(3))
c.setLineWidth(.8);triangle([a,b,d]);sierp(a,b,d,4)
lines(132,['Count from large holes to small holes:   1,   _____,   _____,   _____',
           'I predict the next level would add __________ smaller holes.',
           'This is a finite drawing inspired by the Sierpinski triangle.'],11)
end()

start('Leader notes and short-session tips','Keep with the leader',9)
lines(676,['PAGE 6 / MIRRORS',
 'Reflect each grid point across the middle vertical line; keep its height.',
 'Accept any symmetric coloring. An easy check is to fold or use tracing paper.',
 '',
 'PAGE 7 / HEX',
 'Each corner cell is available to both players and touches two different borders.',
 'A and B are player labels, not pre-filled cells. Use pencil initials or two colors.',
 'A filled finite Hex board always has a winning connection; there is no draw.',
 'The small board is for learning. The Sangwin resource adds larger boards.',
 '',
 'PAGE 8 / TRIANGLES',
 'There are 1, 3, 9, and 27 upside-down holes, from largest to smallest.',
 'The next level adds 81 smaller holes. Ask children to explain the factor of 3.',
 '',
 'BUILD / TWISTED LOOPS',
 'An untwisted loop has two sides and two boundary components.',
 'A loop with one half-twist is a Mobius strip: one side, one boundary component.',
 'Cutting its center produces one longer loop with two sides.',
 'Cutting one-third across a fresh Mobius strip produces two linked loops:',
 'one Mobius strip and one two-sided loop. A drawing alone is not a test.',
 'Let children predict before cutting. Use the downloaded guide for directions.',
 '',
 'PLANNING',
 'For a crowded table, offer a simpler start and a clear stopping point.',
 'An unfinished coloring page or a model to finish at home is still a useful visit.',
 'Try one physical model before the event; these files were checked digitally.',
 '',
 'SOURCES',
 'Hex rules: webhomes.maths.ed.ac.uk/~csangwin/hex/index.html',
 'Mobius activities: mathscraftnz.org/resources',
 'Puzzles and teacher guides: jrmf.org/puzzle/',
 'Text, drawings, and station cards in this PDF were newly prepared.',
 'You may print, adapt, and share this original pack. Source PDFs keep their licences.'],11,17)
end();c.save();print(OUT)
