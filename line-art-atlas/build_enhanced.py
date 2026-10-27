#!/usr/bin/env python3
"""Second-edition detailed mechanism plates, themed by source inventory family."""
from collections import defaultdict
import hashlib
import html
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile
import unicodedata

import pymupdf as fitz
import build_line_art as base
from svg_pdf import svg_to_pdf

ROOT=Path(__file__).resolve().parent/'enhanced'
NS='{http://www.w3.org/2000/svg}'
THEMES=[
 ('COVERAGE / VERIFICATION','ruler'),('TRACKS / COLLISIONS','tracks'),
 ('VOLUMES / DECOMPOSITION','volume'),('TRACES / VALIDATION','trace'),
 ('BUCKETS / TRANSFER','bucket'),('REGISTERS / GENERATORS','register'),
 ('BITS / NEIGHBORHOODS','bits'),('SETS / TOPOLOGY','cantor'),
 ('SIGNATURES / CONSTRAINTS','signature'),('GRAPHS / RELATIONS','network'),
 ('SEEDS / ENTROPY','seed'),('RESIDUES / STRUCTURE','residue'),
 ('LAYERS / DIFFERENCES','triangle'),('CIRCUITS / RESOURCES','circuit'),
]


def escape(value):return html.escape(str(value),quote=True)


def text(x,y,value,size=22,bold=False,fill='#151515',anchor='start'):
 return f'<text x="{x:g}" y="{y:g}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="{fill}">{escape(value)}</text>'


def paragraph(x,y,value,width,size=22,leading=1.4,fill='#333333',bold=False):
 lines=base.wrap(value,width,size,base.BOLD if bold else base.FONT)
 return ''.join(text(x,y+i*size*leading,line,size,bold,fill) for i,line in enumerate(lines)),y+len(lines)*size*leading


def line(x1,y1,x2,y2,width=1,color='#bcbcbc',dash=''):
 return f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" fill="none" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'


def rect(x,y,w,h,fill='none',stroke='#cccccc',width=1,dash=''):
 return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'


def motif(name):
 s=base.Scene()
 if name=='ruler':
  s.line(8,48,94,48,2)
  for i in range(9):s.line(10+i*10,34 if i%2 else 22,10+i*10,62,1)
 elif name=='tracks':
  s.chain([(5,16),(30,28),(49,47),(72,43),(94,64)],True)
  s.chain([(5,81),(27,67),(49,47)])
  s.circle(49,47,7,'white',1.5);s.circle(49,47,2)
 elif name=='volume':
  s.rect(18,31,51,51,base.PALE,base.INK,1.5)
  s.path('M18 31 L41 14 H92 L69 31 M69 31 L92 14 V65 L69 82',1.2)
  for z in (35,52):s.line(z,31,z,82,.55,base.LIGHT)
 elif name=='trace':
  s.line(10,86,94,86,.7,base.GRAY);s.line(10,86,10,10,.7,base.GRAY)
  s.path('M16 76 Q47 25 93 19',2)
  for x,y in ((24,64),(45,45),(67,31),(88,22)):s.circle(x,y,3)
 elif name=='bucket':
  s.rect(9,23,34,60,'white',base.INK,1);s.rect(60,11,34,72,'white',base.INK,1)
  s.line(29,19,29,88,2);s.line(80,7,80,88,2);s.arrow(44,45,59,45,1)
 elif name=='register':
  s.bitrow(7,40,'101101',15)
  s.path('M16 36 V13 H91 V79 H6 V50',1)
 elif name=='bits':
  for i in range(4):
   for j in range(4):s.rect(12+i*20,12+j*20,15,15,base.INK if (i,j) in ((0,1),(1,3),(3,0),(2,2)) else 'white',base.GRAY,.8)
 elif name=='cantor':
  segments=[(7,94)]
  for i in range(4):
   for a,b in segments:s.line(a,17+i*21,b,17+i*21,3 if i else 4)
   segments=[(a,a+(b-a)/3) for a,b in segments]+[(b-(b-a)/3,b) for a,b in segments]
 elif name=='signature':
  s.rect(5,11,26,22,'white',base.INK,1);s.rect(5,69,26,22,'white',base.INK,1)
  s.line(32,23,59,50);s.line(32,80,59,50);s.circle(64,50,11,base.PALE,1.3);s.arrow(76,50,97,50,1.4)
 elif name=='network':
  points=[(13,50),(44,15),(44,84),(73,50),(95,12),(95,88)]
  for a,b in ((0,1),(0,2),(1,3),(2,3),(3,4),(3,5)):s.line(*points[a],*points[b],1)
  for i,p in enumerate(points):s.circle(*p,4,base.INK if i in (0,3) else 'white')
 elif name=='seed':
  s.circle(26,48,17,'white',1.5);s.circle(26,48,3)
  s.arrow(47,48,70,48,1.5);s.rect(76,17,18,63,base.PALE,base.INK,1)
  for y in (28,43,58,73):s.line(79,y,92,y,.6,base.GRAY)
 elif name=='residue':
  for i in range(9):
   a=2*math.pi*i/9;s.circle(50+36*math.cos(a),50+36*math.sin(a),3,base.INK if i%3==0 else 'white')
  s.circle(50,50,2);s.line(50,50,86,50,1.3)
 elif name=='triangle':
  for level in range(4):
   for i in range(4-level):
    x=14+level*12+i*24;y=14+level*24;s.circle(x,y,3,'white',1)
    if level<3 and i<3-level:s.line(x+2,y+4,x+11,y+20,.6,base.LIGHT);s.line(x+22,y+4,x+13,y+20,.6,base.LIGHT)
 else:
  for y in (23,50,77):s.line(5,y,95,y,.8,base.GRAY)
  for x,y in ((25,23),(50,50),(78,77)):s.rect(x-8,y-8,16,16,'white',base.INK,1.3)
  s.line(50,23,50,77,1);s.circle(50,23,3)
 return ''.join(s.parts)


