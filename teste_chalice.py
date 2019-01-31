import json
from unittest import TestCase

from chalice.config import Config
from chalice.local import LocalGateway

from app import app


class ArtistTests(TestCase):

    def setUp(self):
        self.lg = LocalGateway(app, Config())

    def test_get_artists(self):
        response = self.lg.handle_request(
            method='GET',
            path='/artists',
            headers={},
            body=''
        )
        assert response['statusCode'] == 200
        artists = json.loads(response['body'])
        assert artists.get('artists')[0].get('name') == 'OldDog'

    def test_get_artist(self):
        response = self.lg.handle_request(
            method='GET',
            path='/artist/OldDog',
            headers={},
            body=''
        )
        assert response['statusCode'] == 200
        artist = json.loads(response['body'])
        assert artist.get('name') == 'OldDog'

        response = self.lg.handle_request(
            method='GET',
            path='/artist/ACDC',
            headers={},
            body=''
        )
        assert response['statusCode'] == 400

    def test_get_artist_albums(self):
        response = self.lg.handle_request(
            method='GET',
            path='/artist/OldDog/albums',
            headers={},
            body=''
        )
        assert response['statusCode'] == 200
        artist = json.loads(response['body'])
        assert artist[0].get('name') == 'Velho Whiskey'

        response = self.lg.handle_request(
            method='GET',
            path='/artist/ACDC',
            headers={},
            body=''
        )
    def test_create_artist(self):
        artist = {"name": "Luciano"}
        response = self.lg.handle_request(
            method='POST',
            path='/artist',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(artist)
        )
        assert response['statusCode'] == 200
        artist = json.loads(response['body'])
        assert artist.get('name') == 'Luciano'

    def test_create_album(self):
        albums = {"name": "arrozaaao","year": "1212"}
        response = self.lg.handle_request(
            method='POST',
            path='/artist/OldDog/album',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(albums)
        )
        assert response['statusCode'] == 200
        artist = json.loads(response['body'])
        assert artist.get('name') == 'arrozaaao'

    def test_update_artist_name(self):
        artist = {"name": "arrozaaao"}
        response = self.lg.handle_request(
            method='PUT',
            path='/artist/OldDog',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(artist)
        )
        assert response['statusCode'] == 200
        artist = json.loads(response['body'])
        assert artist.get('name') == 'arrozaaao'


    def test_delete_artist(self):
        artist = {"name": "LucianoCamargo"}
        response = self.lg.handle_request(
            method='POST',
            path='/artist',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(artist)
        )

        assert response['statusCode'] == 200

        response = self.lg.handle_request(
            method='DELETE',
            path='/artist',
            headers={},
            body=""
        )
        assert response['statusCode'] == 405