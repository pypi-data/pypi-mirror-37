def includeme(config):
    settings = config.get_settings()
    if 'static' in settings:
        config.add_static_view(
                'static',
                settings['static'],
                cache_max_age=3600)
