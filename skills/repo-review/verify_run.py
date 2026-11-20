import json, re, sys, os
run, root = sys.argv[1], sys.argv[2]
d = json.load(open(run)); bad = 0
for q in d['questions']:
    for x in q['quotes']:
        src = x['source']
        m = re.match(r'([\w./-]+)(?::(\d+)|,?\s+lines?\s+(\d+))?', src)
        name = m.group(1) if m else ''
        path = os.path.join(root, name)
        if not name or not os.path.isfile(path):
            if '.' in name or '/' in name: print(f"{q['short']}: MISSING FILE {name}"); bad += 1
            else: print(f"{q['short']}: not a file quote, skipped ({src[:40]})")
            continue
        ln = m.group(2) or m.group(3)
        if not ln and re.search(r'\blines?\b', src, re.I):
            print(f"{q['short']}: line number in an unreadable form ({src[:40]})"); bad += 1; continue
        text = open(path, encoding='utf-8').read()
        if x['text'] not in text: print(f"{q['short']}: NOT VERBATIM in {name}"); bad += 1; continue
        if ln:
            ln = int(ln); lines = text.splitlines()
            if ln > len(lines) or (x['text'] not in lines[ln-1] and x['text'].splitlines()[0] not in lines[ln-1]):
                print(f"{q['short']}: not on line {ln} of {name}"); bad += 1; continue
        print(f"{q['short']}: ok ({name}{', line '+str(ln) if ln else ''})")
print('problems:', bad)
