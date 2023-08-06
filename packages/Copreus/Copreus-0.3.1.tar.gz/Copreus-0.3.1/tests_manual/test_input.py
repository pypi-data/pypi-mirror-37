import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from copreus.drivers.input import Input

from pelops.myconfigtools import read_config
from pelops.mymqttclient import MyMQTTClient
from pelops.mylogger import create_logger


def input_handler_pressed(message):
    print("button_pressed: {}".format(message))


def input_handler_state(message):
    print("button_state: {}".format(message))


filename = '../tests_unit/config_input.yaml'
config = read_config(filename)
logger = create_logger(config["logger"], __name__)
mqttclient = MyMQTTClient(config["mqtt"], logger, True)
mqttclient.connect()
mqttclient.subscribe(config["device"]["topics-pub"]["button_pressed"], input_handler_pressed)
mqttclient.subscribe(config["device"]["topics-pub"]["button_state"], input_handler_state)

Input.standalone(('-c', filename))

