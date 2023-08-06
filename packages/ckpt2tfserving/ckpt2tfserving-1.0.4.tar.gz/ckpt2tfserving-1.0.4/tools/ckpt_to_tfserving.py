#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import json
import os
from ckpt2tfserving.convertor import convert_ckpt_2_tfserving


def main():
    parser = argparse.ArgumentParser(description="ckpt_to_tfserving usage.")
    parser.add_argument('--input_tensor_names', type=str, help="指定输入tensor,例如{\"image\": \"Placeholder\"}",
                        required=True)
    parser.add_argument('--output_tensor_names', type=str, help="指定输出tensor,例如{\"result\": \"bbox/pred/BiasAdd\"}",
                        required=True)
    parser.add_argument('--export_path', type=str, help="导出模型存放路径，必须是不存在的路径", required=True)
    parser.add_argument('--model_type', type=str, default="predict", help="模型类型,predict/classify/regress三者之一，默认predict")
    parser.add_argument('--signature_key', type=str, default="the_signature_key", help="服务暴露的signature key")
    parser.add_argument('--ckpt_file_path', type=str, help="ckpt文件路径", required=True)
    parser.add_argument('--ckpt_meta_file_path', help="ckpt meta文件路径", required=True)
    args = parser.parse_args()

    input_tensor_names = args.input_tensor_names
    output_tensor_names = args.output_tensor_names
    export_path = args.export_path
    model_type = args.model_type
    signature_key = args.signature_key
    ckpt_file_path = args.ckpt_file_path
    ckpt_meta_file_path = args.ckpt_meta_file_path

    try:
        input_tensor_names = json.loads(input_tensor_names)
        output_tensor_names = json.loads(output_tensor_names)
    except:
        pass
    if not input_tensor_names or not output_tensor_names or not isinstance(input_tensor_names, dict) or not isinstance(
            output_tensor_names, dict):
        raise Exception("input_tensor_names or output_tensor_names is invalid.")
    if not os.path.exists(ckpt_meta_file_path):
        raise Exception("ckpt meta file not exist.")
    print("====== export start =======")
    convert_ckpt_2_tfserving(input_tensor_names, output_tensor_names, export_path, signature_key, ckpt_file_path,
                             ckpt_meta_file_path, model_type)
    print("====== export done ========")


if __name__ == '__main__':
    main()
