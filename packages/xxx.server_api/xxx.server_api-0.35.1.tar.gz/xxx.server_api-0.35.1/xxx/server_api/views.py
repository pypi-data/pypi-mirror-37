import logging

from datetime import datetime
from pyramid.view import view_config
from .models import Number, Post
from .utils import retrieve_number, auth_doc, db

logger = logging.getLogger('xxx')

@view_config(route_name='home', renderer='templates/layout.jinja2')
def home(request):
    return {'project': 'xxx'}


@view_config(route_name='get_number', renderer='templates/number.jinja2', decorator=(retrieve_number,))
def get_number(request):
    number = request.number
    return {'number': number}


@view_config(route_name='tables', renderer='templates/tables.jinja2')
def get_number(request):
    number = 4545
    return {'number': number}

@view_config(route_name='register', renderer='json')
def register(request):
    try:
        payload = request.json_body
        payload['contract_number'] = payload['contact_number']
        auth_dict = auth_doc['users']
        if payload['contact_number'] not in auth_dict:
            auth_dict[payload['contact_number']] = \
                {'hashed_password': payload['hashed_password']}
            db.save(auth_doc)

            number = db.get(payload['contact_number'])
            if not number:
                number = Number()
                number._id = payload['contact_number']
                number.age = payload['age']
                number.city = payload['city']
                number.height = payload['height']
                number.weight = payload['weight']
                number.name = payload['name']
                number.registration_date = datetime.now()
                number.store(db)
    except Exception as e:
        logger.critical(e, exc_info=True)
        return {'data': str(e)}
    return {'data': 200}


@view_config(route_name='login', renderer='json')
def login(request):
    session = request.session
    payload = request.json_body
    contact_number = payload['contact_number']
    auth_dict = auth_doc['users']

    if contact_number not in auth_dict:
        return {'data': 400}
    elif payload['hashed_password'] != auth_dict[contact_number]['hashed_password']:
        return {'data': 401}
    session['authorized'] = True
    return {'data': {'session': session.session_id, 'status': 200}}


@view_config(route_name='add_post', renderer='json')
def add_new_post(request):

    if 'authorized' in request.session:
        payload = request.json_body
        payload['contract_number'] = payload['contact_number']
        number = Number(db.get(payload['contact_number']))
        new_post = Post()
        new_post.date_post = datetime.now()
        new_post.description = payload['description']
        new_post.title = payload['title']
        number.posts.append(new_post)
        number.last_post_date = new_post.date_post
        number.store(db)
        return {'data': {'status': 200}}
    else:
        return {'data': {'status': 400}}
