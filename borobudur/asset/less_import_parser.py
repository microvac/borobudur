import os, re


IMPORT = re.compile('''
    @import

    \s*

    (
        (?P<filename>
            '.*?(?!\\\\)'
        |
            ".*?(?!\\\\)"
        )
    |
        url\(
            (?P<url>
                .*?(?!\\\\)
            )
        \)
    )

    (
        \s*

        (?P<media>
            [a-z \s ,]*
        )
    )?

    \s*

    ;?
''', re.DOTALL | re.VERBOSE)

def parse_import(less):
    match = IMPORT.match(less)

    if not match:
        raise ValueError()

    code = match.group()

    media = [media.strip() for media in match.group('media').split(',')]

    media = tuple(media)

    if len(media) == 1 and media[0] == '':
        media = None

    filename = match.group('filename')

    if filename:
        # strip the quotation marks around the filename
        filename = filename[1:-1]
        yield filename

def parse(dir, file, cache):
    result =  os.path.join(dir, file)
    cache[result] = True
    yield result
    with open(os.path.join(dir, file)) as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            try:
                for item in parse_import(line):
                    full_path = os.path.join(dir, item)
                    child_dir = os.path.dirname(full_path)
                    filename = os.path.basename(full_path)
                    full_path = os.path.join(child_dir, filename)
                    if full_path not in cache:
                        for child_item in parse(child_dir, filename, cache):
                            yield child_item
            except ValueError:
                pass

def get_all_less(file):
    dir = os.path.dirname(file)
    file = os.path.basename(file)
    cache = {}
    for result in parse(dir, file, cache):
        yield result

def parse_modified_after(dir, file, cache, import_cache, modified):
    result =  os.path.join(dir, file)
    cache[result] = True

    if os.path.getmtime(result) > modified:
        if result in import_cache:
            del import_cache[result]
        return True

    if result in import_cache:
        children = import_cache[result]
        for full_path in children:
            child_dir = os.path.dirname(full_path)
            filename = os.path.basename(full_path)
            if full_path not in cache:
                if parse_modified_after(child_dir, filename, cache, import_cache, modified):
                    return True
    else:
        with open(os.path.join(dir, file)) as f:
            children = []
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                try:
                    for item in parse_import(line):
                        full_path = os.path.join(dir, item)
                        child_dir = os.path.dirname(full_path)
                        filename = os.path.basename(full_path)
                        full_path = os.path.join(child_dir, filename)
                        if full_path not in cache:
                            if parse_modified_after(child_dir, filename, cache, import_cache, modified):
                                return True
                            children.append(full_path)
                except ValueError:
                    pass
            import_cache[result] = children
    return False

def is_any_modified_after(file, import_cache, modified):
    dir = os.path.dirname(file)
    file = os.path.basename(file)
    cache = {}
    return parse_modified_after(dir, file, cache, import_cache, modified)
