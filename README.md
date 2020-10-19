# Freelance test project

Hello there, and welcome to the *Freelance test project*, a test for Órama. the goal of this test is
to retrieve the information of json file and find the amout of months a freelancer has with his or 
her job experiences. This projects was made with Django and Django Rest Framework. Let's get to it.


## Prerequisites

- [Python](https://www.python.org/downloads/) >= 3.6.9
- [Docker](https://docs.docker.com/get-docker/) >= 19.03.6

## Running it

This couldn't be any simpler with Docker. Just run:

```
sudo docker build -t orama -f Dockerfile .
sudo docker run -it -d -p 8888:8888 orama
```

Now the application is listening in port 8888 ([http://127.0.0.1:8888](http://127.0.0.1:8888))

## Testing

For testing purposes, I use coverage to get a full overview of the parts of the code that are been 
tested. For that you can install the dependencies in a virtual environment .

```
python3 -m venv ./venv
. venv/bin/activate
pip3 install -r requirements.txt
```

And then run the coverage test:
```
coverage run --source="." manage.py test
```

To see the full report:
```
coverage report
```

To see the coveraged parts in html format:
```
coverage html
```

