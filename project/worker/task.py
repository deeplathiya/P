from celery import Celery
import random
import requests, json

config = {
    'CELERY_BROKER_URL': "redis://localhost",
    'CELERY_RESULT_BACKEND': "redis://localhost"
}

celery = Celery('task', broker=config['CELERY_BROKER_URL'], backend=config['CELERY_RESULT_BACKEND'])


@celery.task(name='task.pay')
def pay(id, amount):
    i = random.randint(0,1)         #Randomly generate a number between 0 and 1 which denotes success or failure

    #Calling the Put API of the payment microservice
    url = "http://localhost"
    data = {'id': id, 'stat': i}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.put(url, data=json.dumps(data), headers=headers)
