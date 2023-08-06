
import json

version_json = '''
{"error": null, "full-revisionid": "26a372bb8afeb0fdac186d0767d6041ff941a0e0", "date": "2018-10-23T22:28:44.718269", "version": "0.16.0", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

