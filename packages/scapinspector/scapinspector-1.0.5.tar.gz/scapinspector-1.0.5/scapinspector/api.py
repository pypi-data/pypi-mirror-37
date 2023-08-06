global data_report_configs
import os
import sys
import jsonpickle
import models
from flask import Flask, request,send_from_directory, render_template, Blueprint
import json

api = Blueprint('scapinspector_api', __name__, template_folder='templates')

from sqlalchemy.ext.declarative import DeclarativeMeta
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


@api.route('/api/scapinspector/get_benchmarks', methods=['POST'])
def config():
    """Return loaded benchmarks """
    benchmarks=models.get_benchmarks()
    
    json_data = json.dumps(benchmarks, cls=AlchemyEncoder)
    #json_data = jsonpickle.encode(benchmarks, unpicklable=False)
    return json_data


