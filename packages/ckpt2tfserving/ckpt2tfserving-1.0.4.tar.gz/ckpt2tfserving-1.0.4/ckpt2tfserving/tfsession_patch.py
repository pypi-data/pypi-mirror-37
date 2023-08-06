#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tensorflow as tf
import os
import re
import traceback

TF_Session = tf.Session


class _Session(TF_Session):
    __SWITCH_ON__ = True

    def run(self, fetches, feed_dict=None, options=None, run_metadata=None):
        """
        session.run可能run的是单个字符串代表的tensor 或者单个tensor，或者字符串组成的list，或者tensor组成的list
        通常一次inference里之多有两个sess.run，一个是load checkpoint的时候，这时候run的tensor都是save开头的
        另一种就是真正的inference，这里要排除第一种情况，只对第二种情况导出tfserving
        """
        try:
            if not _Session.__SWITCH_ON__:
                # inference的demo code通常只包含一次sess.run，如果有多次，则只导出第一次sess.run
                return super(_Session, self).run(fetches, feed_dict, options, run_metadata)
            if isinstance(fetches, unicode) or isinstance(fetches, str):
                if re.match(r'^save(_\d+)?/\w+', fetches, re.IGNORECASE):
                    return super(_Session, self).run(fetches, feed_dict, options, run_metadata)

            if isinstance(fetches, tf.Tensor):
                if re.match(r'^save(_\d+)?/\w+', fetches.name, re.IGNORECASE):
                    return super(_Session, self).run(fetches, feed_dict, options, run_metadata)
            for fetch in fetches:
                if isinstance(fetch, unicode) or isinstance(fetch, str):
                    if re.match(r'^save(_\d+)?/\w+', fetch, re.IGNORECASE):
                        return super(_Session, self).run(fetches, feed_dict, options, run_metadata)
                elif isinstance(fetches, tf.Tensor):
                    if re.match(r'^save(_\d+)?/\w+', fetch.name, re.IGNORECASE):
                        return super(_Session, self).run(fetches, feed_dict, options, run_metadata)
            if not feed_dict:
                # 如果没有feed 肯定不是我们需要导出的 直接忽略
                return super(_Session, self).run(fetches, feed_dict, options, run_metadata)
            print("======== get input tensor start ==========")
            input_tensors_map, output_tensors_map = {}, {}
            for input_tensor in feed_dict.keys():
                input_tensors_map[input_tensor.name] = tf.saved_model.utils.build_tensor_info(input_tensor)
                print("input tensor mapping to grpc input name: %s" % input_tensor.name)
            print("======== get input tensor done ===========")
            print("======== get output tensor start =========")
            for output_tensor in fetches:
                if isinstance(output_tensor, unicode) or isinstance(output_tensor, str):
                    output_tensor = self.graph.get_tensor_by_name(output_tensor)
                output_tensors_map[output_tensor.name] = tf.saved_model.utils.build_tensor_info(output_tensor)
                print("output tensor mapping to grpc output name: %s" % output_tensor.name)
            print("======== get output tensor done ==========")
            print("======== export model start ==============")
            builder = tf.saved_model.builder.SavedModelBuilder(_Session.export_path)
            signature = tf.saved_model.signature_def_utils.build_signature_def(inputs=input_tensors_map,
                                                                               outputs=output_tensors_map,
                                                                               method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME if _Session.model_type == 'predict' else (
                                                                                   tf.saved_model.signature_constants.CLASSIFY_METHOD_NAME if _Session.model_type == 'classify' else tf.saved_model.signature_constants.REGRESS_METHOD_NAME)
                                                                               )
            legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')

            builder.add_meta_graph_and_variables(self, [tf.saved_model.tag_constants.SERVING],
                                                 signature_def_map={_Session.signature_key: signature},
                                                 legacy_init_op=legacy_init_op)
            builder.save()
            print("======== export model done ==============")
            _Session.__SWITCH_ON__ = False
        except Exception as err:
            print("======== export model failed ============")
            traceback.print_exc()
        return super(_Session, self).run(fetches, feed_dict, options, run_metadata)


def patch(export_path, model_type="predict", signature_key="the_signature_key"):
    """
    patch tensorflow session，
    可以自动导出tensorflow model到tensorflow serving的格式 至少支持美研同事的模型
    :param export_path: 模型导出存放的路径
    :param model_type: 模型的类型，predict/classify/regress  默认是predict
    :param signature_key: 模型暴露的signature key，默认是the_signature_key
    :return:
    """
    if not (export_path and model_type and signature_key and model_type in ("predict", "classify", "regress")):
        raise Exception("patch参数错误，请指定export_path, model_type, signature_key.")
    if os.path.exists(export_path):
        raise Exception("export_path必须为不存在的path.")
    _Session.export_path = export_path
    _Session.model_type = model_type
    _Session.signature_key = signature_key
    tf.Session = _Session
