import json, re, os
from collections import Counter

GT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'anonymous-submission', 'dataset', 'groundtruth')
MANIFEST = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'anonymous-submission', 'dashboard', 'public', 'manifest.json')
OUT_DIR = os.path.dirname(__file__)

with open(MANIFEST) as f:
    manifest = json.load(f)
pie_ids = [item['id'] for item in manifest if item.get('figure_type') == 'Pie Chart']
print(f'Found {len(pie_ids)} pie charts')

def get_longest_english_annotation(gt):
    ea = [a for a in gt.get('annotations', []) if a.get('annotation_language') == 'English']
    if not ea:
        ea = gt.get('annotations', [])
    if not ea:
        return ''
    return max(ea, key=lambda a: len(a.get('annotation', ''))).get('annotation', '')

def audit(text):
    tl = text.lower()
    ck = {}
    iss = []

    # PURPOSE
    pk = ['compar', 'distribution', 'proportion', 'breakdown', 'composition',
          'shows', 'represents', 'illustrat', 'depicts', 'displays',
          'features', 'percentage', 'share', 'allocation', 'purpose']
    hp = any(k in tl for k in pk)
    if hp and len(text) > 50:
        ck['purpose'] = 'present'
    elif hp:
        ck['purpose'] = 'partial'
        iss.append('Purpose statement is vague or too brief')
    else:
        ck['purpose'] = 'missing'
        iss.append('No clear statement of chart purpose')

    # SLICE_COUNT
    scp = [r'(\d+)\s*slices', r'(\d+)\s*segments', r'(\d+)\s*sections',
           r'(\d+)\s*categories', r'(\d+)\s*portions', r'(\d+)\s*parts',
           r'(\d+)\s*pieces', r'divided\s*into\s*(\d+)',
           r'consists?\s*of\s*(\d+)', r'contains?\s*(\d+)\s*(?:slices|segments|sections|categories)',
           r'composed\s*of\s*(\d+)', r'includes?\s*(\d+)\s*(?:slices|segments|sections)']
    hsc = any(re.search(p, tl) for p in scp)
    ck['slice_count'] = 'present' if hsc else 'missing'
    if not hsc:
        iss.append('Total number of slices not explicitly stated')

    # SLICE_DETAILS
    pm = re.findall(r'\d+\.?\d*\s*%', text)
    color_kw = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink',
                'brown', 'gray', 'grey', 'black', 'white', 'teal', 'cyan',
                'magenta', 'light blue', 'dark blue', 'light green', 'dark green',
                'sky blue', 'navy', 'gold', 'beige', 'coral', 'maroon', 'olive',
                'violet', 'indigo', 'turquoise', 'lime', 'salmon', 'crimson',
                'color-coded', 'colour']
    hc = any(k in tl for k in color_kw)
    lm = re.findall(r'"[^"]+?"', text)
    if len(pm) >= 2 and hc and len(lm) >= 2:
        ck['slice_details'] = 'present'
    elif len(pm) >= 1 or (hc and len(lm) >= 1):
        ck['slice_details'] = 'partial'
        if len(pm) < 2:
            iss.append('Few percentage values provided for slices')
        if not hc:
            iss.append('Slice colors not described')
        if len(lm) < 2:
            iss.append('Few slice labels identified')
    else:
        ck['slice_details'] = 'missing'
        iss.append('Slice details (label, color, percentage) not provided')

    # LEGEND
    lk = ['legend', 'color key']
    hl = any(k in tl for k in lk)
    ck['legend'] = 'present' if hl else 'missing'
    if not hl:
        iss.append('Legend presence/absence not mentioned')

    # LABEL_PLACEMENT
    plk = ['inside', 'outside', 'within the', 'on the slices', 'adjacent',
           'next to', 'labeled on', 'labeled inside', 'labeled outside',
           'labels are placed', 'label placement', 'marked on', 'annotated',
           'labeled partially inside', 'labels inside', 'percentages are marked',
           'percentages are shown', 'percentages are displayed', 'labeled in']
    hp2 = any(k in tl for k in plk)
    ck['label_placement'] = 'present' if hp2 else 'missing'
    if not hp2:
        iss.append('Label/percentage placement not described')

    # VISUAL_EMPHASIS
    ek = ['exploded', 'offset', 'bold', 'highlight', 'emphasized',
          'separated', 'pulled out', 'stand out', 'emphasis',
          'prominent', 'larger font', 'no visual emphasis',
          'no emphasis', 'proportional representation',
          'no particular emphasis', 'not emphasized', '3d',
          'three-dimensional', 'shadow', 'gradient', 'no special emphasis']
    he = any(k in tl for k in ek)
    ck['visual_emphasis'] = 'present' if he else 'missing'
    if not he:
        iss.append('Visual emphasis (or lack thereof) not noted')

    # ORDERING
    ok2 = ['descending', 'ascending', 'clockwise', 'counterclockwise',
           'counter-clockwise', 'largest to smallest', 'smallest to largest',
           'order', 'arranged', 'sorted', 'no particular order',
           'no specific order', 'sequential', 'alphabetical']
    ho = any(k in tl for k in ok2)
    ck['ordering'] = 'present' if ho else 'missing'
    if not ho:
        iss.append('Slice ordering not described')

    # VALUES_CORRECT
    if len(pm) >= 2:
        pv = []
        for m in pm:
            try:
                pv.append(float(m.replace('%', '').strip()))
            except:
                pass
        if pv:
            t = sum(pv)
            r2 = t % 100
            ck['values_correct'] = 'present'
            if not (r2 < 15 or r2 > 85 or (95 <= t <= 105)):
                iss.append('Percentage values sum to %.1f%%, possibly erroneous' % t)
        else:
            ck['values_correct'] = 'missing'
            iss.append('No parseable percentage values found')
    elif len(pm) == 1:
        ck['values_correct'] = 'partial'
        iss.append('Only one percentage value provided')
    else:
        rn = re.findall(r'\(\s*\d+\.?\d*\s*\)', text)
        if len(rn) >= 2:
            ck['values_correct'] = 'partial'
            iss.append('Values given as raw numbers without % symbol')
        else:
            ck['values_correct'] = 'missing'
            iss.append('No specific values or percentages provided')

    # CLARITY
    ss = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 10]
    if len(text) > 100 and len(ss) >= 2:
        bp = [r'\.\s*\.', r',\s*,', r'\(\s*\)']
        hb = any(re.search(p, text) for p in bp)
        if hb:
            ck['clarity'] = 'partial'
            iss.append('Text contains formatting artifacts or broken patterns')
        else:
            ck['clarity'] = 'present'
    elif len(text) > 50:
        ck['clarity'] = 'partial'
        iss.append('Annotation is relatively short for a pie chart description')
    else:
        ck['clarity'] = 'missing'
        iss.append('Annotation too short to be a meaningful description')

    return ck, iss


