import time

import database
from Analyser import Analyser
import base64
from RabbitMq import RabbitMq

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mydb = database.Database("admin", "password", "aVoice")
    history = mydb.get_messages()

    analyser = Analyser("", "")
    rabbit = RabbitMq()
    analyser.study_messages(history)

    while True:
        rabbit.receive_message()