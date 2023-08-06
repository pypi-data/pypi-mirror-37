from flask import request
from flask_restful import Resource as FlaskResource


class Method(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Status(object):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204


class Resource(FlaskResource):
    endpoint = ''
    serializer = None

    def __init__(self):
        self._serializer = self.serializer()

    def post(self):
        return self._serializer.create(request.json), Status.CREATED

    def put(self, id):
        return self._serializer.update(id, request.json), Status.OK

    def delete(self, id):
        return self._serializer.delete(id), Status.NO_CONTENT

    def get(self, id=None):
        return self._serializer.read(id) if id else self._serializer.list(
            request.args.to_dict()
        )


def add_resource(api, resource, identifier_type='int'):
    endpoint = resource.endpoint

    api.add_resource(
        resource,
        '/{}'.format(endpoint),
        methods=[Method.GET, Method.POST],
        endpoint='{}-list'.format(endpoint)
    )

    api.add_resource(
        resource,
        '/{}/<{}:id>'.format(endpoint, identifier_type),
        methods=[Method.GET, Method.PUT, Method.DELETE],
        endpoint=endpoint + '-detail'
    )
