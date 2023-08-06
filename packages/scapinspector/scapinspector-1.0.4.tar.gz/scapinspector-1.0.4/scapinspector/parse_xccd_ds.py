import os
import sys
import json
import untangle
import map_xml
import benchmarks
import profile_core
import load
import db

# this function loads an SCAP datastream file
# the file may contain many parts, multiple benchmarks, 
# profiles, definitions, dictionaries and other components
# It then parses it for relivant info needed for the UI 
def parse_datastream(xccdf_data_stream_file):
    print ("Parsing:",xccdf_data_stream_file)
    with open(xccdf_data_stream_file, 'r') as ds:
        data=ds.read()
    try:
        result_meta = untangle.parse(data)
    except Exception as err:
        sys.exit("There is an issue the data stream:{} ".format(err))
    #package=map_xml.parse(result_meta,{})
    #namespaces=package['namespace']
    #print(namespaces)

    parsed_data=benchmarks.get(result_meta,xccdf_data_stream_file)
    return parsed_data