def focus(kind):
 if kind in ('collision','near'):return (197,67,58,58)
 if kind in ('cube','cubes','peel'):return (271,48,65,88)
 if kind in ('glv','lattice','surface'):return (238,88,81,73)
 if kind in ('holdout','oracle','train'):return (214,33,70,100)
 if kind=='lfsr':return (205,20,72,81)
 if kind in ('gray','orbit','collatz','permutation'):return (280,56,70,90)
 if kind=='cantor':return (35,59,137,96)
 if kind in ('nonce','signatures','reusednonce'):return (207,50,83,70)
 if kind in ('graph','fanout','distributed'):return (157,51,77,86)
 if kind=='fibonacci':return (196,48,78,72)
 if kind in ('triangle','factor'):return (190,52,94,93)
 if kind=='resource':return (344,45,68,73)
 if kind in ('bucket','donor','roots'):return (317,48,84,93)
 if kind in ('table','bsgs','bloom'):return (184,57,108,80)
 if kind in ('prng','coupled'):return (233,51,92,79)
 if kind in ('bits','mask','bitgrid','bitvote','stego','leak'):return (184,29,81,85)
 if kind in ('clock','archive'):return (65,45,91,91) if kind=='clock' else (267,39,88,88)
 if kind in ('certificate','gate','probe','shift'):return (210,52,90,82)
 if kind in ('tree','branches','prune','inverse','atlas','tower'):return (188,25,118,115)
 if kind in ('regression','sequence','interpolate','converge','sensitivity','null'):return (200,47,105,96)
 if kind in ('weighted','cost','growth','benford','gridmax','selection'):return (167,37,117,112)
 if kind in ('derive','formats','fork','stream'):return (206,57,84,81)
 if kind=='hashchain':return (170,61,72,72)
 if kind=='parse':return (189,47,99,99)
 if kind=='division':return (345,45,94,97)
 if kind=='quotient':return (161,28,118,117)
 if kind=='residue':return (181,53,99,95)
 if kind=='circuit':return (183,37,79,111)
 if kind=='checkpoint':return (209,22,94,88)
 if kind=='venn':return (204,54,71,86)
 if kind=='diameter':return (211,46,100,95)
 if kind=='ap':return (184,37,108,98)
 if kind=='waves':return (193,47,105,96)
 return (182,49,116,99)


