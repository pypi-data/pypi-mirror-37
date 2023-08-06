from couchdb import Server as CouchdbServer
from pyramid.config import Configurator
from .design import sync_design


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('tables', '/tables')
    config.add_route('get_number', '/{number_id:\d+}')
    config.add_route('register', '/webapp_register')
    config.add_route('login', '/webapp_login')
    config.add_route('new_post', '/webapp_new_post')
    config.scan()

    #  database settings
    server = CouchdbServer(settings['couchdb.uri'])
    config.registry.couchdb_server = server
    if settings['couchdb.db'] not in server:
        server.create(settings['couchdb.db'])
    config.registry.db = server[settings['couchdb.db']]
    sync_design(config.registry.db)  # creates views in couchdb


    return config.make_wsgi_app()
