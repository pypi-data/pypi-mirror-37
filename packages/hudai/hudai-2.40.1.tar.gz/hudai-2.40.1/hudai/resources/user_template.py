"""
hudai.resources.user_template
"""
from ..helpers.resource import Resource


class UserTemplateResource(Resource):
    def __init__(self, client):
        Resource.__init__(
            self, client, base_path='/users/templates')
        self.resource_name = 'UserTemplate'

    def list(self, user_id=None, content_type=None, name=None, page=None):
        query_params = self._set_limit_offset({
            'content_type': content_type,
            'name': name,
            'page': page,
            'user_id': user_id
        })

        return self.http_get('/', query_params=query_params)

    def create(self, content_type, markdown, name, user_id=None):
        return self.http_post('/',
                              data={'markdown': markdown,
                                    'name': name,
                                    'content_type': content_type,
                                    'user_id': user_id})

    def fetch(self, template_id):
        return self.http_get('/{id}',
                             params={'id': template_id})

    def delete(self, template_id):
        return self.http_delete('/{id}',
                                params={'id': template_id})
