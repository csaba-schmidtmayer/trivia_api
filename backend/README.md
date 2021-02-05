# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

The backend API uses the following endpoints:

| HTTP method | Route | Link |
| --- | --- | --- |
| GET | /categories | [Read more](#get-categories) |
| GET | /questions | [Read more](#get-questions) |
| GET | /categories/<category_id>/questions | [Read more](#get-categoriescategory_idquestions) |
| POST | /questions | [Read more](#post-questions) |
| POST | /quizzes | [Read more](#post-quizzes) |
| DELETE | /questions/<question_id> | [Read more](#delete-questionsquestion_id) |

### GET /categories

Fetches a list of categories.

#### Example

```bash
curl http://127.0.0.1:5000/categories
```

#### Request arguments

None

#### Response payload

| Key | Data |
| --- | --- |
| `categories` | An array of [category objects](#category-objects). |

### GET /questions

Fetches a paginated list of questions. A page contains ten objects or less if the last page is requested.

#### Example

```bash
curl http://127.0.0.1:5000/questions
```

#### Request arguments

| Name | Type | Use |
| --- | --- | --- |
| `page` | int | Determines the slice of all objects that is returned. Default value is 1. A value over the valid range of pages returns a 404 error. |

#### Response payload

| Key | Data |
| --- | --- |
| `categories` | An array of [category objects](#category-objects). |
| `current_category` | `null` |
| `questions` | An array of [question objects](#question-objects). |
| `success` | true |
| `total_questions` | An integer specifying the total number of questions in the database, can be used to calculate the number of pages. |

### GET /categories/<category_id>/questions

Fetches the list of questions in the specified category. Trying to access an invalid category id returns a 422 error.

#### Example

```bash
curl http://127.0.0.1:5000/categories/2/questions
```

#### Request arguments

None

#### Response payload

| Key | Data |
| --- | --- |
| `current_category` | The id of the requested category. |
| `questions` | An array of all [question objects](#question-objects) belonging to the requested category. |
| `success` | true |
| `total_questions` | An integer specifying the total number of returned questions. |

### POST /questions

Depending on the request payload, creates a new question in the database or performs a search on the question text.

#### Example

```bash
curl http://127.0.0.1:5000/questions -H "Content-Type: application/json" -X POST -d "{\"question\":\"Which country is the only remainig grand duchy?\",\"answer\":\"Luxembourg\",\"category\":3,\"difficulty\":3}"
```

```bash
curl http://127.0.0.1:5000/questions -H "Content-Type: application/json" -X POST -d "{\"search_term\":\"title\"}"
```

#### Request payload of submitting new questions

| Key | Type | Data |
| --- | --- | --- |
| `question` | str | The question text. If a question with the same text exists in the database, a 409 error is returned. |
| `answer` | str | The answer text. |
| `category` | int | The id of the category the question belongs to. |
| `difficulty` | int | The perceived difficulty of the question on a scale of 1-5. |

All of the keys and their corresponding data must be included in the request.

#### Response payload of submitting new questions

| Key | Data |
| --- | --- |
| `success` | true |

#### Request payload of performing a search

| Key | Type | Data |
| --- | --- | --- |
| `search_term` | str | The search term. The search is case insensitive and successful if the search term is found anywhere in the question text. If included, other keys in the payload are discarded.|

#### Response payload of performing a search

| Key | Data |
| --- | --- |
| `current_category` | null |
| `questions` | An array of all [question objects](#question-objects) that match the search term. |
| `success` | true |
| `total_questions` | An integer specifying the total number of returned questions. |

### POST /quizzes

Fetches a question for a quiz with the specified parameters.

#### Example

```bash
curl http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -X POST -d "{\"category\":2,\"previous_questions\":[16,18]}"
```

#### Request arguments

| Name | Type | Use |
| --- | --- | --- |
| `category` | int or null | The id of the category for the quiz or `null` to choose from any category. |

#### Response payload

| Key | Data |
| --- | --- |
| `current_category` | The id of the current category or `null`. |
| `questions` | An single [question object](#question-objects) from the requested category or from any categories. |
| `success` | true |

### DELETE /questions/<question_id>

Deletes the specified question. Trying to delete a question that does not exist returns a 422 error.

#### Example

```bash
curl http://127.0.0.1:5000/questions/2 -X DELETE
```

#### Request arguments

None

#### Response payload

| Key | Data |
| --- | --- |
| `success` | true |
| `id` | The former id of the question that was deleted. |

### Error payload

HTTP errors return a payload with the following shape:

| Key | Data |
| --- | --- |
| `error` | The HTTP status code. |
| `message` | A descriptive message of the exact problem. |
| `success` | false |

#### Example

```
{
  "error": 422,
  "message": "The requested category does not exist.",
  "success": false
}
```

###  Category objects

Category objects represent a quiz category and have the following shape:

| Key | Data |
| --- | --- |
| `id` | The id of the category. |
| `type` | The name of the category. |

#### Example

```
{
  "id": 1,
  "type": "Science"
}
```

###  Question objects

Question objects represent a quiz question and have the following shape:

| Key | Data |
| --- | --- |
| `id` | The id of the question |
| `question` | The question text. |
| `answer` | The answer text. |
| `category` | The id of the category the question belongs to. |
| `difficulty` | The perceived difficulty of the question. |

#### Example

```
{
  "id": 18,
  "question": "How many paintings did Van Gogh sell in his lifetime?",
  "answer": "One",
  "category": 2,
  "difficulty": 4
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Credits

The random question query is based on [this Stackoverflow answer](https://stackoverflow.com/a/33583008) from Jeff Widman.