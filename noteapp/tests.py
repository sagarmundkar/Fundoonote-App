import unittest
from django.test import TestCase, Client

from .forms import UserForm


# Testing the url
# class SimpleTest(unittest.TestCase):
#     # def SetUp(self):
#     #     # Every test needs a client.
#     #     self.client = Client()
#
#     def test_details(self):
#         # Issue a GET request.
#         response = self.client.get('/register/')
#         # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)
#

# Testing the api
class EntryTest(TestCase):
    def test_get_api_json(self):
        resp = self.client.get('/User/login/', format='json')
        self.assertValidJSONResponse(resp)

    # def assertValidJSONResponse(self, resp):
    #     pass


# Testing the Forms
# class AppFormTests(TestCase):
#     def test_form_is_vaid(self):
#         form_data = {'field1': 'value for field 1'}
#         form = UserForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         print(form.errors)
#
#
# Testing the userprofile api
class UserprofileListViewTest(TestCase):  #
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/userprofile/')
        self.assertEqual(response.status_code, 200)


# testing the  user api
class UserListViewTest(TestCase):
    def test_view_url(self):
        response = self.client.get('/User/list/')
        self.assertEqual(response.status_code, 200)


# testing the note view
class NoteViewTest(TestCase):
    def test_note_list_view_url(self):
        response = self.client.get('/Notes/show/')
        self.assertEqual(response.status_code, 200)


# testing the create new note url
class NoteListTest(TestCase):
    def test_note_list_url(self):
        response = self.client.get('/Notes/List/')
        self.assertEqual(response.status_code, 200)
