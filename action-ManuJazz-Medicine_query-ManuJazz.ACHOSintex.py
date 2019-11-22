#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_query_medicine(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    query_medicine(hermes, intentMessage, conf)

def query_medicine(hermes, intentMessage, conf):
    mqttClient.publish_start_session_notification('default', 'Ahora mismo no tienes que tomarte ninguna medicina', None)
    mqttClient.publish_end_session('default', "")

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h, Hermes(mqtt_options=mqtt_opts) as mqttClient:
        h.subscribe_intent("ManuJazz:Medicine_query", subscribe_query_medicine) \
         .start()
