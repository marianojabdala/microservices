from json import dumps as json_dump, loads as json_load
from behave import given, when, then
import sure

@given("The user set the {username} and {password}")
def step_impl(context, username, password):
    context.username = username
    context.password = password
    (username).should_not.be.none
    (password).should_not.be.none

@when("User user post to the /users endpoint")
def step_impl_1(context):

    user = {
        "name": context.username,
        "password": context.password
    }

    res = context.client().post('/users', data=json_dump(user),
                                headers={"Content-Type": "application/json"})

    context.status_code = res.status_code
    context.data = res.data

@then("The response is 201 and the user is created")
def step_impl_2(context):

    context.status_code.should.be.equal(201)

    users = json_load(context.data)["users"]

    users.should.be.a('dict')
    users.should.have.key("_id").being.equal(1)
    users.should.have.key("name").being.equal(context.username)
    users.should.have.key("admin").should.be.falsy
    users.should.have.key("uri").being.equal("/users/1")
