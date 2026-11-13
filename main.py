"""Generate an original, deterministic pastel illustration for the Make.fun contest.

Run with Python 3 and Pillow installed. The sole deliverable is /output/entry.png.
No network access, external assets, random values, or local fonts are used.
"""

from pathlib import Path
from math import cos, pi, sin
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1024
SCALE = 3
CANVAS = SIZE * SCALE
OUT = Path("/output/entry.png")


def xy(point):
    return tuple(round(v * SCALE) for v in point)


def box(coords):
    return tuple(round(v * SCALE) for v in coords)


def line(draw, points, fill, width=3):
    draw.line([xy(p) for p in points], fill=fill, width=round(width * SCALE), joint="curve")


def ellipse(draw, coords, fill, outline=None, width=1):
    draw.ellipse(box(coords), fill=fill, outline=outline, width=round(width * SCALE))


def polygon(draw, points, fill, outline=None, width=1):
    pts = [xy(p) for p in points]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=round(width * SCALE), joint="curve")


def bezier(p0, p1, p2, p3, steps=36):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        pts.append((u**3*p0[0] + 3*u**2*t*p1[0] + 3*u*t**2*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u**2*t*p1[1] + 3*u*t**2*p2[1] + t**3*p3[1]))
    return pts


def path_shape(draw, segments, fill, outline=None, width=4):
    pts = []
    for segment in segments:
        curve = bezier(*segment)
        pts.extend(curve if not pts else curve[1:])
    if pts[-1] != pts[0]:
        pts.append(pts[0])
    draw.polygon([xy(p) for p in pts], fill=fill)
    if outline:
        draw.line([xy(p) for p in pts], fill=outline, width=round(width*SCALE), joint="curve")


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -pi/2 + i*pi/5
        radius = r if i % 2 == 0 else r*0.38
        pts.append((cx + cos(a)*radius, cy + sin(a)*radius))
    polygon(draw, pts, fill)


