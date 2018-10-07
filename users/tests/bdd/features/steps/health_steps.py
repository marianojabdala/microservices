from behave import given, when, then
from json import loads as json_load

@when("Hit the /_health endpoint")

def step_impl(context):
    res = context.client().get('/_health',
                           headers={"Content-Type": "application/json"})

    assert res.status_code == 200
    assert res.data is not None

    context.status_code = res.status_code;
    context.data = res.data


@then("I can get the json body")
def step_impl_2(context):
    app = json_load(context.data)["app"]

    assert app is not None
