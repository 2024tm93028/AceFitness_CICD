import pytest
from ACEest_Fitness import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testing'
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test that the main page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEestFitness and Gym" in response.data
    assert b"Add Workout" in response.data
    assert b"Logged Workouts" in response.data

def test_add_workout_post(client):
    """Test adding a new workout."""
    response = client.post('/', data={'workout': 'Running', 'duration': '30'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Success: 'Running' added successfully!" in response.data
    assert b"Running - 30 minutes" in response.data

def test_add_workout_invalid_duration(client):
    """Test adding a workout with invalid duration."""
    response = client.post('/', data={'workout': 'Yoga', 'duration': 'abc'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Error: Duration must be a valid number." in response.data