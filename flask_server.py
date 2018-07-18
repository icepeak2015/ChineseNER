from flask import Flask, jsonify
import codecs
import pickle
import itertools
from collections import OrderedDict
import os

import tensorflow as tf
import numpy as np
from model import Model
import loader
import utils
import data_utils
import json
from pprint import pprint

app = Flask(__name__)


flags = tf.app.flags
flags.DEFINE_string("ckpt_path",    "ckpt",      "Path to save model")
flags.DEFINE_string("log_test",     "test.log",     "File for test data")
flags.DEFINE_string("map_file",     "maps.pkl",     "file for maps")
flags.DEFINE_string("config_file",  "config_file",  "File for config")

FLAGS = tf.app.flags.FLAGS


slots_types = ["ARTIST", "SONG", "SENTI", "LANG", "THEME", "SCENE", "STYLE"]
def str2json(result):
    slots = []
    outer = OrderedDict()
    inner = OrderedDict()
    entities = result['entities']
    for ret in entities:
        if ret['type'] in slots_types:
            slots.append({"name":"{}".format(ret['type']), "value":"{}".format(ret['word'])})
        elif ret['type'] == "RANDOM":
            inner["intent"] = "RANDOM"
            outer["service"] = "musicX"
        elif ret['type'] == "PLAY":
            inner["intent"] = "PLAY"
            outer["service"] = "musicX"

    inner["slots"] = slots

    outer["rc"] = 0
    outer["semantic"] = dict(inner)

    pprint(dict(outer))
    return dict(outer)


#使用<user>传递参数
@app.route('/hello/<user>')
def hello_get(user):
    return 'hello get %s' % user


@app.route('/ner/<text>')
def ner_get(text):
    result = app.model.evaluate_line(sess, data_utils.input_from_line(text, char_to_id), id_to_tag)
    print('result: ', result)
    ret_json = str2json(result)
    return '%s' % ret_json

if __name__ == '__main__':
    config = utils.load_config(FLAGS.config_file)       # 读取配置文件
    log_path = os.path.join("evl_log", FLAGS.log_test)      # ./log/train.log
    logger = utils.get_logger(log_path)           # log文件名及路径

    # limit GPU memory
    tf_config = tf.ConfigProto()                  # TensorFlow 会话的配置项
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:        # map_file 中存储着字与id，tag与id之间的对应关系
        char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)

    with tf.Session(config=tf_config) as sess:
        model = utils.create_model(sess, Model, FLAGS.ckpt_path, data_utils.load_word2vec, config, id_to_char, logger)
        app.model = model
        app.run()

