from django.urls import reverse

import pytest


pytestmark = pytest.mark.django_db

def test_get_selection_screen_view(client):
    """ Asserts a site visitor can GET the `selection` screen """
    path = reverse('countdown_letters:selection')
    response = client.get(path)
    assert response.status_code == 200, 'Should return an `OK` status code'

def test_get_game_screen_view(client):
    """ Asserts a site visitor can GET the `game` screen """
    base_path = reverse('countdown_letters:game')
    params = {
        'letters_chosen': 'ABCDEFGHI'
    }
    response = client.get(base_path, params)
    assert response.status_code == 200, 'Should return an `OK` status code'
    assert 'The letters selected' in response.content.decode('utf-8'), \
        'Should contain specified text'

@pytest.mark.vcr()
def test_get_results_screen_view(client):
    """ Asserts a site visitor can GET the `results` screen """
    path = reverse('countdown_letters:results')
    params = {
        'letters_chosen': 'SWIMMINGS',
        'players_word': 'SWIMMING'
    }
    response = client.get(path, params)
    assert response.status_code == 200, 'Should return an `OK` status code'
    assert 'You found a' in response.content.decode('utf-8'), 'Should contain specified text'
