"""Render the original profile banner: python assets/render_banner.py (Pillow)."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 240
BG = '#0c1526'
TEAL, PURPLE, MUTED = '#65dfd1', '#b9a4ff', '#8494b0'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
small = ImageFont.truetype(FONT, 13)
label = ImageFont.truetype(FONT, 15)
frames = []
for frame in range(80):
    t = frame / 80
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    for x in range(24, W, 24):
        for y in range(24, H, 24):
            d.ellipse((x, y, x+1, y+1), fill='#1b2a43')
    d.text((35, 24), 'DATA / MODELS / SYSTEMS', font=small, fill=MUTED)
    d.text((35, 204), 'From a signal to something useful.', font=small, fill=MUTED)
    # Three input curves converge on a single processing lane.
    def curve(u, start):
        return 38+u*270, start+(120-start)*(u*u*(3-2*u))
    for lane,start in enumerate((72,120,168)):
        pts=[curve(i/80,start) for i in range(81)]
        d.line(pts, fill='#28465b', width=2)
        for j in range(3):
            u=(t+j/3+lane/9)%1
            x,y=curve(u,start)
            d.ellipse((x-3,y-3,x+3,y+3),fill=TEAL)
    for x1,x2 in ((308,366),(468,527),(629,703)):
        d.line((x1,120,x2,120),fill='#3c526c',width=2)
        u=(t*2)%1;x=x1+(x2-x1)*u
        d.ellipse((x-3,117,x+3,123),fill=TEAL)
    for idx,(x,title) in enumerate(((366,'prepare'),(527,'reason'))):
        d.rounded_rectangle((x,87,x+102,153),radius=13,fill='#14263a',outline='#397d80',width=2)
        for j in range(3):
            yy=103+j*14
            length=28+int(16*(1+math.sin(2*math.pi*(t+idx/3+j/5)))/2)
            d.line((x+29,yy,x+29+length,yy),fill=TEAL,width=3)
        d.text((x+51,169),title,font=label,fill='#dde7f3',anchor='mm')
    d.rounded_rectangle((703,66,923,175),radius=16,fill='#1b2340',outline=PURPLE,width=2)
    d.text((721,82),'RESULT',font=small,fill=PURPLE)
    # Periodic bar motion suggests a progressively formed result with no hard cut.
    for j in range(7):
        h=14+int(39*(0.5+0.5*math.sin(2*math.pi*(t-j/14))))
        x=724+j*26
        d.rounded_rectangle((x,153-h,x+14,153),radius=3,fill=PURPLE if j>3 else TEAL)
    frames.append(im.quantize(colors=32))
out=Path(__file__).with_name('data-to-product.gif')
frames[0].save(out,save_all=True,append_images=frames[1:],duration=75,loop=0,optimize=True,disposal=1)
print(f'{out.name}: {out.stat().st_size:,} bytes; 80 frames; 6 seconds; infinite loop')
