import unittest
from old_app import *

class app_tests(unittest.TestCase):
    def setUp(self):
        """Configure app for testing and create a test client."""
        self.app = app.test_client()
        self.app.testing = True
        self.assertIsNotNone(self.app)
    
    def test_top_species_valid_dict(self):
        """See if valid request to  top_species gives expected output."""
        response = self.app.get('/top_species/Northfield/10/3')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('Amphibia', data)
    
    def test_top_species_valid_contains_observations(self):
        """See if valid request to top_species gives expected output with observations."""
        response = self.app.get('/top_species/Northfield/10/3')
        data = response.get_json()
        self.assertIn('Amphibia', data)
    
    def test_top_species_invalid_location(self):
        """See if invalid location gives expected error."""
        response = self.app.get('/top_species/InvalidCity/10/3')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)

    def test_leaderboard_valid_list(self):
        """See if valid request to leaderboard gives expected output."""
        response = self.app.get('/leaderboard/Common%20Loon')
        data = response.get_json()
        self.assertIsInstance(data, list)
    
    def test_leaderboard_valid_list_contains_users(self):
        """See if valid request to leaderboard gives expected output with users."""
        response = self.app.get('/leaderboard/Common%20Loon')
        data = response.get_json()
        self.assertIn('user', data[0])
    
    def test_leaderboard_invalid_animal(self):
        """See if invalid animal gives expected error."""
        response = self.app.get('/leaderboard/NotAnAnimal')
        data = response.get_json()     
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        return super().tearDown()
    
if __name__ == '__main__':
    unittest.main()