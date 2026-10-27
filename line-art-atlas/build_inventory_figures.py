#!/usr/bin/env python3
"""Build a distinct, annotated landscape mechanism plate for every inventory method."""
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re

import build_line_art as base

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / 'inventory-svg'
SHEET = '#f9faf7'
INK = '#123833'
TEAL = '#0d5c57'
MUTED = '#657a72'
ORANGE = '#e06129'

# These newer method entries did not exist when the original 225-plate atlas was
# made. Each gets a mechanism-appropriate visual kind and unique stage labels.
NEW = {
    'M103': ('bitgrid', ['firmware register state', 'Yasmarang positions', 'affected output bytes']),
    'M104': ('coupled', ['cold-boot inputs', 'mixer and skip paths', 'post-hash comparison']),
    'M105': ('derive', ['sanitized initial state', 'wallet generation replay', 'derived example keys']),
    'M106': ('bloom', ['funded-address list', 'read-only membership', 'exact address status']),
    'M107': ('clock', ['dated UTXO snapshots', 'drain-wave sequence', 'remaining outputs']),
    'M108': ('graph', ['pre-drain inputs', 'co-input clustering', 'later sweep comparison']),
    'M109': ('cross', ['UID / tick / skip grid', 'wallet path derivation', 'funded-dump comparison']),
    'M110': ('hashchain', ['Yasmarang state', 'BIP-39 / BIP-32 path', 'address encoding']),
    'M111': ('benchmark', ['register variations', '65,536 output window', 'collision / bit statistics']),
    'M112': ('gridmax', ['ten generator models', 'unknown-target matrix', 'exact identity checks']),
    'M113': ('lfsr', ['LCG-compatible states', 'masked word packing', 'tier survivor count']),
    'M114': ('prng', ['Lehmer multipliers', 'word order / packing', 'target HASH160']),
    'M115': ('mask', ['SplitMix64 draws', 'masked sequence layout', 'target hash check']),
    'M116': ('sequence', ['lagged state words', '16 / 32 / 64-bit layouts', 'recurrence consistency']),
    'M117': ('glv', ['half-generator relation', 'cross-curve coordinates', 'DLP implication check']),
    'M118': ('null', ['64 declared features', '3,000 matched controls', 'family maximum']),
    'M119': ('regression', ['low-bit observations', 'affine / linear models', 'held-out rejection']),
    'M120': ('table', ['77 unknown tiers', 'public constraints', 'unresolved coordinates']),
    'M121': ('holdout', ['index-offset model', 'held-out tiers', 'coefficient bounds']),
}


def esc(value):
    return html.escape(str(value), quote=True)


def lines(value, max_width, size, max_lines=2):
    result = base.wrap(str(value), max_width, size, base.FONT)
    if len(result) > max_lines:
        result = result[:max_lines]
        tail = result[-1]
        while tail and base.FONT.text_length(tail+'…',fontsize=size)>max_width:
            tail = tail[:-1]
        result[-1] = tail.rstrip()+'…'
    return result


def text(x, y, value, size=18, color=INK, weight='normal'):
    return (f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{esc(value)}</text>')


def mechanism_core(method, old):
    if old:
        raw = (HERE / old['svg_file']).read_text()
        kind, stages = old['diagram_kind'], old['visual_stages']
    else:
        kind, stages = NEW[method['id']]
        raw = base.sketch(method, kind, stages)
    match = re.search(r'(<g stroke-linecap=.*</g>)', raw, re.DOTALL)
    if not match:
        raise ValueError(f"Missing drawing group for {method['id']}")
    core = match.group(1)
    for before, after in [('fill="white"', f'fill="{SHEET}"'),
                          ('#151515', INK), ('#777777', MUTED),
                          ('#c5c5c5', '#c0cec3'), ('#ededed', '#e7eee8')]:
        core = core.replace(before, after)
    return kind, stages, core


def plate(method, kind, stages, core):
    result = [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="370" viewBox="0 0 960 370">',
              f'<title>{esc(method["id"]+" — "+method["method"]+" / mechanism plate")}</title>',
              f'<desc>{esc(method["how_it_works"]+" Finding: "+method["finding"])}</desc>',
              f'<rect width="960" height="370" fill="{SHEET}"/>',
              f'<path d="M24 30 H596" stroke="#c0cec3" stroke-width="1"/>',
              text(25,22,'OPERATIONAL MECHANISM',13,MUTED,'bold'),
              f'<g transform="translate(17 36) scale(1.2)">{core}</g>',
              f'<path d="M615 34 V327" stroke="#c0cec3" stroke-width="1"/>',
              text(638,54,'READ THE PLATE',13,TEAL,'bold')]
    detail=(method['inputs_needed'],method['what_is_actually_done'],method['finding'])
    for i,(stage,tag,body) in enumerate(zip(stages,('INPUT','OPERATION','READOUT'),detail)):
        y = 83+i*89
        result.append(f'<circle cx="648" cy="{y}" r="5" fill="{ORANGE}"/>')
        if i<2:
            result.append(f'<path d="M648 {y+7} V{y+82}" stroke="{ORANGE}" stroke-width="1.3"/>')
        result.append(text(668,y-9,f'0{i+1} / {tag}',11.5,TEAL,'bold'))
        result.append(text(668,y+11,stage,16.2,INK,'bold'))
        for j,line in enumerate(lines(body,265,14.2,2)):
            result.append(text(668,y+34+j*18,line,14.2,MUTED))
        if i<2:
            result.append(f'<path d="M668 {y+68} H938" stroke="#d7e0d7" stroke-width="1"/>')
    result.append('</svg>')
    return ''.join(result)


def main():
    methods = json.loads((ROOT/'methods-explained.json').read_text())['methods']
    legacy = {row['method']:row for row in json.loads((HERE/'diagram_manifest.json').read_text())['methods']}
    OUT.mkdir(exist_ok=True)
    entries=[]
    labels=[]
    hashes=[]
    for method in methods:
        old=legacy.get(method['method'])
        kind,stages,core=mechanism_core(method,old)
        svg=plate(method,kind,stages,core)
        path=OUT/(method['id']+'.svg')
        path.write_text(svg)
        digest=hashlib.sha256(svg.encode()).hexdigest()
        hashes.append(digest)
        labels.append(tuple(stages))
        entries.append({'id':method['id'],'method':method['method'],'kind':kind,
                        'stages':stages,'svg_file':str(path.relative_to(HERE)),
                        'sha256':digest,'legacy':bool(old)})
    if len(set(hashes))!=len(methods) or len(set(labels))!=len(methods):
        raise ValueError('A repeated mechanism plate or visible stage triplet was generated')
    counts=Counter(row['kind'] for row in entries)
    (OUT/'manifest.json').write_text(json.dumps({'count':len(entries),'kind_counts':counts,
                                                   'methods':entries},indent=2)+'\n')
    print(json.dumps({'figures':len(entries),'unique_svg':len(set(hashes)),
                      'unique_stage_triplets':len(set(labels)),'kinds':len(counts)}))


if __name__=='__main__':
    main()
