# SCHEDULER FLASK API

It is a simple scheduler using a in memory dictionary as storage that could be improved and replaced by a Redis or Apache Kafka solution for example.

## Preparing

### Prepare a python 3 environment
Python 3 is required.

`python --version`

It is recommended to have a separated python virtual environment (https://docs.python.org/3/library/venv.html).  

`python3 -m venv schedulerenv`

`source schedulerenv/bin/activate`
 
 
### Install all requirements

Switch to the project directory

`pip install -r requirements.txt`

## Running

### Run flask

Starting flask on 5000 localhost port

`python -m flask run`

### Test the endpoint

You can test the endpoint with curl or any other tool:
```
curl -i --request POST \
  --url http://127.0.0.1:5000/scheduler/new \
  --header 'Content-Type: application/json' \
  --data '{ "content": "some content", "datetime": "2021-04-01 16:40"}'
```  


## Test

### Run tests

`pytest --capture=sys`

### Run coverage

`coverage run --source=. -m pytest --capture=sys`

### Check the report

`coverage report -m`