def enrich_core(method,kind,core):
 root=ET.fromstring(core);s=base.Scene();ident=method['id']
 if kind=='collision' and ident in ('M022','M146','M215'):
  s.text(83,24,'distance t',10,base.GRAY)
  s.text(85,165,'distance '+('s' if ident=='M215' else 'w'),10,base.GRAY)
 elif kind=='cube':
  s.text(139,93,'R^3',13);s.arrow(158,89,185,89,.8,base.GRAY)
  s.text(396,131,'D',12,base.GRAY);s.line(384,128,370,128,.7,base.GRAY)
 elif kind=='cubes':
  s.text(136,106,'a^3',12);s.text(328,87,'b^3',11)
 elif kind=='holdout':
  s.path('M53 23 V16 H209 V23',.75,base.GRAY);s.text(131,11,'fit on retained examples',9,base.GRAY)
 elif kind=='lfsr':s.text(330,22,'feedback',10,base.GRAY)
 elif kind=='prng':
  operators={'M087':'a*x + c','M093':'MT twist','M161':'MT twist','M163':'MT64',
             'M165':'LCG48','M166':'SHA-1','M168':'x 16807','M169':'x 48271',
             'M171':'MT / range','M172':'old twist','M176':'subtract'}
  for node in root.iter(NS+'text'):
   if node.text=='update':node.text=operators.get(ident,'state rule')
  s.text(100,145,'seeded state',10,base.GRAY)
 elif kind in ('mask','stego'):
  for y,label in ((41,'input'),(78,'mask'),(115,'result')):s.text(33,y,label,8.5,base.GRAY)
 elif kind=='prune':
  s.text(55,161,'pruned',9,base.GRAY);s.text(302,161,'pruned',9,base.GRAY)
 elif kind in ('glv',):
  for node in root.iter(NS+'text'):
   if node.text=='part 1':node.text='k1' if ident=='M053' else 'dA'
   elif node.text=='part 2':node.text='lambda k2' if ident=='M053' else 'lambda dB'
 elif kind=='fanout':
  pts=[(68,85),(190,30),(190,85),(190,144),(320,39),(320,127),(432,84)]
  for a,b in ((0,2),(2,1),(2,3),(2,4),(2,5),(4,6)):
   x1,y1=pts[a];x2,y2=pts[b]
   x,y=x1+(x2-x1)*.68,y1+(y2-y1)*.68;angle=math.atan2(y2-y1,x2-x1)
   for delta in (-.55,.55):s.line(x,y,x-6*math.cos(angle+delta),y-6*math.sin(angle+delta),.85)
 elif kind in ('nonce','signatures','reusednonce'):
  count=0
  for node in root.iter(NS+'text'):
   if node.text=='signature':
    count+=1
    if kind=='nonce':node.text='r, s' if count==1 else 'key relation'
    else:node.text=('r' if kind=='reusednonce' else 'r'+str(count))+', s'+str(count)
 elif kind=='resource':
  s.path('M340 129 V138 H421 V129',.8,base.GRAY);s.text(380,153,'code distance d',9,base.GRAY)
 elif kind=='triangle':
  s.text(416,32,'mod m',10,base.GRAY)
  for x,y in ((136,49),(236,49),(336,49)):s.text(x,y,'-',10,base.GRAY)
 elif kind=='cantor':s.text(240,53,'middle thirds',9,base.GRAY)
 elif kind=='fibonacci':s.text(239,39,'2 + 8 + 34 = 44',10,base.GRAY)
 elif kind=='weighted':
  s.path('M45 24 V15 H438 V24',.75,base.GRAY)
  s.text(240,40,'shared work budget',9,base.GRAY)
 if s.parts:
  extra=ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(s.parts)+'</svg>')
  for child in extra:root.append(child)
 for node in root.iter(NS+'text'):
  size=float(node.get('font-size'));x=float(node.get('x'));y=float(node.get('y'))
  width=base.FONT.text_length(node.text or '',fontsize=size)
  left=x-width/2 if node.get('text-anchor')=='middle' else x
  assert left>=0 and left+width<=480 and y-size>=0 and y+size*.25<=235,(ident,node.text,'core detail bounds')
 return ET.tostring(root,encoding='unicode')


