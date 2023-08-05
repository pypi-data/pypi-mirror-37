from django.test import TestCase
from movies_api.models import Movie
from movies_api.utils import response_to_json


class MoviesAPITestEndpoints(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000'

    def test_post_movies(self):
        response = self.client.post(self.url + '/movies', {'title': 'test'})
        self.assertEqual(200, response.status_code)

    def test_post_movies_wrong_request(self):
        response = self.client.post(self.url + '/movies')
        self.assertEqual(400, response.status_code)

        response = self.client.post(self.url + '/movies', {'title': ' '})
        self.assertEqual(400, response.status_code)

    def test_post_movies_movie_not_found(self):
        response = self.client.post(self.url + '/movies', {'title': 'zxcvbnm'})

        self.assertEqual(404, response.status_code)

    def test_get_movies(self):
        response = self.client.get(self.url + '/movies')
        self.assertEqual(200, response.status_code)

        self.client.post(self.url + '/movies', {'title': 'test'})
        response = self.client.get(self.url + '/movies/1')
        self.assertEqual(200, response.status_code)

    def test_get_movies_wrong_id(self):
        response = self.client.get(self.url + '/movies/tre')
        self.assertEqual(404, response.status_code)

        response = self.client.get(self.url + '/movies/-5')
        self.assertEqual(404, response.status_code)

    def test_post_comments(self):
        self.client.post(self.url + '/movies', {'title': 'test'})
        response = self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})
        self.assertEqual(200, response.status_code)

    def test_post_comments_wrong_request(self):
        response = self.client.post(self.url + '/comments')
        self.assertEqual(400, response.status_code)

        response = self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})
        self.assertEqual(400, response.status_code)

        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})

        response = self.client.post(self.url + '/comments', {'movie_id': '1'})
        self.assertEqual(400, response.status_code)

        response = self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': ' '})
        self.assertEqual(400, response.status_code)

    def test_get_comments(self):
        response = self.client.get(self.url + '/comments')
        self.assertEqual(200, response.status_code)

        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})

        response = self.client.get(self.url + '/comments/1')
        self.assertEqual(200, response.status_code)

    def test_get_comments_wrong_id(self):
        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})

        response = self.client.get(self.url + '/comments/tre')
        self.assertEqual(404, response.status_code)

        response = self.client.get(self.url + '/comments/-5')
        self.assertEqual(404, response.status_code)

    def test_get_top(self):
        response = self.client.get(self.url + '/top/1900-01-01/2018-12-31')
        self.assertEqual(200, response.status_code)

    def test_get_top_wrong_date(self):
        response = self.client.get(self.url + '/top/0000-00-00/2018-12-31')
        self.assertEqual(400, response.status_code)


class MoviesAPITestFunctions(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000'

    def test_movies_count(self):
        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/movies', {'title': 'django'})
        self.client.post(self.url + '/movies', {'title': 'robert'})

        response = self.client.get(self.url + '/movies')
        response_json = response_to_json(response)

        self.assertTrue(len(response_json) == Movie.objects.count())

    def test_comments_count(self):
        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/movies', {'title': 'django'})
        self.client.post(self.url + '/movies', {'title': 'robert'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Noo!'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Rubbish'})
        self.client.post(self.url + '/comments', {'movie_id': '2', 'comment': 'Yes'})
        self.client.post(self.url + '/comments', {'movie_id': '2', 'comment': 'Not Sure'})

        response = self.client.get(self.url + '/movies')
        response_json = response_to_json(response)

        self.assertTrue(len(response_json) == Movie.objects.count())

    def test_top(self):
        def test_top_count():
            response = self.client.get(self.url + '/top/1900-01-01/2018-12-31')
            response_json = response_to_json(response)

            self.assertTrue(len(response_json), 3)

        def test_top_first():
            response = self.client.get(self.url + '/top/1900-01-01/2018-12-31')
            response_json = response_to_json(response)

            self.assertTrue(response_json[0]['movie_id'] == 2)

        def test_top_rank():
            response = self.client.get(self.url + '/top/1900-01-01/2018-12-31')
            response_json = response_to_json(response)

            self.assertTrue(response_json[0]['rank'] == 1)
            self.assertTrue(response_json[1]['rank'] == 2)
            self.assertTrue(response_json[2]['rank'] == 2)

        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/movies', {'title': 'django'})
        self.client.post(self.url + '/movies', {'title': 'robert'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Awesome!'})
        self.client.post(self.url + '/comments', {'movie_id': '1', 'comment': 'Noo!'})
        self.client.post(self.url + '/comments', {'movie_id': '3', 'comment': 'Rubbish'})
        self.client.post(self.url + '/comments', {'movie_id': '3', 'comment': '2/10'})
        self.client.post(self.url + '/comments', {'movie_id': '2', 'comment': 'Yes'})
        self.client.post(self.url + '/comments', {'movie_id': '2', 'comment': 'Not Sure'})
        self.client.post(self.url + '/comments', {'movie_id': '2', 'comment': 'Like it'})

        test_top_count()
        test_top_first()
        test_top_rank()

    def test_movies_sort(self):
        self.client.post(self.url + '/movies', {'title': 'test'})
        self.client.post(self.url + '/movies', {'title': 'django'})
        self.client.post(self.url + '/movies', {'title': 'robert'})

        response = self.client.get(self.url + '/movies?sort_by=released')
        response_json = response_to_json(response)

        self.assertTrue(response_json[0]['title'] == 'Django')

