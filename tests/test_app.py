import pytest
from ACEest_Fitness import app
from flask import session


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testing'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            # Ensure session is clean before each test
            sess['workouts'] = {"Warm-up": [], "Workout": [], "Cool-down": []}
        yield client # Tests run here

def test_index_get(client):
    """Test that the main page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEestFitness and Gym" in response.data
    assert b"Add Session" in response.data
    assert b"Logged Workouts" in response.data
    assert b"Total Time Spent: 0 minutes" in response.data
    assert b"Good start! Keep moving" in response.data
    assert b"Warm-up" in response.data
    assert b"Workout" in response.data
    assert b"Cool-down" in response.data

def test_add_workout_post(client):
    """Test adding a new workout."""
    response = client.post('/', data={'category': 'Workout', 'workout': 'Running', 'duration': '30'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Success: 'Running' added to Workout!" in response.data
    assert b"Running - 30 min" in response.data
    assert b"Total Time Spent: 30 minutes" in response.data
    assert b"Nice effort! You're building consistency" in response.data

def test_add_workout_invalid_input(client):
    """Test adding a workout with invalid data."""
    response = client.post('/', data={'category': 'Workout', 'workout': 'Yoga', 'duration': 'abc'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Error: Duration must be a valid number." in response.data

    response = client.post('/', data={'category': '', 'workout': 'Yoga', 'duration': '15'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Error: Please fill all fields." in response.data