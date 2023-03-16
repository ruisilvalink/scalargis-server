import logging
from flask import request
from flask_restx import Resource

from ..portal.parsers import *
from ..portal.serializers import *
from ..portal.dao import settings as dao_settings
from ..endpoints import check_user, ns_portal as ns


logger = logging.getLogger(__name__)


@ns.route('/settings/', defaults={'table': None})
@ns.route('/settings/<string:table>')
class SettingsList(Resource):
    def __init__(self, api=None, entity_name=None, *args, **kwargs):
        #self.api = api
        super(SettingsList, self).__init__(api, *args, **kwargs)
        self.entity_name = entity_name

    def options(self, table=None):
        return {'Allow': 'GET, POST, PUT, DELETE'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, X-API-KEY'
                }

    @ns.expect(parser_records_with_page)
    @ns.marshal_with(page_settings)
    def get(self, table=None):
        """Returns Settings"""
        if (check_user(request)):
            return dao_settings.get(table or self.entity_name, request), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return None, 401, {'Access-Control-Allow-Origin': '*'}

    @ns.doc('create_settings')
    @ns.expect(settings_api_model)
    @ns.marshal_with(settings_api_model, code=201)
    def post(self, table=None):
        '''Create a new table record'''
        #if (check_user(request)):
        item = dao_settings.create(table or self.entity_name, request.json)
        return item, 201, {'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Methods': 'POST',
                           'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
                           }
        #else:
        #    return None, 401, {'Access-Control-Allow-Origin': '*',
        #                       'Access-Control-Allow-Methods': 'POST',
        #                       'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
        #                       }

    @ns.doc('delete_settings values')
    @ns.response(204, 'Generic values deleted')
    def delete(self, table=None):
        '''Delete a record given its identifier'''
        #if (check_user(request)):
        data = request.args.get('filter')
        status = dao_settings.delete_list(table or self.entity_name, data)
        return None, status, {'Access-Control-Allow-Origin': '*',
                              'Access-Control-Allow-Methods': 'GET, POST PUT, DELETE',
                              'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
                              }
        #else:
        #    return None, 401, {'Access-Control-Allow-Origin': '*',
        #                       'Access-Control-Allow-Methods': 'GET, POST PUT, DELETE',
        #                       'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
        #                       }


#@ns.route('/settings/', defaults={'table': None})
@ns.route('/settings/<string:table>/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The record identifier')
class Settings(Resource):
    def __init__(self, api=None, entity_name=None, *args, **kwargs):
        super(Settings, self).__init__(api, *args, **kwargs)
        self.entity_name = entity_name

    def options(self, id, table=None):
        return {'Allow': 'GET, PUT, DELETE'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, X-API-KEY'
                }

    '''Show a single todo item and lets you delete them'''

    @ns.doc('get_setting')
    @ns.marshal_with(settings_api_model)
    def get(self, id, table=None):
        '''Fetch a given resource'''
        if (check_user(request)):
            item = dao_settings.get_by_id(table or self.entity_name, id)
            return item, 201, {'Access-Control-Allow-Origin': '*',
                               'Access-Control-Allow-Methods': 'GET, POST PUT, DELETE',
                               'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
                               }
        else:
            return None, 401, {'Access-Control-Allow-Origin': '*',
                               'Access-Control-Allow-Methods': 'GET, POST PUT, DELETE',
                               'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
                               }

    @ns.doc('delete_settings')
    @ns.response(204, 'Record deleted')
    def delete(self, id, table=None):
        '''Delete a record given its identifier'''
        #if (check_user(request)):
        status = dao_settings.delete(table or self.entity_name, id)
        return None, status, {'Access-Control-Allow-Origin': '*',
                              'Access-Control-Allow-Methods': 'GET, POST PUT, DELETE',
                              'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
                              }
        #else:
        #    return None, 401, {'Access-Control-Allow-Origin': '*',
        #                       'Access-Control-Allow-Methods': 'GET, POST PUT, DELETE',
        #                       'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
        #                       }

    @ns.expect(settings_api_model)
    @ns.marshal_with(settings_api_model)
    def put(self, id, table=None):
        '''Update a record given its identifier'''
        item = dao_settings.update(table or self.entity_name, id, request.json)
        return item, 200, {'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Methods': 'PUT',
                           'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
                           }
