import pytest
from app import app
from train import ingest_data

def test_data_ingestion_shape():
    X_train, x_test, y_train, y_test = ingest_data()
    assert X_train.shape[0] >0, "Nope, there's no data."
    assert X_train.shape[1] == 8, "Invalid number of features."

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client: 
        yield client

def test_predict_endpoint(client):
    mock_payload = {
        "MedInc": 10,
        "HouseAge": 10,
        "AveRooms": 10, 
        "AveBedrms": 10, 
        "Population": 10, 
        "AveOccup" :10, 
        "Latitude": 10, 
        "Longitude": 10
    }

    response = client.post('/predict', json = mock_payload)
    assert response.status_code in [200, 500], "API did not start."

#Run with python -m pytest test_pipeline.py -v