def plate(method,kind,stages,family_number,theme,core_svg):
 name,icon=theme
 children=''.join(ET.tostring(child,encoding='unicode') for child in ET.fromstring(core_svg)
                  if child.tag not in (NS+'title',NS+'desc'))
 rx,ry,rw,rh=focus(kind)
 main_scale=2.3;mx,my=48,214
 # The detail window is a true crop of the same vector geometry.
 bx,by,bw,bh=60,820,425,282
 zoom=min((bw-24)/rw,(bh-24)/rh)
 tx=bx+(bw-rw*zoom)/2-rx*zoom;ty=by+(bh-rh*zoom)/2-ry*zoom
 result=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1500" viewBox="0 0 1200 1500">',
  f'<title>{escape(method["id"]+" — "+method["method"]+" / enhanced thematic plate")}</title>',
  '<desc>'+escape(method['how_it_works']+' Original finding: '+method['finding'])+'</desc>',
  '<rect width="1200" height="1500" fill="white"/>',
  f'<defs><clipPath id="focus-{method["id"]}"><rect x="{bx+1}" y="{by+1}" width="{bw-2}" height="{bh-2}"/></clipPath></defs>',
  line(48,38,1152,38,3,'#151515'),text(49,70,f'{family_number:02d}  /  {name}',18,True,'#555555'),
  f'<g transform="translate(1050 55) scale(.88)">{motif(icon)}</g>',
  text(49,109,method['id'],26,True),
 ]
 title,last=paragraph(49,151,method['method'],950,31,1.21,bold=True)
 result.append(title)
 assert last<230,(method['id'],'title overlaps drawing')
 result.append(f'<g transform="translate({mx} {my}) scale({main_scale})">{children}</g>')
 result.append(rect(mx+rx*main_scale,my+ry*main_scale,rw*main_scale,rh*main_scale,'none','#666666',1.5,'7 7'))
 result.append(text(mx+rx*main_scale-9,my+ry*main_scale-10,'D',17,True,'#555555'))
 for i,x in enumerate((80,240,400),1):result.append(text(mx+x*main_scale,my+188*main_scale,f'0{i}',16,True,'#666666','middle'))
 result.extend([line(48,757,1152,757,1,'#bcbcbc'),text(60,792,'D / OPERATION DETAIL',18,True,'#555555'),rect(bx,by,bw,bh,'white','#777777',1),
  f'<g clip-path="url(#focus-{method["id"]})"><g transform="translate({tx:g} {ty:g}) scale({zoom:g})">{children}</g></g>',
  text(bx,1128,f'Vector detail / {zoom/main_scale:.2f}× main-view scale',16,False,'#777777'),
  text(550,792,'HOW THE OPERATION WORKS',18,True,'#555555')])
 value,end=paragraph(550,835,method['how_it_works'],598,21,1.35)
 result.append(value)
 result.append(text(550,end+26,'READ THE THREE STAGES',17,True,'#666666'))
 y=end+55
 for i,stage in enumerate(stages,1):
  result.append(text(550,y,f'{i:02d}',18,True,'#666666'))
  value,next_y=paragraph(600,y,stage,545,20,1.2)
  result.append(value);y=next_y+6
 assert y<1136,(method['id'],'mechanism explanation too long')
 result.extend([line(48,1162,1152,1162,1,'#bcbcbc'),text(60,1195,'WHAT WAS ACTUALLY DONE',17,True,'#555555')])
 value,end=paragraph(60,1228,method['what_is_actually_done'],1080,20,1.37)
 result.append(value)
 result.append(text(60,1328,'ORIGINAL FINDING / '+method['evidence'].upper(),17,True,'#555555'))
 value,end=paragraph(60,1360,method['finding'],1080,20,1.37)
 result.append(value)
 assert end<1441,(method['id'],'finding exceeds plate')
 result.extend([line(48,1451,1152,1451,.8,'#cccccc'),text(49,1478,'METHODS, DRAWN / ENHANCED THEMATIC EDITION',14,True,'#666666'),
  text(1150,1478,'SCHEMATIC • '+', '.join(method.get('source_ids',[])),14,False,'#666666','end'),'</svg>'])
 return ''.join(result),{'focus_rect_source_units':[rx,ry,rw,rh],'detail_relative_scale':zoom/main_scale,'theme':name,'family_number':family_number}


def fonts(page):base.fonts(page)
def put(page,*args,**kwargs):base.put(page,*args,**kwargs)


