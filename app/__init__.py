from flask_restplus import Api
from flask import Blueprint

from .main.controller.typhoon_controller  import api as doms_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='NATCAT service',
          version='1.0',
          )

api.add_namespace(doms_ns, path='/typhoon')