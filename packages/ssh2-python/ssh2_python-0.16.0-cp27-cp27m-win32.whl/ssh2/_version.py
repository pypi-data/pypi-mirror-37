
import json

version_json = '''
{"date": "2018-10-23T22:06:33.675000", "full-revisionid": "26a372bb8afeb0fdac186d0767d6041ff941a0e0", "dirty": false, "version": "0.16.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

