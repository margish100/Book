from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_add_book():
    response = client.post(
        "/books/",
        json={"title": "Python Book", "author": "Margish", "publication_year": 2024},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Python Book"

def test_submit_review():
    # Assuming you have a book ID to use here; otherwise, create a book first
    book_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    response = client.post(
        "/reviews/",
        json={"book_id": book_id, "text": "testing", "rating": 3},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "testing"

def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_reviews_for_book():
    # Assuming you have a book ID with reviews
    book_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    response = client.get(f"/reviews/{book_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
