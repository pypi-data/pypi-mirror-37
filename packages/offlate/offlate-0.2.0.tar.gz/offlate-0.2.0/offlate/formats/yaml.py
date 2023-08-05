""" The Yaml format. """

from ruamel import yaml
from .entry import YAMLEntry

def yaml_rec_load(path, source, dest):
    ans = []
    for s in source:
        path2 = list(path)
        path2.append(s)
        if isinstance(source[s], str):
            ans.append({'path': path, 'id': s,
                'source_string': str(source[s]),
                'translation': str(dest[s])})
        else:
            ans.extend(yaml_rec_load(path2, source[s], dest[s]))
    return ans

def yaml_rec_update(callback, source, old, new):
    ans = {}
    for i in new:
        o = ''
        s = ''
        n = new[i]
        try:
            s = source[i]
        except Exception:
            pass
        try:
            o = old[i]
        except Exception:
            pass
        if isinstance(n, str):
            if o == '':
                ans[i] = n
            elif n == '':
                ans[i] = o
            else:
                ans[i] = callback(s, o, n)
        else:
            ans[i] = yaml_rec_update(callback, s, o, n)
    return ans

class YamlFormat:
    def __init__(self, conf):
        self.conf = conf
        self.source = conf['source']
        self.dest = conf['dest']
        with open(self.source, 'rb') as sf:
            with open(self.dest, 'rb') as df:
                source = yaml.safe_load(sf)
                dest = yaml.safe_load(df)
                # TODO: check that Yaml files always are rooted with the language name
                lang1 = list(source.keys())[0]
                lang2 = list(dest.keys())[0]
                self.contents = yaml_rec_load([lang2], source[lang1], dest[lang2])

    def content(self):
        return [YAMLEntry(x) for x in self.contents]

    def save(self):
        data = {}
        for d in self.contents:
            path = d['path']
            curr = data
            for p in path:
                if p in curr:
                    curr = curr[p]
                else:
                    curr[p] = {}
                    curr = curr[p]
            curr[d['id']] = str(d['translation'])
        with open(self.dest, 'wb') as f:
            f.write(yaml.dump(data, allow_unicode=True, Dumper=yaml.RoundTripDumper).encode('utf8'))

    def merge(self, older, callback):
        with open(older.dest, 'rb') as oldf:
            with open(self.dest, 'rb') as newf:
                with open(self.source, 'rb') as sourcef:
                    old = yaml.safe_load(oldf)
                    new = yaml.safe_load(newf)
                    source = yaml.safe_load(sourcef)
                    merged = yaml_rec_update(callback, source, old, new)
                    with open(self.dest, 'wb') as f:
                        f.write(yaml.dump(merged, allow_unicode=True, Dumper=yaml.RoundTripDumper).encode('utf8'))
