import time

import database
from Analyser import Analyser
import base64
from RabbitMq import RabbitMq

if __name__ == '__main__':
    mydb = database.Database("admin", "password", "aVoice")
    history = mydb.get_messages()
    users = mydb.get_users()
    print(users)

    analyser = Analyser("", "")
    rabbit = RabbitMq()
    analyser.study_messages(history)

    # TODO: run rabbit on thread
    # while True:
    #     rabbit.receive_message()