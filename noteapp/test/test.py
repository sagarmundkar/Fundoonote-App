import pytest

from Fundoonotes.noteapp.views import NoteDetail


def test_details(rf):
    request = rf.get('/Notes/List')
    response = NoteDetail(request)
    assert response.status_code == 200

    # import pytest
    # from mixer.backend.django import mixer
    # from django import urls
    #
    #
    # @pytest.mark.webtest
    # # class Testurl:
    # def test_detail_url(client):
    #     url = urls.reverse('Notes/List')
    #     resp = client.get(url)
    #     assert resp.status_code == 200

    #
    # # class TestModel:
    # def test_model(self):
    #         note = mixer.blend("noteapp.Note", id=1)
    #         assert note.title == True


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200
