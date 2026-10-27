#!/usr/bin/env python3
"""Draw a source-linked monochrome vector atlas for all 225 recorded methods."""
from collections import defaultdict
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import re
import textwrap
import xml.etree.ElementTree as ET
import zipfile

import pymupdf as fitz
from matplotlib import font_manager

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'methods-with-math.json'
WIDTH,HEIGHT=480,235
INK='#151515'
GRAY='#777777'
LIGHT='#c5c5c5'
PALE='#ededed'
FONT_PATH=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans'))
BOLD_PATH=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight='bold'))
FONT=fitz.Font(fontfile=FONT_PATH)
BOLD=fitz.Font(fontfile=BOLD_PATH)


def esc(value):return html.escape(str(value),quote=True)


class Scene:
    def __init__(self):self.parts=[]
    def line(self,x1,y1,x2,y2,w=1.3,color=INK,dash=None):
        self.parts.append(f'<path d="M{x1:g},{y1:g} L{x2:g},{y2:g}" fill="none" stroke="{color}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def arrow(self,x1,y1,x2,y2,w=1.3,color=INK,dash=None):
        self.line(x1,y1,x2,y2,w,color,dash)
        a=math.atan2(y2-y1,x2-x1)
        for delta in (-.5,.5):self.line(x2,y2,x2-7*math.cos(a+delta),y2-7*math.sin(a+delta),w,color)
    def path(self,data,w=1.3,color=INK,dash=None,fill='none'):
        self.parts.append(f'<path d="{data}" fill="{fill}" stroke="{color}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def circle(self,x,y,r=3,fill=INK,w=1,color=INK):
        self.parts.append(f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}" stroke="{color}" stroke-width="{w}"/>')
    def rect(self,x,y,w,h,fill='none',stroke=INK,lw=1):
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>')
    def text(self,x,y,value,size=12,color=INK,anchor='middle',weight='normal'):
        self.parts.append(f'<text x="{x:g}" y="{y:g}" font-family="DejaVu Sans, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{esc(value)}</text>')
    def words(self,x,y,value,limit=23,size=12,color=INK):
        for i,line in enumerate(textwrap.wrap(value,limit)):self.text(x,y+i*14,line,size,color)
    def dots(self,x,y,cols,rows,spacing=8,color=GRAY,r=1):
        for a in range(cols):
            for b in range(rows):self.circle(x+a*spacing,y+b*spacing,r,color,0,color)
    def chain(self,points,heavy=False):
        for a,b in zip(points,points[1:]):self.line(*a,*b,2.6 if heavy else 1.1)
        for i,p in enumerate(points):self.circle(*p,3.4 if heavy else 2.7,INK if i%3==0 else 'white')
    def label_stages(self,labels):
        self.line(25,180,455,180,.65,LIGHT)
        for x,label in zip((80,240,400),labels):self.words(x,201,label,23,11.8)
    def bitrow(self,x,y,bits,cell=18):
        for i,bit in enumerate(bits):
            self.rect(x+i*cell,y,cell-3,15,INK if bit=='1' else 'white',GRAY,.7)
    def svg(self,method,labels):
        self.label_stages(labels)
        desc=method['how_it_works']+' Source finding: '+method['finding']
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="235" viewBox="0 0 480 235"><title>{esc(method["id"]+" — "+method["method"])}</title><desc>{esc(desc)}</desc><rect width="480" height="235" fill="white"/><g stroke-linecap="round" stroke-linejoin="round">'+''.join(self.parts)+'</g></svg>'


def sketch(method,kind,labels):
    s=Scene();mid=method['id']
    if kind in ('derive','hashchain','stream','parse','formats','fork'):
        if kind=='hashchain':
            for i in range(4):
                x=55+i*120;s.rect(x,70,48,48,PALE,INK,1.5);s.text(x+24,99,'H' if i else 'seed',12)
                if i<3:s.arrow(x+55,94,x+108,94)
        elif kind=='stream':
            for x in (50,90,130):s.rect(x,75,24,38,'white',GRAY,.8)
            s.arrow(166,95,224,95,2);s.path('M240 70 L265 95 L240 120 L215 95 Z',1.8)
            s.arrow(271,95,335,95,2);s.circle(365,95,17,'white',2)
            s.arrow(240,126,240,156,.9,GRAY);s.text(275,160,'release',11,GRAY)
        elif kind=='parse':
            for i in range(16):s.rect(36+i*25,56,22,26,INK if i%5==0 else PALE,GRAY,.6)
            for a,b,y in ((36,130,115),(137,280,136),(287,433,115)):
                s.path(f'M{a} 91 V{y} H{b} V91',1.2);s.circle((a+b)/2,y+7,2.5)
        elif kind in ('formats','fork'):
            s.rect(40,75,58,42,PALE,INK,1.8);s.line(100,96,172,96,1.8)
            for y in (54,137):
                s.arrow(172,96,234,y);s.rect(245,y-16,82,32,'white',INK,1.3);s.arrow(335,y,392,y);s.circle(412,y,13,'white',1.5)
            s.text(286,58,'A',12);s.text(286,141,'B',12)
        else:
            for x in (55,215,375):
                s.rect(x,65,52,58,PALE if x==215 else 'white',INK,1.8)
                s.dots(x+12,79,4,4,8,INK if x==215 else GRAY,1)
            s.arrow(118,94,202,94,2.5);s.arrow(278,94,361,94,2.5)
            s.text(242,145,'deterministic mapping',11,GRAY)
    elif kind in ('scan','sample','partition','shards','endpoints','band','priority','anchor','clip','containment','widen'):
        s.line(35,96,445,96,1.5)
        for x in (35,445):s.line(x,83,x,109,2)
        if kind=='scan':
            for i in range(17):
                x=48+i*24;s.circle(x,96,3,INK if i<9 else 'white',1)
            s.arrow(50,62,250,62,2.2);s.text(310,66,'next',11,GRAY)
        elif kind=='sample':
            for x,y in ((48,92),(73,78),(105,101),(147,90),(174,111),(209,80),(240,96),(281,87),(303,105),(342,91),(383,107),(425,80)):
                s.circle(x,y,3.2,INK)
            s.line(35,131,445,131,.6,LIGHT);s.text(240,153,'positions distributed over the range',11,GRAY)
        elif kind in ('shards','partition'):
            for i in range(8):
                x=35+i*51.25;s.rect(x,63,51.25,64,'white' if i%2 else PALE,GRAY,.8)
                if kind=='shards':s.circle(x+12+(i*17)%29,95,4,INK)
            s.text(240,151,'disjoint integer intervals',12,GRAY)
        elif kind=='endpoints':
            s.circle(35,96,7);s.circle(445,96,7)
            s.line(60,96,420,96,2,LIGHT,'3 8');s.text(240,139,'interior remains unchecked',12,GRAY)
        elif kind=='clip':
            s.rect(65,46,237,35,PALE,GRAY,.8);s.rect(190,109,232,35,'white',GRAY,.8)
            s.rect(190,46,112,98,PALE,'none');s.line(190,46,190,144,2.6);s.line(302,46,302,144,2.6)
            s.text(246,166,'intersection',12)
        elif kind=='containment':
            for a,b in ((55,140),(180,290),(340,425)):
                s.rect(a,70,b-a,50,PALE,GRAY,.8)
            s.circle(232,96,7,INK);s.line(232,39,232,78,1.2);s.text(232,29,'known answer',12)
        elif kind=='anchor':
            s.rect(150,64,180,64,PALE,'none');s.line(150,64,150,128,1.4);s.line(330,64,330,128,1.4)
            s.circle(240,96,7);s.arrow(236,43,236,79);s.text(240,32,'anchor',12)
        elif kind=='widen':
            for a,b,y in ((207,273,52),(151,329,94),(57,423,137)):
                s.line(a,y,b,y,3 if y==52 else 1.3,INK if y==52 else GRAY)
                s.line(a,y-7,a,y+7);s.line(b,y-7,b,y+7)
            s.line(240,62,240,125,.9,GRAY,'3 4')
        else:
            s.rect(175,68,104,56,PALE,'none');s.line(175,96,279,96,4)
            for x in (175,279):s.line(x,62,x,130,1.8)
            if kind=='priority':
                s.arrow(177,40,276,40,2);s.text(225,30,'1',12);s.arrow(295,145,428,145,.9,GRAY);s.arrow(164,145,50,145,.9,GRAY);s.text(240,154,'2',12,GRAY)
            else:s.text(227,151,'selected band',12)
    elif kind in ('permutation','orbit','gray','collatz'):
        cx,cy,r=245,90,65
        count=8 if kind=='gray' else 10
        points=[(cx+r*math.cos(2*math.pi*i/count),cy+r*math.sin(2*math.pi*i/count)) for i in range(count)]
        if kind=='permutation':order=[(i*3)%10 for i in range(10)]
        else:order=list(range(count))
        for a,b in zip(order,order[1:]+order[:1]):s.arrow(*points[a],*points[b],.8,LIGHT if kind=='permutation' else GRAY)
        for i,p in enumerate(points):s.circle(*p,5,INK if i in (0,4) else 'white',1.2)
        if kind=='gray':
            gray_words=('000','001','011','010','110','111','101','100')
            assert all((int(a,2)^int(b,2)).bit_count()==1 for a,b in zip(gray_words,gray_words[1:]+gray_words[:1]))
            for i,word in enumerate(gray_words):
                angle=2*math.pi*i/count
                s.text(cx+(r+22)*math.cos(angle),cy+(r+17)*math.sin(angle)+4,word,10)
        elif kind=='collatz':
            s.path('M180 77 L118 50 L80 70 L108 122 L177 111',1.5);s.text(79,49,'odd',11);s.text(112,147,'even',11)
        else:s.text(cx,cy+5,'modular cycle' if kind=='permutation' else 'state orbit',12)
    elif kind in ('collision','walk','pointwalk','near'):
        if kind=='collision':
            a=[(35,44),(89,59),(130,38),(174,72),(223,91),(275,108),(325,80),(369,112),(438,94)]
            b=[(35,145),(95,130),(141,146),(182,116),(223,91)]
            s.chain(a,True);s.chain(b)
            s.circle(223,91,10,'white',2.2);s.circle(223,91,3)
            s.line(223,72,223,32,1);s.text(223,24,'same state',12)
        elif kind=='near':
            s.circle(234,88,6);s.circle(265,112,4,'white',1.5);s.line(235,89,264,111,1,GRAY,'2 4')
            for r in (35,66):s.circle(234,88,r,'none',.75,LIGHT)
            s.arrow(308,136,268,114);s.text(357,150,'distance',12)
        else:
            pts=[(40,114),(98,75),(161,99),(223,51),(296,87),(361,56),(438,106)]
            s.chain(pts,kind=='pointwalk')
            for i,(x,y) in enumerate(pts[1::2]):s.circle(x,y,8,'white',1.4);s.circle(x,y,2)
            s.text(237,153,'successive point updates' if kind=='pointwalk' else 'selected states are retained',12,GRAY)
    elif kind in ('table','bsgs','bloom'):
        for row in range(5):
            s.rect(187,32+row*24,100,24,PALE if row==2 else 'white',GRAY,.75)
            s.text(212,49+row*24,str(row),11,GRAY);s.line(230,32+row*24,230,56+row*24,.6,LIGHT)
        for i,y in enumerate((44,88,135)):
            s.circle(52,y,4,INK);s.arrow(63,y,173,91,1 if i!=1 else 2.5,GRAY if i!=1 else INK)
        s.arrow(302,92,402,92,2.7);s.circle(426,92,12,'white',1.5)
        if kind=='bsgs':
            for x in (331,363,395):s.line(x,128,x,146,1.2);s.arrow(320,151,431,151,1)
        if kind=='bloom':
            s.bitrow(35,158,'010010110',11);s.arrow(109,135,109,151,.8);s.text(363,124,'exact lookup',11)
    elif kind=='shift':
        s.circle(74,92,30,'white',1.7);s.text(74,97,'Q',18)
        s.arrow(113,92,191,92,1.8);s.circle(238,92,34,PALE,1.5)
        s.text(238,87,'subtract',11);s.text(238,104,'base x G',12)
        s.arrow(282,92,359,92,1.8);s.circle(404,92,30,'white',1.7);s.text(404,97,'D1 x G',11)
        s.path('M238 48 V21 H404 V52',.7,GRAY,'3 4')
    elif kind=='factor':
        s.chain([(53,44),(173,44),(294,44),(423,44)])
        for x in (115,235,355):
            s.arrow(x,56,x,94,1);s.circle(x,107,12,'white',1.1)
            s.line(x,119,x-25,153,.8,GRAY);s.line(x,119,x+25,153,.8,GRAY)
            s.circle(x-25,156,3);s.circle(x+25,156,3)
        s.text(235,27,'neighbor differences',11,GRAY)
    elif kind=='division':
        for i in range(4):
            s.rect(52+i*80,54,80,74,PALE,INK,1.2)
            for j in range(3):s.line(62+i*80+j*22,64,62+i*80+j*22,118,.6,LIGHT)
        s.rect(372,54,55,74,'white',INK,1.8)
        s.dots(386,72,3,5,10,GRAY,1)
        s.path('M52 144 V155 H372 V144',1.2)
        s.text(212,171,'equal-size groups',11);s.text(400,149,'remainder',10)
    elif kind=='quotient':
        for x,value in zip((57,113,169,225),('12','18','6','24')):
            s.rect(x,38,44,30,'white',INK,1);s.text(x+22,59,value,12)
        s.arrow(290,53,360,53,1.3);s.text(331,34,'divide by 6',12)
        for x,value in zip((57,113,169,225),('2','3','1','4')):
            s.rect(x,112,44,30,PALE,INK,1);s.text(x+22,133,value,12)
        s.path('M382 54 V126 H284',1.3);s.arrow(293,126,284,126,1.3)
    elif kind in ('cube','cubes','peel'):
        if kind=='cubes':
            sizes=[74,48];xs=[100,304]
        else:sizes=[88];xs=[190]
        for x,z in zip(xs,sizes):
            y=57;d=26
            s.path(f'M{x} {y} l{d} -18 h{z} l-{d} 18 Z',1.2,fill=PALE)
            s.rect(x,y,z,z,PALE,INK,1.5)
            s.path(f'M{x+z} {y} l{d} -18 v{z} l-{d} 18',1.2)
            for q in range(1,4):
                s.line(x+q*z/4,y,x+q*z/4,y+z,.5,LIGHT);s.line(x,y+q*z/4,x+z,y+q*z/4,.5,LIGHT)
        if kind=='cube':
            s.rect(289,59,34,86,'white',INK,1);s.dots(338,116,4,4,9,INK,1.4)
            s.text(343,42,'layer',11);s.line(330,48,307,59,.7,GRAY);s.text(352,160,'residual',11)
        elif kind=='cubes':s.text(243,104,'+',25);s.line(92,163,380,163,2)
        elif kind=='peel':
            s.line(190,81,278,81,2.6);s.arrow(293,80,379,51);s.rect(385,35,28,28,'white',INK,1.3);s.text(88,103,'remove',12);s.arrow(133,98,177,98)
        else:
            s.rect(51,52,100,100,PALE,INK,1.4)
            for y in (77,102,127):s.line(51,y,151,y,.8,GRAY)
            s.arrow(157,102,181,102);s.text(353,99,'q',23);s.text(353,132,'+ remainder',11)
    elif kind in ('tower','atlas','branches','tree','prune','inverse','cross'):
        if kind=='cross':
            for x in (78,138,198):s.circle(x,38,5,'white',1.4)
            for y in (70,103,136):s.circle(43,y,5)
            for x in (78,138,198):
                for y in (70,103,136):s.rect(x-9,y-9,18,18,PALE,GRAY,.8)
            s.arrow(230,103,330,103,2);s.dots(350,65,5,5,14,INK,1.6)
        elif kind=='tower':
            for i in range(5):
                x=47+i*88;y=24+i*23;s.rect(x,y,68,29,PALE if i%2 else 'white',INK,1.2)
                if i<4:s.arrow(x+68,y+15,x+88,y+38,1)
            s.path('M47 64 H80 V165 H439',.7,LIGHT,'3 5')
        elif kind=='inverse':
            s.rect(346,68,79,47,PALE,INK,1.6)
            for y in (30,80,130):s.rect(47,y,78,26,'white',GRAY,1);s.arrow(134,y+13,330,92,1,GRAY)
            s.line(45,158,125,158,3);s.text(214,157,'extra anchor chooses one',12)
        else:
            pts=[(240,22),(118,72),(357,72),(55,132),(175,132),(302,132),(423,132)]
            for a,b in ((0,1),(0,2),(1,3),(1,4),(2,5),(2,6)):
                reject=kind=='prune' and b in (3,5)
                s.line(*pts[a],*pts[b],.8 if reject else 1.7,LIGHT if reject else INK,'3 4' if reject else None)
            for i,p in enumerate(pts):s.circle(*p,6,'white' if i in (3,5) else INK,1)
            if kind=='prune':
                for x,y in (pts[3],pts[5]):s.line(x-8,y-8,x+8,y+8,1.6,GRAY);s.line(x+8,y-8,x-8,y+8,1.6,GRAY)
            if kind=='atlas':
                for x,y in pts[3:]:s.rect(x-15,y+14,30,18,PALE,GRAY,.6)
    elif kind in ('weighted','cost','resource','growth','benford','selection','gridmax'):
        if kind in ('selection','gridmax'):
            for r in range(4):
                for c in range(8):
                    chosen=(r,c)==(1,5);s.rect(60+c*46,28+r*30,38,23,INK if chosen else PALE,INK if chosen else LIGHT,.8)
            s.path('M285 51 V17 H379',1.5);s.text(408,20,'selected',11)
        elif kind=='resource':
            if mid=='M223':
                for y in (65,105,145):s.line(42,y,274,y,.8,GRAY)
                for x,y in ((80,65),(135,105),(187,65),(237,145)):
                    s.rect(x-14,y-12,28,24,'white',INK,1.2)
                s.text(156,38,'logical operation depth',11)
            else:
                for i,(h,label) in enumerate(((40,'data'),(65,'work'),(29,'ancilla'))):
                    x=58+i*75;s.rect(x,150-h,45,h,PALE,INK,1.2);s.text(x+22,168,label,10)
            s.arrow(285,101,330,101,1.8)
            for i in range(7):
                for j in range(7):s.rect(340+i*12,40+j*12,9,9,INK if (i+j)%4==0 else PALE,GRAY,.4)
        else:
            heights=[22,43,82,121,65,30,16]
            if kind=='benford':heights=[121,77,54,42,34,28,24,21,18]
            if kind=='growth':heights=[9,14,23,39,60,89,125]
            for i,h in enumerate(heights):
                x=48+i*(380/len(heights));s.rect(x,151-h,27,h,INK if i==3 else PALE,INK,1 if i==3 else .7)
                if kind=='benford':s.text(x+13,168,str(i+1),10,GRAY)
            s.line(35,152,449,152,.9)
            if kind=='cost':s.path('M45 137 Q180 60 432 32',2.4);s.text(358,24,'work curve',11)
            if kind=='weighted':s.text(240,20,'relative allocation',12,GRAY)
    elif kind in ('glv','lattice','surface'):
        for i in range(8):
            for j in range(5):s.circle(79+i*43+j*10,37+j*26,1.2,LIGHT,0,LIGHT)
        if kind=='glv':
            s.arrow(105,137,270,137,2.7);s.arrow(270,137,330,46,2.7);s.arrow(105,137,330,46,1.4,GRAY)
            s.text(184,157,'part 1',12);s.text(338,102,'part 2',12);s.circle(330,46,5)
        elif kind=='lattice':
            s.path('M111 142 L309 20 L352 67 L155 164 Z',1.7,fill=PALE)
            for p in ((174,113),(217,87),(260,61)):s.circle(*p,4)
        else:
            for i in range(6):s.path(f'M60 {80+i*15} Q200 {15+i*11} 422 {70+i*15}',1,GRAY)
            for i in range(8):
                x=75+i*46;s.path(f'M{x} 78 Q{x+30} 112 {x+12} 158',.7,GRAY)
            s.circle(270,101,6);s.line(270,101,270,36,1.6);s.text(270,24,'estimate',12)
    elif kind in ('benchmark','holdout','train','null','oracle'):
        for y in (55,123):
            s.line(45,y,433,y,.8,LIGHT)
            for i in range(10):s.circle(53+i*39,y,3.5,GRAY if y==123 else INK,0)
        if kind in ('holdout','train'):
            if kind=='holdout':
                s.circle(248,55,9,'white',1.8);s.arrow(248,70,248,105,1.5);s.text(248,158,'hidden until scoring',12)
            else:
                s.line(292,25,292,149,1.5,GRAY,'4 4');s.arrow(110,88,271,88,2);s.text(355,92,'future',12)
        elif kind=='oracle':
            s.rect(175,28,131,49,PALE,INK,1.2);s.text(240,57,'supplied truth',12)
            s.rect(175,98,131,49,'white',INK,1.2);s.text(240,128,'estimated',12)
        elif kind=='benchmark':
            for y,w in ((40,105),(108,165)):s.rect(136,y,w,30,PALE,INK,1.2)
            s.text(355,64,'A',15);s.text(355,130,'B',15)
        else:
            s.path('M59 153 Q142 147 180 105 Q231 37 280 103 Q327 147 428 152',2.1)
            s.path('M59 153 Q153 146 192 98 Q244 48 290 106 Q338 148 428 152',1.1,GRAY,'4 4')
            s.text(240,21,'same statistic / same selection',11,GRAY)
    elif kind in ('regression','sequence','interpolate','converge','sensitivity'):
        s.line(43,151,446,151,.8,GRAY);s.line(43,151,43,24,.8,GRAY)
        points=[(65,132),(120,119),(179,102),(237,93),(298,62),(356,49),(421,32)]
        if kind=='converge':points=[(64,45),(115,120),(174,79),(231,101),(291,91),(353,96),(421,94)]
        for i,p in enumerate(points):s.circle(*p,3.5,'white' if i==3 else INK,1)
        if kind in ('sequence','converge'):
            s.chain(points);s.circle(*points[3],8,'white',1.2)
        elif kind=='interpolate':
            s.line(*points[1],*points[5],1.8);s.circle(237,84,6,'white',1.7);s.line(237,84,237,151,.8,GRAY,'3 4')
        else:
            s.path('M56 142 Q227 81 430 27',2.4)
            if kind=='sensitivity':s.path('M56 132 Q227 111 430 52',1,GRAY,'3 4');s.arrow(345,66,345,43,1.2)
            else:s.path('M57 151 Q225 96 430 45',.7,LIGHT);s.path('M57 124 Q225 66 430 13',.7,LIGHT)
    elif kind in ('bucket','donor','roots'):
        offsets=(80,80 if mid=='M073' else 190*80/141)
        for (x,w),offset in zip(((53,141),(260,190)),offsets):
            s.rect(x,51,w,82,'white',GRAY,1);s.rect(x,96,offset,37,PALE,'none');s.line(x+offset,43,x+offset,141,2.4)
            s.circle(x+offset,96,5)
        s.arrow(204,87,249,87,2)
        if kind=='roots':
            s.text(122,31,'root bucket',12);s.text(365,31,'normalized',12)
        elif kind=='donor':
            endpoint=260+offsets[1]
            s.path('M54 151 H133 M54 145 V157 M133 145 V157',1.2)
            s.path(f'M260 151 H{endpoint:g} M260 145 V157 M{endpoint:g} 145 V157',1.2)
        else:s.text(240,126,'share',12,GRAY)
    elif kind in ('bits','mask','bitgrid','bitvote','stego','lfsr','prng','coupled','fibonacci'):
        if kind=='prng':
            s.rect(58,66,86,59,PALE,INK,1.7);s.rect(235,66,86,59,'white',INK,1.7)
            s.text(101,101,'state',13);s.text(278,101,'update',13);s.arrow(154,95,222,95,2)
            s.path('M278 57 V27 H101 V57',1.1,GRAY);s.arrow(329,95,407,95,1.6);s.bitrow(373,140,'10101',12)
        elif kind=='lfsr':
            s.bitrow(78,79,'101001101101',26)
            for x in (108,237,367):s.line(x,76,x,35,1.1)
            s.line(108,35,412,35,1.3);s.path('M412 35 V140 H58 V94 H71',1.5)
            s.circle(237,35,9,'white',1.3);s.line(232,35,242,35,1);s.line(237,30,237,40,1)
        elif kind=='coupled':
            s.bitrow(61,47,'10110101');s.bitrow(275,118,'11000110')
            s.arrow(182,67,316,105,2);s.arrow(316,106,181,67,1,GRAY,'3 4')
            s.path('M88 79 V140 H251',1);s.path('M389 105 V42 H226',1)
        elif kind=='fibonacci':
            terms=[1,2,3,5,8,13,21,34,55]
            for i,n in enumerate(terms):
                x=42+i*47;s.circle(x,80,13,INK if i in (1,4,7) else 'white',1);s.text(x,84,str(n),11,'white' if i in (1,4,7) else INK)
            s.line(89,118,371,118,1.4);s.text(240,144,'separated active terms',12)
        else:
            rows=['1011010010110010','0011010000100010','1000000010010000']
            if kind=='bitgrid':rows=['0011100000000000','0011010000000000','0011001000000000','0011000100000000']
            for i,row in enumerate(rows):s.bitrow(62,30+i*37,row,22)
            if kind in ('mask','stego'):
                s.text(35,81,'XOR',10,GRAY);s.line(55,99,413,99,.8,GRAY)
            if kind=='bitvote':
                s.rect(60+6*22,23,21,117,'none',INK,2);s.arrow(200,147,320,147,1.4);s.text(366,151,'vote',12)
    elif kind in ('hamming','cluster'):
        center=(240,92)
        for radius in (37,72):s.circle(*center,radius,'none',.7,LIGHT)
        for i in range(12):
            a=i*math.pi/6;r=37 if i%2 else 72;x=240+r*math.cos(a);y=92+r*math.sin(a)
            s.line(*center,x,y,.6,LIGHT);s.circle(x,y,3.5,INK if i%3==0 else 'white',1)
        s.circle(*center,7)
        if kind=='cluster':
            for x,y in ((73,48),(91,76),(67,100),(393,56),(414,94),(382,126)):s.circle(x,y,3,GRAY)
            s.path('M99 76 L173 92 M313 92 L383 94',.8,GRAY,'3 4')
    elif kind in ('feedback','waves'):
        if kind=='feedback':
            for x,y in ((75,78),(229,32),(371,110)):s.rect(x-31,y-20,62,40,PALE,INK,1.6)
            s.arrow(111,65,191,36,1.8);s.arrow(265,46,337,95,1.8);s.path('M365 135 Q205 183 81 105',1.8);s.arrow(90,114,81,105,1.8)
        else:
            for j in range(3):
                points=[(42+i*4,42+j*45+12*math.sin(i*.19+j)) for i in range(100)]
                s.path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in points),2.3 if j==0 else .9,INK if j==0 else GRAY)
    elif kind in ('diameter','cantor','ap'):
        if kind=='diameter':
            points=[(65,75),(102,116),(150,46),(237,89),(297,53),(344,128),(414,82)]
            for p in points:s.circle(*p,4)
            s.line(*points[0],*points[-1],2.8);s.circle(*points[0],9,'none',.8);s.circle(*points[-1],9,'none',.8)
            s.path('M65 146 H414 M65 140 V152 M414 140 V152',1.2)
        elif kind=='cantor':
            segments=[(40,440)]
            for level in range(4):
                for a,b in segments:s.line(a,31+level*36,b,31+level*36,5 if level==0 else 3.2)
                segments=[(a,a+(b-a)/3) for a,b in segments]+[(b-(b-a)/3,b) for a,b in segments]
            if mid=='M123':s.text(240,165,'proposed mapping ?',12,GRAY)
        else:
            for y in (55,113):
                for i in range(13):s.circle(45+i*32,y,3,INK if i in (2,5,8) else LIGHT,0)
            s.line(109,55,301,55,2);s.path('M109 73 V87 H205 V73 M205 73 V87 H301 V73',.9)
            s.text(205,159,'equal gaps / selected labels',12,GRAY)
    elif kind in ('nonce','signatures','reusednonce','leak'):
        if kind=='leak':
            s.bitrow(55,41,'1100000000000011',23)
            for i in range(7):s.line(100+i*35,84,80+i*35,151,.65,LIGHT)
            for i in range(4):s.line(80,89+i*18,385,89+i*18,.65,LIGHT)
            s.circle(239,123,5);s.rect(207,94,62,52,'none',INK,2);s.text(396,147,'bounds',11)
        else:
            for y in (45,122):s.rect(47,y-17,92,34,'white',INK,1.2);s.text(93,y+4,'signature',11)
            s.circle(240,83,21,PALE,1.7);s.text(240,87,'nonce',11)
            s.line(145,45,219,76,1.3);s.line(145,122,219,91,1.3)
            s.arrow(269,83,349,83,2.2);s.rect(364,63,55,40,'white',INK,1.2)
            if kind=='reusednonce':s.text(240,39,'reused',12);s.text(392,89,'key',12)
            else:s.text(392,88,'test',12)
    elif kind in ('graph','fanout','distributed','parallel'):
        if kind=='parallel':
            for y in (40,80,120):
                for x in (63,175,287,399):s.rect(x-17,y-12,34,24,PALE,INK,.9)
                s.arrow(86,y,148,y,1.5);s.arrow(198,y,260,y,1.5);s.arrow(310,y,372,y,1.5)
            s.line(35,24,35,139,2);s.line(444,24,444,139,2)
        else:
            points=[(68,85),(190,30),(190,85),(190,144),(320,39),(320,127),(432,84)]
            edges=[(0,1),(0,2),(0,3),(1,4),(2,4),(2,5),(3,5),(4,6),(5,6)]
            if kind=='fanout':edges=[(0,2),(2,1),(2,3),(2,4),(2,5),(4,6)]
            for i,(a,b) in enumerate(edges):s.line(*points[a],*points[b],2.4 if i%3==0 else .8,INK if i%3==0 else GRAY)
            for i,p in enumerate(points):s.circle(*p,8 if i in (0,2) else 5,INK if i in (0,2) else 'white',1.3)
            if kind=='distributed':
                for p in points[1:-1]:s.rect(p[0]-13,p[1]-13,26,26,'none',GRAY,.6)
    elif kind in ('certificate','gate','probe'):
        s.rect(45,34,111,116,'white',INK,1.5)
        for y in range(54,134,18):s.line(62,y,136,y,.8,GRAY)
        s.arrow(166,92,221,92,1.8)
        s.path('M255 56 L292 92 L255 128 L219 92 Z',1.6,fill=PALE)
        s.arrow(300,92,379,92,2.4);s.circle(408,92,15,'white',1.8)
        if kind=='probe':s.text(255,95,'small',11);s.text(408,97,'?',17)
        elif kind=='gate':
            s.arrow(255,136,255,161,.8,GRAY);s.text(292,165,'reject',11,GRAY)
        else:s.text(255,97,'bounds',10)
    elif kind in ('clock','archive','circuit'):
        if kind=='clock':
            s.circle(109,88,52,'white',1.5)
            for i in range(12):
                a=i*math.pi/6;s.line(109+44*math.cos(a),88+44*math.sin(a),109+49*math.cos(a),88+49*math.sin(a),.8)
            s.line(109,88,109,52,2.5);s.line(109,88,136,103,1.4);s.arrow(180,88,258,88,2)
            s.rect(278,62,107,55,PALE,INK,1.2);s.dots(296,78,8,3,10,INK,1)
        elif kind=='archive':
            for i in range(3):s.rect(50+i*13,47-i*10,89,111,'white',GRAY,1)
            for y in range(61,126,18):s.line(95,y,137,y,.8,GRAY)
            s.arrow(177,91,246,91,1.8);s.circle(309,83,38,'none',2.4);s.line(336,111,382,151,5)
            s.dots(291,66,4,4,11,GRAY,1)
        else:
            for y in (52,101,146):
                s.line(48,y,433,y,.9,GRAY)
            for x,y,label in ((117,52,'H'),(216,101,'U'),(323,52,'QFT')):
                s.rect(x-20,y-17,40,34,'white',INK,1.4);s.text(x,y+4,label,10)
            s.line(216,52,216,146,1.2);s.circle(216,52,4);s.circle(216,146,8,'white',1.2)
            s.text(367,164,'schematic resource pipeline',10,GRAY)
    elif kind=='checkpoint':
        s.chain([(42,98),(111,75),(181,108),(258,82),(337,104),(431,75)],True)
        s.rect(215,28,83,36,'white',INK,1.5);s.text(257,51,'state',12);s.arrow(258,79,258,65,1)
        s.path('M291 50 Q375 3 419 54',1.1,GRAY,'3 4');s.arrow(419,54,425,63,1.1,GRAY)
    elif kind=='venn':
        s.circle(194,89,65,'none',1.5);s.circle(280,89,65,'none',1.5)
        for y in range(53,130,9):
            for x in range(222,254,8):
                if (x-194)**2+(y-89)**2<65**2 and (x-280)**2+(y-89)**2<65**2:s.circle(x,y,1,GRAY,0)
        s.text(171,93,'A',16);s.text(301,93,'B',16);s.text(238,166,'shared / total set bits',12)
    elif kind=='residue':
        for i in range(9):
            x=48+i*47;s.rect(x,62,30,64,PALE if i%3 else 'white',GRAY,.8);s.text(x+15,145,str(i),11)
            for j in range(1+(i*5)%5):s.circle(x+15,113-j*10,2.4,INK)
        s.arrow(65,30,420,30,.9,GRAY);s.text(240,19,'residue classes',12)
    elif kind=='triangle':
        rows=[[2,5,9,14],[3,4,5],[1,1],[0]]
        for level,row in enumerate(rows):
            y=28+level*40;xs=[88+level*50+i*100 for i in range(len(row))]
            for x,value in zip(xs,row):s.circle(x,y,12,'white',1);s.text(x,y+4,str(value),12)
            if level<3:
                for i in range(len(row)-1):
                    tx=138+level*50+i*100;s.line(xs[i]+9,y+11,tx,y+28,.65,LIGHT);s.line(xs[i+1]-9,y+11,tx,y+28,.65,LIGHT)
    else:raise ValueError(f'No drawing recipe for {kind}')
    return s.svg(method,labels)


