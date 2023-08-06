global data_report_configs
import os
import sys
import jsonpickle
import models
from flask import Flask, request,send_from_directory, render_template, Blueprint


api = Blueprint('scapinspector_api', __name__, template_folder='templates')


@api.route('/api/scapinspector/get_benchmarks', methods=['POST'])
def config():
    """Return loaded benchmarks """
    benchmarks=models.get_benchmarks()
    json_data = jsonpickle.encode(benchmarks, unpicklable=False)
    return json_data


