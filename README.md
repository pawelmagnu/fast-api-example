# FastAPI + PostgreSQL + Docker Compose API Example

This is an example of a FastAPI application that uses PostgreSQL as a database and is run with Docker Compose.

## To run the application
```bash
docker-compose up --build
```

### Example API endpoints with curl

#### POST a new book
```bash
curl -X 'POST' \
  'http://localhost:8000/books/' \
  -H 'Content-Type: application/json' \
  -d '{
  "serial_number": "123456",
  "title": "Example Book",
  "author": "John Doe",
  "is_borrowed": false
}'
```

#### GET all books
```bash
curl -X 'GET' 'http://localhost:8000/books/' 
```

#### PUT (update) a book's availability
```bash
curl -X 'PUT' \
  'http://localhost:8000/books/123456' \
  -H 'Content-Type: application/json' \
  -d '{
  "is_borrowed": true,
  "borrowed_by": "654321",
  "borrowed_date": "2021-01-01"
}'
```

#### DELETE a book
```bash
curl -X 'DELETE' 'http://localhost:8000/books/123456'
```

