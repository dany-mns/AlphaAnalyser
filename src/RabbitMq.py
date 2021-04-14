import base64
import io
import pandas as pd

import pika
from nn import model, text
import numpy as np
import cv2
from retry import retry
from src.message import Message

class RabbitMq:
    config = {
    'host': '0.0.0.0',
    'port': 5678,
    'username': 'student',
    'password': 'student',
    'exchange': 'alphapp.direct',
    'routing_key': 'alphapp.routingkey1',
    'queue': 'alphapp.queue'
    }
    credentials = pika.PlainCredentials(config['username'],
    config['password'])
    parameters = (pika.ConnectionParameters(host=config['host']),
    pika.ConnectionParameters(port=config['port']),
    pika.ConnectionParameters(credentials=credentials))

    def __init__(self, user_data):
        self.user_data = user_data
        self.image_network = model.Sequential()
        self.image_network.load("/home/danny/Documents/AC-2020/Licenta/AlphaAnalyser/model/image_cls.an")
        self.text_network = model.Sequential()
        self.text_network.load("/home/danny/Documents/AC-2020/Licenta/AlphaAnalyser/model/mood_cls.an")
        self.vectorizer = text.CountVectorizer()
        self.vectorizer.fit(self.get_sentences())

    def on_received_message(self, blocking_channel, deliver, properties, message):
        result = message.decode('utf-8')
        blocking_channel.confirm_delivery()
        try:
            envelope = Message(result)
            self.add_message(envelope)
            blocking_channel.stop_consuming()
        except Exception as e:
            print(e)
            print("wrong data format")
        finally:
            blocking_channel.stop_consuming()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def receive_message(self):
        # automatically close the connection
        with pika.BlockingConnection(self.parameters) as connection:
        # automatically close the channel
            with connection.channel() as channel:
                channel.basic_consume(self.config['queue'], self.on_received_message, auto_ack=True)
                try:
                    channel.start_consuming()
                    # Don't recover connections closed by server
                except pika.exceptions.ConnectionClosedByBroker:
                    print("Connection closed by broker.")
                    # Don't recover on channel errors
                except pika.exceptions.AMQPChannelError:
                    print("AMQP Channel Error")
                    # Don't recover from KeyboardInterrupt
                except KeyboardInterrupt:
                    print("Application closed.")

    @staticmethod
    def get_sentences():
        filepath_dict = {'yelp': '../vocabulary/sentiment/yelp_labelled.txt',
                         'amazon': '../vocabulary/sentiment/amazon_cells_labelled.txt',
                         'imdb': '../vocabulary/sentiment/imdb_labelled.txt'}

        df_list = []
        for source, filepath in filepath_dict.items():
            df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
            df['source'] = source  # Add another column filled with the source name
            df_list.append(df)

        df = pd.concat(df_list)

        df_yelp = df[df["source"] == "yelp"]
        df_amazon = df[df["source"] == "amazon"]
        df_imdb = df[df["source"] == "imdb"]

        sentences_y = df_yelp["sentence"].values
        y_y = df_yelp["label"].values

        sentences_imdb = df_imdb["sentence"].values
        y_imdb = df_imdb["label"].values

        sentences_amazon = df_amazon["sentence"].values
        y_amazon = df_amazon["label"].values

        sentences = []
        sentences.extend(sentences_y)
        sentences.extend(sentences_amazon)
        sentences.extend(sentences_imdb)
        y = []
        y.extend(y_y)
        y.extend(y_amazon)
        y.extend(y_imdb)

        sentences = np.array(sentences)
        y = np.array(y)

        return sentences, y

    def mediete_mood(self, username, value):
        tmp = np.mean(self.user_data[username]["text"].copy().append(value))
        self.user_data[username]["text"].append(tmp)

    @staticmethod
    def preprocess_image(b64_image):
        image = cv2.imread(io.BytesIO(base64.b64decode(b64_image)))
        # move channel to position 3
        # (H, W, C) -> (C, H, W)
        image = np.moveaxis(image, -1, 0)
        # simulate that the image is a single feature map
        return [image]

    def preprocess_text(self, raw_text):
        return self.vectorizer.transform(np.array([raw_text]))

    def add_message(self, envelope):
        print(envelope.from_user)
        print(envelope.body_message)
        print(envelope.type_message)
        if envelope.from_user not in self.user_data:
            self.user_data[envelope.from_user] = {"images": {"airplane": 0, "automobile": 0, "ship": 0, "truck": 0, "unknown": 0}, "text": []}

        if envelope.type_message == "text":
            clean_text = self.preprocess_text(envelope.body_message)
            sentiment_value = self.text_network.predict(clean_text)
            self.mediete_mood(envelope.from_user, sentiment_value)
            print(f"The message {envelope.body_message} is {sentiment_value} negative-positive")
        elif envelope.type_message == "image":
            image = self.preprocess_image(envelope.body_message)
            class_index = np.argmax(self.image_network.predict(image))
            print(f"For image I predict {class_index} index class")
        else:
            print("Unknown format message")


    def clear_queue(self, channel):
        channel.queue_purge(self.config['queue'])