results = []
for fid in sorted(pie_ids):
    gp = os.path.join(GT_DIR, fid + '.json')
    if not os.path.exists(gp):
        print(f'WARNING: {gp} not found')
        results.append({
            'figure_id': fid,
            'figure_type': 'Pie Chart',
            'checklist': {k: 'missing' for k in ['purpose', 'slice_count', 'slice_details',
                          'legend', 'label_placement', 'visual_emphasis',
                          'ordering', 'values_correct', 'clarity']},
            'issues': ['Ground truth file not found']
        })
        continue
    with open(gp) as f:
        gt = json.load(f)
    ann = get_longest_english_annotation(gt)
    if not ann:
        results.append({
            'figure_id': fid,
            'figure_type': 'Pie Chart',
            'checklist': {k: 'missing' for k in ['purpose', 'slice_count', 'slice_details',
                          'legend', 'label_placement', 'visual_emphasis',
                          'ordering', 'values_correct', 'clarity']},
            'issues': ['No English annotation found']
        })
        continue
    c, i = audit(ann)
    results.append({
        'figure_id': fid,
        'figure_type': 'Pie Chart',
        'checklist': c,
        'issues': i
    })

with open(os.path.join(OUT_DIR, 'audit.json'), 'w') as f:
    json.dump(results, f, indent=2)

ckeys = ['purpose', 'slice_count', 'slice_details', 'legend', 'label_placement',
         'visual_emphasis', 'ordering', 'values_correct', 'clarity']
summary = {'total_figures': len(results), 'checklist_counts': {}}
for key in ckeys:
    counts = {'present': 0, 'partial': 0, 'missing': 0}
    for r in results:
        v = r['checklist'].get(key, 'missing')
        counts[v] = counts.get(v, 0) + 1
    summary['checklist_counts'][key] = counts

ai = []
for r in results:
    ai.extend(r['issues'])
ic = Counter(ai)
summary['most_common_issues'] = [{'issue': k, 'count': v} for k, v in ic.most_common(20)]
summary['figures_by_issue_count'] = sorted(
    [{'figure_id': r['figure_id'], 'issue_count': len(r['issues'])} for r in results],
    key=lambda x: -x['issue_count']
)

with open(os.path.join(OUT_DIR, 'summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print('Processed %d pie charts' % len(results))
print()
for key in ckeys:
    c = summary['checklist_counts'][key]
    print('  %s: present=%d, partial=%d, missing=%d' % (key, c['present'], c.get('partial', 0), c['missing']))
print()
for item in summary['most_common_issues'][:10]:
    print('  [%d] %s' % (item['count'], item['issue']))
