
import json

version_json = '''
{"full-revisionid": "26a372bb8afeb0fdac186d0767d6041ff941a0e0", "error": null, "version": "0.16.0", "date": "2018-10-23T22:15:37.434356", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

