from flask_restplus import Namespace, fields


class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'


class NullableRaw(fields.Raw):
    __schema_type__ = ['object', 'null']
    __schema_example__ = 'nullable object'


class TyphonnDto:
    api = Namespace('Typhoon', description='us-er related operations')
    simple = api.model('Typhoon', {
        'name': fields.String(required=True, description='user email address'),
        'identifier': NullableString(description='user username'),
        'description': NullableString(description='user username'),
        'id': NullableString(description='user password'),
        'year': fields.DateTime(description='user Identifier'),
        'classification': fields.String(required=True, description='collection classification'),
    })
    # detailed = api.model('Typhoon Details', {
    #     'name': fields.String(required=True, description='user email address'),
    #     'identifier': NullableString(description='user username'),
    #     'description': NullableString(description='user username'),
    #     'id': NullableString(description='user password'),
    #     'created_on': fields.DateTime(description='user Identifier'),
    #     'super_domain_id': fields.String(required=True, description='Super Domain Id'),
    #     'modified_on': fields.DateTime(description='user Identifier'),
    #     'classification': fields.String(required=True, description='collection classification'),
    #     'enableDF': fields.Boolean(description='Enable Data Factory')
    # })
