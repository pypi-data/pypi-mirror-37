import json

from heptet_app.myapp_config import entry_points_json


def test_entry_points_json(app_request):
    context = None
    request = app_request
    response = entry_points_json(context, request)
    data = json.loads(response.text)

    assert 0, data
