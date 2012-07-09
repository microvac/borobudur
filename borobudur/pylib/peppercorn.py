def data_type(value):
    if ':' in value:
        parts = value.split(":")
        return [ parts[0].strip(), parts[1].strip() ]
    return ('', value.strip())

def next(iterator):
    idx = iterator["i"]
    idx += 1
    iterator["i"] = idx
    return iterator["list"][idx]

def iter(item):
    return {"i": -1, "list":item}

def partial(fn, arg):
    def part():
        return fn(arg)
    return part

START = '__start__'
END = '__end__'
SEQUENCE = 'sequence'
MAPPING = 'mapping'
RENAME = 'rename'

all_typs = (SEQUENCE, MAPPING, RENAME)

def stream(next_token_gen, token):
    """
    thanks to the effbot for
    http://effbot.org/zone/simple-iterator-parser.htm
    """
    op, data = token
    if op == START:
        name, typ = data_type(data)
        out = []

        if typ in all_typs:
            if typ == MAPPING:
                out = {}
                def add(x, y):
                    out[x]= y
            else:
                out = []
                add = lambda x, y: out.append(y)
            token = next_token_gen()
            op, data = token
            while op != END:
                key, val = stream(next_token_gen, token)
                add(key, val)
                token = next_token_gen()
                op, data = token
            if typ == RENAME:
                if out:
                    out = out[0]
                else:
                    out = ''
            return name, out
        else:
            raise ValueError('Unknown stream start marker %s' % token)
    else:
        return op, data

def parse(fields):
    """ Infer a data structure from the ordered set of fields and
    return it."""
    f = []
    f.append((START, MAPPING))
    f.extend(fields)
    f.append((END, ''))

    fields = f
    src = iter(fields)
    sr  = stream(partial(next, src), next(src))
    result = sr[1]
    return result
