global data_report_configs
import os
import sys
import jsonpickle
import models
from flask import Flask, request,send_from_directory, render_template, Blueprint
import json
from sqlalchemy.ext.serializer import loads, dumps

api = Blueprint('scapinspector_api', __name__, template_folder='templates')


def serialize(_query):
    #d = dictionary written to per row
    #D = dictionary d is written to each time, then reset
    #Master = dictionary of dictionaries; the id Key (int, unique from database) 
    #from D is used as the Key for the dictionary D entry in Master
    Master = {}
    D = {}
    x = 0
    for u in _query:
        d = u.__dict__
        D = {}
        for n in d.keys():
           if n != '_sa_instance_state':
                    D[n] = d[n]
        x = d['id']
        Master[x] = D
    return Master

@api.route('/api/scapinspector/get_benchmarks', methods=['POST'])
def get_benchmarks():
    """Return loaded benchmarks """
    benchmarks=models.get_benchmarks()
    json_data =  json.dumps(serialize(benchmarks))
    return json_data


