from behave import given, when, then
from json import dumps as json_dump, loads as json_load

@given("The user set the {username} and {password}")
def step_impl(context, username, password):
    context.username = username
    context.password = password

    assert username is not None
    assert password is not None

@when("User user post to the /users endpoint")
def step_impl_1(context):

    user = {
        "name": context.username,
        "password": context.password
    }

    res = context.client().post('/users', data = json_dump(user),
                             headers={"Content-Type": "application/json"})

    context.status_code = res.status_code;
    context.data = res.data

@then("The response is 201 and the user is created")
def step_impl_2(context):
    assert context.status_code == 201

    users = json_load(context.data)["users"]

    assert users["_id"] is not None
    assert users["name"] == context.username
    assert users["admin"] == False
    assert users["uri"] == "/users/1"