def make_art():
    # A soft dawn-to-mint gradient, made locally with no external assets.
    img = Image.new("RGB", (CANVAS, CANVAS))
    pix = img.load()
    top, bottom = (255, 226, 239), (210, 241, 226)
    for y in range(CANVAS):
        t = y/(CANVAS-1)
        row = tuple(round(top[i]*(1-t) + bottom[i]*t) for i in range(3))
        for x in range(CANVAS):
            pix[x, y] = row
    d = ImageDraw.Draw(img)

    # Warm halo and rolling meadow.
    ellipse(d, (166, 82, 858, 774), (255, 242, 218))
    ellipse(d, (191, 104, 833, 746), (255, 247, 231))
    path_shape(d, [((0,682),(145,588),(270,655),(394,685)),
                   ((394,685),(535,720),(692,605),(1024,655)),
                   ((1024,655),(1024,820),(1024,940),(1024,1024)),
                   ((1024,1024),(700,1024),(320,1024),(0,1024)),
                   ((0,1024),(0,880),(0,752),(0,682))], (183,224,190))
    path_shape(d, [((0,776),(180,710),(300,794),(440,776)),
                   ((440,776),(650,738),(804,792),(1024,734)),
                   ((1024,734),(1024,880),(1024,960),(1024,1024)),
                   ((1024,1024),(690,1024),(325,1024),(0,1024)),
                   ((0,1024),(0,920),(0,830),(0,776))], (161,211,173))

    # Puffy clouds.
    cloud, cloudline = (255,255,250), (239,190,198)
    for cx, cy, s in [(212,276,0.78),(809,310,0.72)]:
        ellipse(d,(cx-72*s,cy-5*s,cx+73*s,cy+47*s),cloud,cloudline,2)
        ellipse(d,(cx-48*s,cy-32*s,cx+12*s,cy+38*s),cloud,cloudline,2)
        ellipse(d,(cx-4*s,cy-48*s,cx+57*s,cy+39*s),cloud,cloudline,2)
        ellipse(d,(cx-47*s,cy+2*s,cx+55*s,cy+42*s),cloud)

    # Sparkles, tiny hearts and dots.
    star(d,299,184,15,(244,183,92)); star(d,731,199,12,(244,183,92))
    star(d,167,459,10,(255,255,246)); star(d,866,485,13,(255,255,246))
    ellipse(d,(254,354,263,363),(244,183,92)); ellipse(d,(782,408,791,417),(244,183,92))
    path_shape(d,[((174,350),(150,323),(180,308),(194,332)),
                  ((194,332),(212,308),(239,327),(214,352)),
                  ((214,352),(202,365),(190,373),(194,382)),
                  ((194,382),(186,372),(174,361),(174,350))],(247,156,174))
    path_shape(d,[((835,388),(818,369),(839,355),(850,374)),
                  ((850,374),(865,355),(886,370),(869,392)),
                  ((869,392),(861,400),(851,407),(853,414)),
                  ((853,414),(846,407),(835,399),(835,388))],(247,156,174))

    # Soft shadow under the cup.
    shadow = Image.new("RGBA", (CANVAS,CANVAS), (0,0,0,0))
    ImageDraw.Draw(shadow).ellipse(box((274,820,754,906)), fill=(91,111,95,54))
    img = Image.alpha_composite(img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(24*SCALE))).convert("RGB")
    d = ImageDraw.Draw(img)
    outline, cream = (145,101,99), (255,250,239)
    pink, pink_light = (247,157,178), (255,193,203)

    # Teacup handle behind the bunny.
    ellipse(d,(690,612,830,769),(255,231,220),outline,8)
    ellipse(d,(726,648,792,733),(205,237,204),outline,5)

    # Bunny's long ears and pink inner fur.
    path_shape(d,[((386,390),(342,318),(338,183),(378,151)),
                  ((378,151),(415,119),(465,183),(460,280)),
                  ((460,280),(459,323),(451,366),(440,404)),
                  ((440,404),(423,417),(402,407),(386,390))],cream,outline,7)
    path_shape(d,[((390,330),(368,275),(367,203),(383,187)),
                  ((383,187),(406,168),(431,213),(430,276)),
                  ((430,276),(429,316),(420,349),(413,365)),
                  ((413,365),(403,363),(397,350),(390,330))],(250,190,194))
    path_shape(d,[((578,397),(578,325),(592,197),(633,166)),
                  ((633,166),(677,132),(706,196),(690,288)),
                  ((690,288),(681,340),(661,383),(640,409)),
                  ((640,409),(618,419),(594,410),(578,397))],cream,outline,7)
    path_shape(d,[((607,343),(607,285),(617,214),(638,196)),
                  ((638,196),(660,180),(674,233),(663,290)),
                  ((663,290),(655,326),(642,354),(630,367)),
                  ((630,367),(619,365),(612,355),(607,343))],(250,190,194))

    # Saucer, tapered cup and glossy rim.
    ellipse(d,(265,812,759,890),(255,244,226),outline,7)
    ellipse(d,(340,827,686,875),(234,245,220),(210,191,164),3)
    path_shape(d,[((291,625),(420,636),(610,636),(739,625)),
                  ((739,625),(725,747),(709,822),(668,842)),
                  ((668,842),(579,878),(424,878),(343,842)),
                  ((343,842),(306,820),(298,727),(291,625))],pink,outline,8)
    path_shape(d,[((324,675),(334,714),(341,780),(357,817)),
                  ((357,817),(365,830),(378,829),(381,817)),
                  ((381,817),(365,776),(358,711),(354,674)),
                  ((354,674),(343,672),(333,673),(324,675))],pink_light)
    ellipse(d,(282,606,748,668),(255,218,216),outline,7)
    ellipse(d,(307,614,722,659),(255,240,220),(222,154,158),3)
    ellipse(d,(344,620,690,652),(241,192,139))
    for x,y,r in [(392,632,5),(654,637,4),(611,627,3)]:
        ellipse(d,(x-r,y-r,x+r,y+r),(255,233,198))

    # Bunny peeking out of the teacup.
    ellipse(d,(361,490,665,740),cream,outline,7)
    ellipse(d,(380,690,500,780),(255,246,231),outline,6)
    ellipse(d,(526,690,646,780),(255,246,231),outline,6)
    for x in (428,574):
        ellipse(d,(x-9,733,x+1,744),(239,174,174)); ellipse(d,(x+8,733,x+18,744),(239,174,174))
    ellipse(d,(333,306,691,653),cream,outline,8)
    path_shape(d,[((349,492),(325,481),(312,460),(320,441)),
                  ((320,441),(327,454),(335,460),(348,461)),
                  ((348,461),(345,472),(346,484),(349,492))],cream,outline,5)
    path_shape(d,[((674,492),(697,481),(710,460),(702,441)),
                  ((702,441),(695,454),(687,460),(674,461)),
                  ((674,461),(677,472),(676,484),(674,492))],cream,outline,5)
    ellipse(d,(396,375,628,594),(255,252,243))
    ellipse(d,(371,481,450,524),(255,205,203)); ellipse(d,(574,481,653,524),(255,205,203))
    line(d,bezier((427,459),(438,436),(464,436),(477,459),18),outline,7)
    line(d,bezier((547,459),(560,436),(584,436),(597,459),18),outline,7)
    line(d,[(423,452),(414,447)],outline,4); line(d,[(601,452),(610,447)],outline,4)
    polygon(d,[(500,480),(524,480),(512,496)],(231,139,150))
    line(d,[(512,495),(512,506)],outline,4)
    line(d,bezier((512,506),(499,523),(486,516),(482,508),14),outline,4)
    line(d,bezier((512,506),(525,523),(538,516),(542,508),14),outline,4)
    for x,y in [(390,466),(405,474),(616,474),(631,466)]:
        ellipse(d,(x-3,y-3,x+3,y+3),(192,137,132))

    # One paw offers a strawberry.
    line(d,bezier((573,570),(597,573),(606,592),(620,608),18),outline,8)
    ellipse(d,(596,575,625,606),cream,outline,4)
    path_shape(d,[((620,576),(606,546),(630,526),(651,546)),
                  ((651,546),(676,526),(699,548),(680,578)),
                  ((680,578),(671,605),(653,628),(649,642)),
                  ((649,642),(637,627),(620,604),(620,576))],(239,105,117),(166,91,89),4)
    polygon(d,[(620,552),(623,538),(635,546),(643,533),(651,545),(664,536),(663,551),(677,547),(670,562),(646,558)],
            (118,174,111),(91,137,94),2)
    for x,y in [(631,567),(650,571),(669,568),(638,590),(658,594),(649,614)]:
        ellipse(d,(x-2.5,y-3,x+2.5,y+3),(255,221,151))

    # Tiny daisy decal on the cup.
    for i in range(8):
        a=i*pi/4; cx,cy=510+cos(a)*34,762+sin(a)*34
        ellipse(d,(cx-13,cy-18,cx+13,cy+18),(255,248,223))
    ellipse(d,(496,748,524,776),(246,190,93))
    line(d,[(511,784),(511,806)],(104,158,104),5)
    line(d,bezier((510,795),(493,787),(488,794),(490,802),12),(104,158,104),4)
    line(d,bezier((512,800),(529,791),(535,798),(532,806),12),(104,158,104),4)

    # Little meadow flowers frame the scene.
    def flower(cx,cy,petal_color,radius=10):
        for i in range(6):
            a=i*pi/3; px,py=cx+cos(a)*radius*1.15,cy+sin(a)*radius*1.15
            ellipse(d,(px-radius*.55,py-radius*.55,px+radius*.55,py+radius*.55),petal_color)
        ellipse(d,(cx-4,cy-4,cx+4,cy+4),(245,191,95))
    flower(182,823,(255,250,226),10); flower(845,844,(255,236,219),11)
    flower(242,906,(255,222,224),8); flower(783,914,(255,250,226),8)
    line(d,[(182,834),(177,864)],(101,157,106),4)
    line(d,[(845,857),(851,888)],(101,157,106),4)
    line(d,[(242,916),(240,937)],(101,157,106),3)
    line(d,[(783,924),(787,944)],(101,157,106),3)

    return img.resize((SIZE,SIZE),Image.Resampling.LANCZOS)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    make_art().save(OUT,format="PNG",optimize=True,compress_level=9)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
