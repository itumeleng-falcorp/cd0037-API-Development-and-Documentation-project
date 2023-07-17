# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

This documentation provides an overview of the endpoints available in the API.

## Base URL

The base URL for all API endpoints is `http://127.0.0.1:5000`.

## Error Handling

The API will return the following error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity
- 500: Internal Server Error

Errors will be returned as  objects in the following format:

{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}

## Endpoints

### Retrieve Categories

Fetches a dictionary of categories in which the keys are the ids and the values are the corresponding strings of the categories.

- URL: `/categories`
- Method: GET
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key-value pairs.

#### Example


GET http://127.0.0.1:5000/categories

Response:
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}


### Retrieve Questions

Fetches a paginated list of questions.

- URL: `/questions`
- Method: GET
- Request Arguments: None
- Returns:
  - `success`: Boolean indicating the success of the request.
  - `questions`: An array of question objects.
  - `total_questions`: Total number of questions.
  - `categories`: An object containing all categories.
  - `current_category`: The first category from the list.

#### Example


GET http://127.0.0.1:5000/questions

Response:
{
  "success": true,
  "questions": [...],
  "total_questions": 20,
  "categories": {...},
  "current_category": {...}
}

### Delete Question

Deletes a question using its ID.

- URL: `/questions/<question_id>`
- Method: DELETE
- Request Arguments: None
- Returns:
  - `success`: Boolean indicating the success of the request.
  - `deleted`: The ID of the deleted question.
  - `questions`: An array of remaining question objects.
  - `total_questions`: Total number of questions.

#### Example

DELETE http://127.0.0.1:5000/questions/10

Response:
{
  "success": true,
  "deleted": 10,
  "questions": [...],
  "total_questions": 19
}

### Create Question

Creates a new question.

- URL: `/questions`
- Method: POST
- Request Arguments: None
- Request Body:
  - `question`: The question text.
  - `answer`: The answer to the question.
  - `difficulty`: The difficulty level of the question.
  - `category`: The category ID of the question.
- Returns:
  - `success`: Boolean indicating the success of the request.
  - `created`: The ID of the created question.
  - `questions`: An array of all questions.
  - `total_questions`: Total number of questions.

#### Example


POST http://127.0.0.1:5000/questions

Request Body:
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "difficulty": 2,
  "category": 3
}

Response:
{
  "success": true,
  "created": 21,
  "questions": [...],
  "total_questions": 21
}

### Search Questions

Searches for questions containing a specific term.

- URL: `/questions/search`
- Method: POST
- Request Arguments: None
- Request Body:
  - `searchTerm`: The term to search for in the questions.
- Returns:
  - `success`: Boolean indicating the success of the request.
  - `questions`: An array of matching question objects.
  - `total_questions`: Total number of matching questions.
  - `categories`: An object containing all categories.
  - `current_category`: The first category from the list.

#### Example

POST http://127.0.0.1:5000/questions/search

Request Body:
{
  "searchTerm": "capital"
}

Response:
{
  "success": true,
  "questions": [...],
  "total_questions": 3,
  "categories": {...},
  "current_category": {...}
}

### Retrieve Questions by Category

Fetches a paginated list of questions filtered by category.

- URL: `/categories/<category_id>/questions`
- Method: GET
- Request Arguments: None
- Returns:
  - `success`: Boolean indicating the success of the request.
  - `questions`: An array of question objects.
  - `total_questions`: Total number of questions.

#### Example

GET http://127.0.0.1:5000/categories/3/questions

Response:
{
  "success": true,
  "questions": [...],
  "total_questions": 5
}

### Retrieve Quiz Questions

Fetches a random question for a quiz.

- URL: `/quizzes`
- Method: POST
- Request Arguments: None
- Request Body:
  - `previous_questions`: An array of IDs of previously asked questions.
  - `quiz_category`: An object containing the category ID and type.
- Returns:
  - `success`: Boolean indicating the success of the request.
  - `question`: A random question object.

#### Example

POST http://127.0.0.1:5000/quizzes

Request Body:
{
  "previous_questions": [5, 9],
  "quiz_category": {
    "id": 2,
    "type": "Art"
  }
}

Response:
{
  "success": true,
  "question": {...}
}

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
