
import json

version_json = '''
{"date": "2018-10-23T22:50:17.292656", "dirty": false, "error": null, "full-revisionid": "26a372bb8afeb0fdac186d0767d6041ff941a0e0", "version": "0.16.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

