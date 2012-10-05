"""
    this module performs topological sort on dependency graphs and groups result in sorted list of ordered sets

    i.e. magic

    e.g.

    given partial order A->B and A->C
    the possible topological sort are [A, B, C] and [A, C, B]
    the result will be [{A}, {B, C}]

"""
__all__ =["count"]

import itertools

def make_dependencies(available_modules):
    """
    convert available_modules to simple dict of dependencies, result will look like:
    {
        "time": set(),
        "datetime": set("time"),
        "math": set(),
        "colander: set("datetime", "time")
    }
    """
    modules = available_modules.values()
    results = {}
    availables = set(available_modules.keys())
    for m in modules:
        key = m.modname
        deps = set()
        for dep in m.dependencies:
            if dep in availables:
                deps.add(dep)
        results[key] = deps
    return results

def get_dependencies(module_names, available_modules):
    """
    create list of all dependencies, e.g.
    ["math", "time", "datetime"]
    """
    results = set()
    stack = []
    stack.extend(module_names)
    visited = set()
    while len(stack):
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        results.add(current)
        if current in available_modules :
            stack.extend(available_modules[current].dependencies)

    return results

def toposort(data):
    """
    return input that is sort topologically
    """
    for k, v in data.items():
        v.discard(k) # Ignore self dependencies
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item,dep in data.items() if not dep)
        if not ordered:
            break
        for item in ordered:
            yield item
        data = {item: (dep - ordered) for item,dep in data.items()
                if item not in ordered}
    assert not data, "A cyclic dependency exists amongst %r" % data

class Pack(object):

    def __init__(self, id, target_names):
        self.id = id
        self.items = []
        self.target_names = tuple(sorted(target_names))

    def append(self, item):
        self.items.append(item)

    def __repr__(self):
        return "\n%d %s -> %s\n" % (self.id, self.target_names, self.items)

class Bundler(object):

    def __init__(self, target_names):
        self.counter = itertools.count()

        self.last_required = set(target_names)
        self.last_pack = Pack(next(self.counter), set(target_names))
        self.packs = {}
        self.all_packs = [self.last_pack]
        for target_name in target_names:
            self.packs[target_name] = [self.last_pack]

    def append(self, modname, target_names):
        if target_names == self.last_required:
            self.last_pack.append(modname)
        else:
            self.last_pack = Pack(next(self.counter), target_names)
            self.last_pack.append(modname)
            self.last_required = target_names

            for target_name in target_names:
                self.packs[target_name].append(self.last_pack)
            self.all_packs.append(self.last_pack)

    def compact(self):
        for i in range(len(self.all_packs) -1 , -1, -1):
            if not self.all_packs[i].items:
                del self.all_packs[i]
        for name in self.packs:
            for i in range(len(self.packs[name])-1, -1, -1):
                if not self.packs[name][i].items:
                    del self.packs[name][i]


def merge_pack(source, target, modules_in_between, simple):
    """
    merge packs with same targets if doesn't dependant to modules in between
    """
    modules_in_between = set(modules_in_between)
    new_source_items = []
    for item in source.items:
        dependent_to_something_in_between = simple[item].intersection(modules_in_between)
        if dependent_to_something_in_between:
            new_source_items.append(item)
            modules_in_between.add(item)
        else:
            target.items.append(item)
    source.items = new_source_items

def count(targets, available_modules):
    all_dependencies = make_dependencies(available_modules)
    sorted_module_names = list(toposort(all_dependencies))

    dependencies = {}
    for name in targets:
        dependencies[name] = get_dependencies(targets[name], available_modules)

    bundler = Bundler(targets.keys())

    for module_name in sorted_module_names:
        required_in = set()
        for name in dependencies:
            if module_name in dependencies[name]:
                required_in.add(name)
        if required_in:
            bundler.append(module_name, required_in)

    last_packs = {}
    for i,pack in enumerate(bundler.all_packs):
        if pack.target_names in last_packs:
            last_i, last_pack = last_packs[pack.target_names]
            modules_in_between = set()
            for j in range(last_i+1, i):
                for module in bundler.all_packs[j].items:
                    modules_in_between.add(module)
            merge_pack(pack, last_pack, modules_in_between, all_dependencies)
        if pack.target_names in last_packs and len(pack.items) == 0:
            continue
        last_packs[pack.target_names] = (i, pack)
    bundler.compact()

    return bundler

