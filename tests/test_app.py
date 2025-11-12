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