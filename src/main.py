import time
import database
from nn import utils
from Analyser import Analyser
import base64
from RabbitMq import RabbitMq

if __name__ == '__main__':
    mydb = database.Database("admin", "password", "aVoice")
    users = mydb.get_users()

    rabbit = RabbitMq(None)

    # TODO: run rabbit on thread
    # while True:
    #     rabbit.receive_message()

