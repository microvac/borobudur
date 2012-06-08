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

