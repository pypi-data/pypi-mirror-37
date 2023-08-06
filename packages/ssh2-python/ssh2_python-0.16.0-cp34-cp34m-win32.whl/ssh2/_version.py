
import json

version_json = '''
{"date": "2018-10-23T22:11:11.817563", "dirty": false, "full-revisionid": "26a372bb8afeb0fdac186d0767d6041ff941a0e0", "version": "0.16.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

