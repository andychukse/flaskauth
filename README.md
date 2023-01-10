# flaskauth

Recently, I decided to learn Python, as part of learning I built a remote jobs ([remoteworka](https://remoteworka.com)) platform using Python Flask. 
This repo is part of the article:
## How to Building a User Authentication API using Python Flask and MySQL

## Download repo
```
git clone git@github.com:andychukse/flaskauth.git
```

## Step 1: Install and Set up your Flask Project.
 
You can follow the guide at Flask Official Documentation site or follow the steps below. Please ensure you have python3 and pip installed in your machine.

```
cd flaskauth
python3 -m venv venv
. venv/bin/activate
pip install requirements.txt 
```


## Install and Run the application
You can run the application by running
```
flask --app flaskauth run
```
Ensure the virtual environment is active and you're on the root project folder when you run this. 
Alternatively, you don't need to be in the root project folder to run the command if you installed the application using the command below
```
pip install -e .
```
