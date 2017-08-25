from celery import Celery


backend = 'mysql+pymysql://root:passwd@localhost:3306//celery'

app = Celery('tasks', broker='amqp://guest@localhost//', backend=backend)


@app.task
def add(x, y):
    return x + y


@app.task
def get_detailed_land_info():

    return True



