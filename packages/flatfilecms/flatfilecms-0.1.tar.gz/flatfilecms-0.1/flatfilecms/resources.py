from pyramid.path import AssetResolver
from pathlib import PurePath


def flat(d, path):
    structure = []
    for k, v in d.items():
        if isinstance(v, dict):
            structure.extend(flat(v, f"{path}/{k}"))
        else:
            if k == 'index':
                structure.append(f"{path}/")
            else:
                structure.append(f"{path}/{k}")
    return structure


class Folder(dict):
    def __init__(self, name, parent, path):
        self.__path__ = path
        self.__name__ = name
        self.__parent__ = parent
        for entry in AssetResolver().resolve(path).listdir():
            asset = f"{path}/{entry}"
            if AssetResolver().resolve(asset).isdir():
                self.create_dir(asset)
            else:
                self.create_file(asset)

    def create_file(self, asset):
        path = PurePath(asset)
        if path.suffix == '.md':
            self[path.stem] = Markdown(path.stem, self, asset)
        elif path.suffix == '.yaml':
            self[path.stem] = YAML(path.stem, self, asset)
        elif path.suffix == '.j2' or path.suffix == '.jinja2':
            self[path.stem] = Jinja2(path.stem, self, asset)
        else:
            name = path.name
            # Если имя файла не index.html,
            # то отдавать по имени файла
            if name == 'index.html':
                name = 'index'
            self[name] = Document(name, self, asset)

    def create_dir(self, asset):
        path = PurePath(asset)
        self[path.name] = Folder(path.name, self, asset)

    def structure(self, base_dir=''):
        return flat(self, base_dir)


class Root(Folder):
    def __init__(self, path):
        super(Root, self).__init__('', None, path)


class Document(object):
    def __init__(self, name, parent, path):
        self.__name__ = name
        self.__parent__ = parent
        self.__path__ = path


class Markdown(Document):
    pass


class YAML(Document):
    pass


class Jinja2(Document):
    pass