def main():
 payload=json.loads(base.SOURCE.read_text());methods=payload['methods']
 groups=list(dict.fromkeys(method['category'] for method in methods))
 specs={line.split('\t')[0]:(line.split('\t')[1],line.split('\t')[2:]) for line in (base.ROOT/'diagram_specs.tsv').read_text().splitlines() if line.strip()}
 documents={};records=[]
 for index,method in enumerate(methods):
  kind,stages=specs[method['id']];family=groups.index(method['category'])
  core=enrich_core(method,kind,base.sketch(method,kind,stages))
  svg,details=plate(method,kind,stages,family+1,THEMES[family],core)
  path=ROOT/'svg'/(method['id']+'-enhanced.svg');path.write_text(svg)
  pdf_path=ROOT/'vector'/(method['id']+'-enhanced.pdf')
  svg_to_pdf(svg,pdf_path)
  document=fitz.open(pdf_path);documents[method['id']]=document
  document[0].get_pixmap(matrix=fitz.Matrix(4,4),alpha=False).save(ROOT/'png'/(method['id']+'-enhanced.png'))
  records.append({**method,**details,'diagram_kind':kind,'visual_stages':stages,
                  'svg_file':'svg/'+path.name,'png_file':'png/'+method['id']+'-enhanced.png',
                  'svg_sha256':hashlib.sha256(svg.encode()).hexdigest()})
  if (index+1)%50==0:print(f'Enhanced and rasterized {index+1}/225 methods',flush=True)
 atlas=fitz.open();toc=[]
 page=atlas.new_page(width=600,height=750);fonts(page)
 put(page,35,62,'METHODS,',40,True);put(page,35,111,'DRAWN.',40,True)
 put(page,37,150,'ENHANCED THEMATIC EDITION',13,True,color=(.4,.4,.4))
 base.text_block(page,37,188,'225 mechanism plates / 14 visual families / enlarged vector details',515,13)
 for ident,region in [('M022',fitz.Rect(25,245,290,575)),('M202',fitz.Rect(307,245,572,575))]:page.show_pdf_page(region,documents[ident],0)
 base.text_block(page,37,618,'A closer view of each operation, with its mechanism, execution record, and original finding. Line hierarchy, grayscale, family motifs, and matched detail windows keep the visual language consistent.',525,11)
 put(page,37,722,'Vector PDF + editable SVG + high-resolution PNG',10,color=(.4,.4,.4))
 toc.append([1,'Enhanced visual guide',1])
 page=atlas.new_page(width=600,height=750);fonts(page)
 put(page,33,53,'THEMATIC INDEX',24,True)
 put(page,34,79,'Each family has its own motif and operator vocabulary.',10,color=(.4,.4,.4))
 index_info=[]
 for family,category in enumerate(groups):
  y=115+family*42
  icon_svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">{motif(THEMES[family][1])}</svg>'
  icon_source=fitz.open(stream=icon_svg.encode(),filetype='svg')
  icon_doc=fitz.open(stream=icon_source.convert_to_pdf(),filetype='pdf')
  page.show_pdf_page(fitz.Rect(31,y-15,61,y+15),icon_doc,0)
  put(page,74,y-2,f'{family+1:02d} / {THEMES[family][0]}',9,True)
  base.text_block(page,74,y+12,category,466,7.6)
  index_info.append((category,y))
 for method,record in zip(methods,records):
  ident=method['id'];page=atlas.new_page(width=600,height=750)
  page.show_pdf_page(page.rect,documents[ident],0)
  record['atlas_page']=len(atlas)
  if not any(row[1]==method['category'] for row in toc):toc.append([1,method['category'],len(atlas)])
  toc.append([2,ident+' / '+method['method'],len(atlas)])
 # Clickable category entries on the index page.
 for category,y in index_info:
  first=next(record['atlas_page'] for record in records if record['category']==category)
  atlas[1].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(25,y-19,577,y+23),'page':first-1})
 atlas.set_toc(toc)
 atlas.set_metadata({'title':'Methods, Drawn — Enhanced Thematic Edition','subject':'225 source-linked monochrome mechanism plates with enlarged vector details'})
 atlas_path=ROOT/'METHODS_DRAWN_ENHANCED.pdf';atlas.save(atlas_path,garbage=4,deflate=True)
 preview_ids=['M022','M038','M059','M088','M108','M134','M153','M202','M223']
 preview=fitz.open();page=preview.new_page(width=1800,height=2360);fonts(page)
 put(page,30,51,'METHODS, DRAWN / ENHANCED',31,True)
 put(page,31,81,'Closer mechanisms, enlarged detail windows, and family-specific monochrome themes',14,color=(.4,.4,.4))
 for i,ident in enumerate(preview_ids):
  x=25+(i%3)*593;y=110+(i//3)*744
  page.draw_rect(fitz.Rect(x,y,x+575,y+720),color=(.82,.82,.82),width=.8)
  page.show_pdf_page(fitz.Rect(x+5,y+5,x+570,y+715),documents[ident],0)
 preview.save(ROOT/'ENHANCED_PREVIEW.pdf',garbage=4,deflate=True)
 page.get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(ROOT/'ENHANCED_PREVIEW_5400px.png')
 for ident in ['M022','M038','M202']:
  documents[ident][0].get_pixmap(matrix=fitz.Matrix(6,6),alpha=False).save(ROOT/(ident+'-DETAIL_3600px.png'))
 output={'edition':'Enhanced thematic edition','method_count':len(records),'themes':[dict(number=i+1,name=t[0],motif=t[1]) for i,t in enumerate(THEMES)],
         'source':str(base.SOURCE),'source_sha256':hashlib.sha256(base.SOURCE.read_bytes()).hexdigest(),
         'atlas_pages':len(atlas),'svg_plate_size':[1200,1500],'png_size':[2400,3000],'preview_width_px':5400,'methods':records}
 (ROOT/'manifest.json').write_text(json.dumps(output,indent=2)+'\n')
 # Validate all plates, retained findings, narrative blocks, and native label bounds.
 whole=' '.join(p.get_text() for p in fitz.open(atlas_path));normalize=lambda value:re.sub(r'\s+',' ',unicodedata.normalize('NFKC',value)).strip()
 all_text=normalize(whole)
 for method,record in zip(methods,records):
  for field in ['id','finding','how_it_works','what_is_actually_done']:
   assert normalize(method[field]) in all_text,(method['id'],field,'missing from PDF')
  for node in ET.parse(ROOT/record['svg_file']).getroot():
   if node.tag!=NS+'text':continue
   x,y,size=[float(node.get(attribute)) for attribute in ('x','y','font-size')]
   font=base.BOLD if node.get('font-weight')=='bold' else base.FONT
   width=font.text_length(node.text or '',fontsize=size)
   anchor=node.get('text-anchor','start')
   left=x-width/2 if anchor=='middle' else x-width if anchor=='end' else x
   assert left>=0 and left+width<=1200 and y-size>=0 and y+size*.25<=1500,(method['id'],node.text,'plate label bounds')
 validation={'methods':225,'svg_files':len(list((ROOT/'svg').glob('*.svg'))),'png_files':len(list((ROOT/'png').glob('*.png'))),
             'atlas_pages':len(atlas),'themes':14,'all_source_narratives_and_findings_retained':True,'all_plates_rendered':True}
 (ROOT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
 (ROOT/'README.md').write_text('# Enhanced thematic edition\n\n225 detailed vector plates, 14 semantic family motifs, enlarged detail insets, full source mechanisms and execution descriptions, and original findings.\n\n- METHODS_DRAWN_ENHANCED.pdf: complete illustrated atlas.\n- ENHANCED_PREVIEW_5400px.png: nine-plate high-resolution contact sheet.\n- svg/: editable 1200 × 1500 vector plates.\n- png/: 2400 × 3000 raster exports.\n- M022 / M038 / M202 DETAIL images: 3600 × 4500 close-reading exports.\n- manifest.json: source records, theme assignments, detail crops, hashes, and page references.\n\nDetail windows magnify the same source geometry; schematic examples remain illustrative. Original findings are retained. The first edition is preserved in the parent directory.\n')
 with zipfile.ZipFile(ROOT/'ENHANCED_SVG_AND_PNG.zip','w',zipfile.ZIP_DEFLATED) as bundle:
  for directory in ['svg','png']:
   for path in sorted((ROOT/directory).glob('*')):bundle.write(path,path.relative_to(ROOT))
  for name in ['README.md','manifest.json','validation.json']:bundle.write(ROOT/name,name)
 print(json.dumps({'atlas':str(atlas_path),'preview':str(ROOT/'ENHANCED_PREVIEW_5400px.png'),**validation},indent=2))


if __name__=='__main__':main()
