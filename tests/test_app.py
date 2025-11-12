import pytest
from app import app
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

def test_workout_chart_page(client):
    """Test that the workout chart page loads correctly."""
    response = client.get('/workout-chart')
    assert response.status_code == 200
    assert b"Personalized Workout Chart" in response.data

def test_diet_chart_page(client):
    """Test that the diet chart page loads correctly."""
    response = client.get('/diet-chart')
    assert response.status_code == 200
    assert b"Best Diet Chart for Fitness Goals" in response.data

def test_progress_tracker_page(client):
    """Test that the progress tracker page loads correctly and shows initial data."""
    response = client.get('/progress-tracker')
    assert response.status_code == 200
    assert b"Personal Progress Tracker" in response.data
    assert b"Overall Total Time Spent: 0 minutes" in response.data
    assert b"Good start! Keep moving" in response.data
    assert b"Warm-up: 0 minutes" in response.data
    assert b"Workout: 0 minutes" in response.data
    assert b"Cool-down: 0 minutes" in response.data

def test_progress_tracker_with_data(client):
    """Test progress tracker with some logged data."""
    client.post('/', data={'category': 'Workout', 'workout': 'Running', 'duration': '30'}, follow_redirects=True)
    client.post('/', data={'category': 'Warm-up', 'workout': 'Stretching', 'duration': '10'}, follow_redirects=True)
    response = client.get('/progress-tracker')
    assert response.status_code == 200
    assert b"Warm-up: 10 minutes" in response.data
    assert b"Workout: 30 minutes" in response.data
    assert b"Overall Total Time Spent: 40 minutes" in response.data
    assert b"Nice effort! You're building consistency" in response.data