#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

import tensorflow as tf


def convert_ckpt_2_tfserving(input_tensor_names, output_tensor_names, export_path, signature_key,
                             ckpt_file_path, ckpt_meta_file_path, model_type="predict"):
    """

    :param input_tensor_names: serving的input key和输入的tensor名字对应关系，例如 {"image": "Placeholder"}
    :param output_tensor_names: serving的output key和输出的tensor名字对应关系，例如 {"result0": "packed_25", "result1": "cls/prob/Reshape_1", "result2": "bbox/pred/BiasAdd"}
    :param export_path: 导出模型存放的路径
    :param model_type: 模型类型 predict/classify/regress  默认predict
    :param signature_key: serving的signature key
    :param ckpt_file_path: 模型checkpoint文件路径
    :param ckpt_meta_file_path 模型checkpoint meta文件路径
    :return:
    """
    if model_type not in ("predict", "classify", "regress"):
        raise Exception('model_type must be predict or classify or regress.')
    if not os.path.exists(ckpt_meta_file_path):
        raise Exception('checkpoint file or meta file not exist.')
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)) as sess:
        saver = tf.train.import_meta_graph(ckpt_meta_file_path)
        saver.restore(sess, ckpt_file_path)
        input_tensors_map, output_tensors_map = {}, {}
        for input_tensor_name_key, input_tensor_name in input_tensor_names.items():
            input_tensors_map[input_tensor_name_key] = tf.saved_model.utils.build_tensor_info(
                sess.graph.get_tensor_by_name("%s:0" % input_tensor_name))
        for output_tensor_name_key, output_tensor_name in output_tensor_names.items():
            output_tensors_map[output_tensor_name_key] = tf.saved_model.utils.build_tensor_info(
                sess.graph.get_tensor_by_name("%s:0" % output_tensor_name))

        builder = tf.saved_model.builder.SavedModelBuilder(export_path)
        signature = tf.saved_model.signature_def_utils.build_signature_def(inputs=input_tensors_map,
                                                                           outputs=output_tensors_map,
                                                                           method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME if model_type == 'predict' else (
                                                                               tf.saved_model.signature_constants.CLASSIFY_METHOD_NAME if model_type == 'classify' else tf.saved_model.signature_constants.REGRESS_METHOD_NAME)
                                                                           )
        legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')

        builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING],
                                             signature_def_map={signature_key: signature},
                                             legacy_init_op=legacy_init_op)
        builder.save()
        print('save end to tf serving folder : ' + export_path)
