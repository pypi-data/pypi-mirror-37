from pyramid.config import Configurator
from pyramid.path import AssetResolver
from .resources import Root

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pathlib import Path


class PagesEventHandler(FileSystemEventHandler):
    def __init__(self, root, root_path):
        super(PagesEventHandler, self).__init__()
        self.root = root
        self.root_path = root_path

    def find_dir(self, path):
        folder = self.root
        path = path.relative_to(self.root_path)
        for name in path.parts[:-1]:
            folder = folder[name]
        return folder

    def on_created(self, event):
        super(PagesEventHandler, self).on_created(event)
        path = Path(event.dest_path if hasattr(event, 'dest_path')
                    else event.src_path)
        folder = self.find_dir(path)
        if event.is_directory:
            folder.create_dir(path)
        else:
            folder.create_file(path)

    def on_deleted(self, event):
        super(PagesEventHandler, self).on_deleted(event)
        path = Path(event.src_path)
        folder = self.find_dir(path)
        name = path.stem
        if path.suffix not in ['.md', '.yaml', '.j2', '.jinja2'] \
           and path.name != 'index.html':
            name = path.name
        del folder[name]

    def on_moved(self, event):
        super(PagesEventHandler, self).on_moved(event)
        self.on_deleted(event)
        self.on_created(event)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from pyramid.settings import asbool
    watchdog = asbool(settings.get(
               'watchdog', 'false'))
    settings['watchdog'] = watchdog
    settings.setdefault('pages_dir', 'pages')
    settings.setdefault('data_dir', 'data')

    pages = Root(settings['pages_dir'])

    def factory(request):
        return pages

    config = Configurator(settings=settings,
                          root_factory=factory)
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.scan()
    if watchdog:
        path = AssetResolver().resolve(
            settings['pages_dir']).abspath()
        observer = Observer()
        event_handler = PagesEventHandler(pages, path)
        observer.schedule(
                event_handler,
                path,
                recursive=True)
        observer.start()
    return config.make_wsgi_app()
