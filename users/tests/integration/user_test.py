# -*- coding: utf-8 -*-
import unittest
import json
from users.tests.base import BaseTestCase


class UsersTestCase(BaseTestCase):
    """This class represents the Users test case"""

    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        user = {
            "name": "test",
            "password": "12345"
        }

        res = self.client().post('/users', data=json.dumps(user), headers={"Content-Type": "application/json"})
        self.assertEqual(res.status_code, 201)
        users = json.loads(res.data)["users"]

        self.assertEqual(users["_id"], 1 , "The user id is None")
        self.assertEqual(users["name"], "test", "The name is not the same")
        self.assertEqual(users["admin"], False, "The new user shouldn't be admin")
        self.assertEqual(users["uri"], "/users/1", "The uri doesn't match")


    #
    def test_api_can_get_all_users(self):
        """Test API can get a users (GET request)."""
        user = {
                "name": "test",
                "password": "12345"
        }
        res = self.client().post('/users', data=json.dumps(user),
                               headers={"Content-Type":"application/json"})
        self.assertEqual(res.status_code, 201)

        auth = self.get_token(json.dumps({"username": user["name"], "password": user["password"]}))

        headers = {**auth, **{"Content-Type": "application/json"}}

        res = self.client().get('/users', headers = headers)

        self.assertEqual(res.status_code, 200)
        self.assertIn("name", str(res.data))

    def test_api_can_get_user_by_id(self):
        """Test API can get a single user by using it's id."""

        user = {
            "name": "test",
            "password": "12345"
        }
        rv = self.client().post('/users', data=json.dumps(user),
                              headers={"Content-Type": "application/json"})
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))["users"]

        auth = self.get_token(json.dumps({"username": user["name"], "password":user["password"]}))

        result = self.client().get(
            '/users/{}'.format(result_in_json['_id']), headers=auth)
        self.assertEqual(result.status_code, 200)
        self.assertIn(user["name"], str(result.data))

    def test_user_can_be_edited(self):
        user = {'name': 'Test User 2', "password": "123455"}

        """Test API can edit an existing user. (PUT request)"""
        rv = self.client().post('/users', data=json.dumps(user),
                                headers={"Content-Type": "application/json"})

        users = json.loads(rv.data)["users"]

        self.assertEqual(rv.status_code, 201)

        auth = self.get_token(json.dumps({"username": user["name"], "password": user["password"]}))

        headers = {**auth, **{"Content-Type": "application/json"}}

        user_id = users["_id"]

        user_to_update = {
            "_id": user_id,
            "name": "Test User 2",
            "password": "12346",
            "isAdmin": True

        }

        rv = self.client().put(
            f'/users/{user_id}',
            data=json.dumps(user_to_update), headers=headers)

        self.assertEqual(rv.status_code, 200)
        get_result = self.client().get(f'/users/{user_id}', headers=headers)

        self.assertEqual(get_result.status_code, 200)
        self.assertIn(user_to_update["name"], str(get_result.data))

    def test_users_deletion(self):
        """Test API can delete an existing users. (DELETE request)."""
        user = {'name': 'Test User 2', "password": "123456"}

        rv = self.client().post(
            '/users',
            data=json.dumps(user),
            headers={"Content-Type": "application/json"})

        self.assertEqual(rv.status_code, 201)

        users = json.loads(rv.data)["users"]

        user_id = users["_id"]

        auth = self.get_token(json.dumps({"username": user["name"], "password": user["password"]}))

        headers = {**auth, **{"Content-Type": "application/json"}}

        res = self.client().delete(f'/users/{user_id}',headers=headers)

        self.assertEqual(res.status_code, 204)

        # Test to see if it exists, should return a 404
        result = self.client().get(f'/users/{user_id}', headers=headers)
        self.assertEqual(result.status_code, 404)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()