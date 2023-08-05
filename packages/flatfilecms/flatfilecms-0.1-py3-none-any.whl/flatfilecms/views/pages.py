from pyramid.view import (
    view_config,
    render_view_to_response,
    )
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import (HTTPFound, HTTPNotFound)
from pyramid.response import FileResponse
from pyramid.path import AssetResolver
from pathlib import PurePath
from ..resources import (Folder, Document, Markdown, YAML, Jinja2)
import yaml
import frontmatter


class Loader(yaml.Loader):
    def __init__(self, stream):
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)

    def include(self, node):
        if isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            return [self.extractFile(filename)
                    for filename in self.construct_sequence(node)]

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k, v in self.construct_mapping(node).items():
                result[k] = self.extractFile(v)
            return result

        else:
            raise yaml.constructor.ConstructorError(
                    "Error:: unrecognised node type in !include statement")

    def extractFile(self, filename):
        path = PurePath(self.data_dir) / filename
        f = AssetResolver().resolve(str(path)).stream()
        if f:
            if path.suffix in ['.yaml', '.yml', '.json']:
                return yaml.load(f, Loader)
            return f.read().decode()


def LoaderFactory(data_dir):
    cl = Loader
    cl.data_dir = data_dir
    return cl


class CustomYAMLHandler(frontmatter.YAMLHandler):
    def __init__(self, data_dir):
        self.loader = LoaderFactory(data_dir)

    def load(self, fm, **kwargs):
        return yaml.load(fm, self.loader)


class PagesView:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Folder)
    def folder(self):
        if 'index' not in self.context:
            raise HTTPNotFound
        return render_view_to_response(self.context['index'], self.request)

    @view_config(context=Document)
    def document(self):
        return FileResponse(
                AssetResolver().resolve(self.context.__path__).abspath(),
                request=self.request)

    def process_yaml(self):
        if 'redirect' in self.post:
            return HTTPFound(location=self.post.redirect)
        if 'menu' not in self.post:
            self.post['menu'] = yaml.load(
                AssetResolver().resolve(
                    str(PurePath(self.request.registry.settings['data_dir']) /
                    'menu/default.yaml')).stream(),
                LoaderFactory(self.request.registry.settings['data_dir']))
        response = render_to_response(
                '{0}.jinja2'.format(
                    self.post.get('template', 'default')),
                self.post,
                request=self.request
                )
        if 'content_type' in self.post:
            response.content_type = self.post['content_type']
        return response

    @view_config(context=YAML)
    def yaml(self):
        self.post = yaml.load(
                AssetResolver().resolve(
                    self.context.__path__).stream(),
                LoaderFactory(self.request.registry.settings['data_dir']))
        return self.process_yaml()

    @view_config(context=Markdown)
    def markdown(self):
        self.post = frontmatter.load(
                AssetResolver().resolve(
                    self.context.__path__).stream(),
                handler=CustomYAMLHandler(self.request.registry.settings['data_dir']),
                ).to_dict()
        return self.process_yaml()

    @view_config(context=Jinja2)
    def jinja2(self):
        return render_to_response(
                self.context.path,
                {},
                request=self.request
                )
