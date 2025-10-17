import re

class LrgParser:
    def parse(self, text: str):
        tokens = []
        if not text:
            return tokens

        if text.startswith('{'):
            if '}' in text:
                section = text[1:text.find('}')]
                parts = section.split(',')
                for p in parts:
                    if ':' in p:
                        k, v = p.split(':', 1)
                        tokens.append((k.strip(), v.strip()))
                    else:
                        tokens.append((p.strip(), None))
            else:
                raise ValueError('bad format')
        elif text.startswith('['):
            inner = text[1:-1]
            elems = inner.split(';')
            for e in elems:
                if e == '':
                    continue
                if '=' in e:
                    k, v = e.split('=', 1)
                    if v.isdigit():
                        tokens.append((k, int(v)))
                    else:
                        if v.lower() in ('true', 'false'):
                            tokens.append((k, v.lower() == 'true'))
                        else:
                            tokens.append((k, v))
                else:
                    tokens.append((e, None))
        else:
            matches = re.findall(r"(\\w+):(\\w+)", text)
            for m in matches:
                tokens.append(m)

        result = []
        for t in tokens:
            if t[1] is None:
                if t[0].isdigit():
                    result.append(int(t[0]))
                else:
                    result.append(t[0])
            else:
                result.append({t[0]: t[1]})

        return result

    def heavy_method(self, lines: list):
        out = []
        for ln in lines:
            if ln is None:
                continue
            s = ln.strip()
            if s == '':
                continue
            if s.startswith('#'):
                continue
            if '=>' in s:
                a, b = s.split('=>', 1)
                a = a.strip()
                b = b.strip()
                if '|' in b:
                    for part in b.split('|'):
                        if ':' in part:
                            k, v = part.split(':', 1)
                            out.append((a, k, v))
                        else:
                            out.append((a, part))
                else:
                    if b.isdigit():
                        out.append((a, int(b)))
                    else:
                        out.append((a, b))
            else:
                if ':' in s:
                    k, v = s.split(':', 1)
                    out.append((k.strip(), v.strip()))
                else:
                    out.append(s)
        return out