def wrap(text,width,size,font=FONT):
    result=[]
    for paragraph in str(text).splitlines() or ['']:
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if line and font.text_length(candidate,fontsize=size)>width:
                result.append(line);line=word
            else:line=candidate
        result.append(line)
    return result


def fonts(page):
    page.insert_font(fontname='AtlasSans',fontfile=FONT_PATH)
    page.insert_font(fontname='AtlasBold',fontfile=BOLD_PATH)


def put(page,x,y,text,size=9,bold=False,color=(.1,.1,.1)):
    page.insert_text((x,y),text,fontsize=size,fontname='AtlasBold' if bold else 'AtlasSans',color=color)


def text_block(page,x,y,text,width,size=8.1,bold=False):
    lines=wrap(text,width,size,BOLD if bold else FONT)
    for i,line in enumerate(lines):put(page,x,y+i*size*1.35,line,size,bold)
    return y+len(lines)*size*1.35


def main():
    payload=json.loads(SOURCE.read_text());methods=payload['methods']
    specs={}
    for line in (ROOT/'diagram_specs.tsv').read_text().splitlines():
        if not line.strip():continue
        ident,kind,*labels=line.split('\t')
        if ident in specs:raise ValueError('Duplicate specification '+ident)
        if len(labels)!=3:raise ValueError('Expected three visual stages for '+ident)
        specs[ident]=(kind,labels)
    assert set(specs)=={m['id'] for m in methods},'Method/spec coverage mismatch'
    methods_by_id={m['id']:m for m in methods}
    svgs={};vector_docs={};manifest=[]
    for method in methods:
        ident=method['id'];kind,labels=specs[ident]
        svg=sketch(method,kind,labels)
        filename=ident+'-'+kind+'.svg';(ROOT/'svg'/filename).write_text(svg)
        source=fitz.open(stream=svg.encode(),filetype='svg')
        vector=fitz.open(stream=source.convert_to_pdf(),filetype='pdf')
        svgs[ident]=svg;vector_docs[ident]=vector
        manifest.append({**method,'diagram_kind':kind,'visual_stages':labels,'svg_file':'svg/'+filename,
                         'svg_sha256':hashlib.sha256(svg.encode()).hexdigest()})
    doc=fitz.open();toc=[]
    page=doc.new_page(width=842,height=595);fonts(page)
    put(page,38,57,'METHODS, DRAWN.',34,True)
    put(page,40,87,'225 monochrome mechanism studies',14,color=(.35,.35,.35))
    put(page,40,114,'A visual companion to the Bitcoin research inventory',11)
    intro='Black marks show the active object or route. Gray marks show context, alternatives, or supporting structure. Thin rules show relationships; heavier strokes show the operation being emphasized.'
    text_block(page,40,150,intro,370,11)
    intro2='Each method retains its original ID, evidence label, and report finding. Schematic positions and weights are illustrative. The drawings describe mechanisms, including hypotheses and unsuccessful routes; the source finding states what was actually established.'
    text_block(page,40,242,intro2,370,10)
    for ident,rect in [('M022',fitz.Rect(445,112,806,289)),('M202',fitz.Rect(445,321,806,498))]:
        page.show_pdf_page(rect,vector_docs[ident],0)
        put(page,445,rect.y0-8,ident+' / '+methods_by_id[ident]['method'],9,True)
    put(page,40,407,'Visual vocabulary',13,True)
    page.draw_line((41,433),(120,433),color=(.08,.08,.08),width=2.7)
    put(page,134,437,'active operation',10)
    page.draw_line((41,458),(120,458),color=(.65,.65,.65),width=.65)
    put(page,134,462,'context or relationship',10)
    page.draw_circle((52,486),3,color=(.08,.08,.08),fill=(.08,.08,.08))
    page.draw_circle((81,486),5,color=(.08,.08,.08),fill=(1,1,1))
    put(page,134,490,'states, values, or candidate positions',10)
    put(page,40,557,'Vector drawings • 14 method families • 225 source-linked entries',10,color=(.35,.35,.35))
    toc.append([1,'Visual guide',1])
    groups=defaultdict(list)
    for method in methods:groups[method['category']].append(method)
    page=doc.new_page(width=842,height=595);fonts(page)
    put(page,35,49,'CONTENTS',25,True)
    put(page,35,77,'Methods are grouped exactly as in the source inventory.',10,color=(.4,.4,.4))
    contents=[];index_page=2
    for number,(category,rows) in enumerate(groups.items(),1):
        first_page=len(doc)+1
        contents.append((category,rows,first_page))
        toc.append([1,f'{number:02d}  {category}',first_page])
        for start in range(0,len(rows),4):
            page=doc.new_page(width=842,height=595);fonts(page)
            header=wrap(category,710,11,BOLD)
            for i,line in enumerate(header):put(page,28,23+i*13,line,11,True)
            put(page,780,23,f'{number:02d}',10,color=(.5,.5,.5))
            for index,method in enumerate(rows[start:start+4]):
                ident=method['id'];x=28+(index%2)*401;y=52+(index//2)*263
                rect=fitz.Rect(x,y,x+385,y+250)
                page.draw_rect(rect,color=(.83,.83,.83),width=.55)
                put(page,x+11,y+14,ident+'  /  SCHEMATIC',7.5,True,color=(.4,.4,.4))
                evidence=method['evidence']
                if FONT.text_length(evidence,fontsize=7)>170:evidence='Source evidence label in manifest'
                put(page,x+192,y+14,evidence,7,color=(.4,.4,.4))
                title_lines=wrap(method['method'],363,10.3,BOLD)
                assert len(title_lines)<=2,(ident,title_lines)
                for j,line in enumerate(title_lines):put(page,x+11,y+30+j*12,line,10.3,True)
                page.show_pdf_page(fitz.Rect(x+8,y+45,x+377,y+201),vector_docs[ident],0)
                finding='Finding: '+method['finding']
                size=7.35
                while len(wrap(finding,363,size))*size*1.3>40:size-=.15
                assert size>=6,(ident,'Finding text too long')
                last=text_block(page,x+11,y+211,finding,363,size)
                assert last<=y+249,(ident,'Card overflow',last-y)
                toc.append([2,ident+'  '+method['method'],len(doc)])
                manifest[int(ident[1:])-1]['atlas_page']=len(doc)
            put(page,28,586,'Line-art companion • original findings retained • full SVGs indexed by method ID',7,color=(.5,.5,.5))
            put(page,790,586,str(len(doc)),7,color=(.5,.5,.5))
    page=doc[1]
    for i,(category,rows,number) in enumerate(contents):
        y=112+i*30
        put(page,35,y,f'{i+1:02d}',10,True)
        put(page,70,y,category,9)
        put(page,720,y,f'{len(rows)} methods',8,color=(.4,.4,.4))
        put(page,803,y,str(number),9,True)
        page.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(33,y-13,815,y+6),'page':number-1})
    doc.set_toc(toc)
    doc.set_metadata({'title':'Methods, Drawn — 225 Monochrome Mechanism Studies','author':'Research inventory visual companion','subject':'Source-linked line-art representations of recorded research methods'})
    atlas=ROOT/'METHODS_DRAWN_225.pdf'
    doc.save(atlas,garbage=4,deflate=True)
    # Diverse 12-method contact sheet, with all drawing geometry still vector.
    preview_ids=['M022','M038','M053','M059','M088','M108','M122','M134','M153','M185','M202','M223']
    preview=fitz.open();page=preview.new_page(width=1200,height=1110);fonts(page)
    put(page,26,42,'METHODS, DRAWN.',28,True)
    put(page,27,67,'A first look at 12 of the 225 monochrome mechanism drawings',12,color=(.4,.4,.4))
    for i,ident in enumerate(preview_ids):
        x=25+(i%3)*392;y=92+(i//3)*248
        page.draw_rect(fitz.Rect(x,y,x+366,y+230),color=(.82,.82,.82),width=.7)
        put(page,x+12,y+18,ident,9,True,color=(.4,.4,.4))
        title_lines=wrap(methods_by_id[ident]['method'],342,10.5,BOLD)
        for j,line in enumerate(title_lines):put(page,x+12,y+36+j*13,line,10.5,True)
        page.show_pdf_page(fitz.Rect(x+5,y+60,x+361,y+224),vector_docs[ident],0)
    preview.save(ROOT/'LINE_ART_PREVIEW.pdf',garbage=4,deflate=True)
    page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(ROOT/'LINE_ART_PREVIEW.png')
    payload={'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
             'diagram_count':len(manifest),'family_count':len(groups),'atlas_pages':len(doc),
             'style':'Monochrome vector line art; 0.5–5 unit strokes, open and filled points, gray density and line hierarchy.',
             'interpretation':'Schematic positions and weights; original findings retained for claim calibration.',
             'methods':manifest}
    (ROOT/'diagram_manifest.json').write_text(json.dumps(payload,indent=2)+'\n')
    (ROOT/'README.md').write_text('# Methods, Drawn\n\n225 monochrome vector diagrams for the existing research inventory.\n\n- METHODS_DRAWN_225.pdf: complete illustrated atlas with category and method bookmarks.\n- LINE_ART_PREVIEW.png / .pdf: 12-method contact sheet.\n- svg/: one editable vector diagram per method.\n- diagram_manifest.json: original method text, sources, findings, visual stages, hashes, and atlas page numbers.\n- diagram_specs.tsv: explicit method-to-drawing assignments and labels.\n- build_line_art.py: reproducible local renderer.\n\nMarks and weights are schematic. Findings and evidence labels come from methods-with-math.json. The companion preserves that file and the original reports.\n')
    # Check actual written PDF coverage and all individual SVG renders.
    written=fitz.open(atlas)
    text='\n'.join(p.get_text() for p in written)
    missing=[m['id'] for m in methods if m['id'] not in text]
    assert not missing,missing
    assert len(list((ROOT/'svg').glob('*.svg')))==len(methods)
    normalize=lambda value:re.sub(r'\s+',' ',value).strip()
    all_text=normalize(text)
    assert all(normalize(method['finding']) in all_text for method in methods),'A source finding was dropped'
    for record in manifest:
        tree=ET.parse(ROOT/record['svg_file'])
        for node in tree.iter('{http://www.w3.org/2000/svg}text'):
            x,y,size=[float(node.get(attribute)) for attribute in ('x','y','font-size')]
            font=BOLD if node.get('font-weight')=='bold' else FONT
            width=font.text_length(node.text or '',fontsize=size)
            anchor=node.get('text-anchor','start')
            left=x-width/2 if anchor=='middle' else x-width if anchor=='end' else x
            assert left>=-.5 and left+width<=480.5 and y-size>=-.5 and y+size*.25<=235.5,(record['id'],node.text,'text bounds')
    validation={'method_count':len(methods),'svg_count':len(vector_docs),'atlas_pages':len(written),
                'all_methods_present_in_pdf':not missing,'all_svg_files_rendered':True,
                'all_original_findings_present_in_pdf':True,'svg_text_bounds_checked':len(methods),
                'text_out_of_bounds':[],'gray_code_cycle_single_bit_changes':True,
                'source_unchanged':hashlib.sha256(SOURCE.read_bytes()).hexdigest()==payload['source_sha256']}
    (ROOT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'METHOD_DIAGRAMS_SVG.zip','w',compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted((ROOT/'svg').glob('*.svg')):bundle.write(path,path.relative_to(ROOT))
        for name in ('README.md','diagram_manifest.json','diagram_specs.tsv','validation.json'):
            bundle.write(ROOT/name,name)
    print(json.dumps({'atlas':str(atlas),'preview':str(ROOT/'LINE_ART_PREVIEW.png'),**validation},indent=2))


if __name__=='__main__':main()
