# ckpt2tfserving
a simple tool which can convert tensorflow checkpoint model file to tensorflow serving format.

## 安装

    pip install ckpt2tfserving

## 使用

#### 直接使用命令行工具 `ckpt_to_tfserving`

pip安装完毕后，会自动在系统中添加 `ckpt_to_tfserving` 命令，使用帮助请执行 `ckpt_to_tfserving --help`

示例

    ckpt_to_tfserving --input_tensor_names "{\"image\": \"Placeholder\"}" --output_tensor_names "{\"result0\": \"packed_25\", \"result1\": \"cls/prob/Reshape_1\", \"result2\": \"bbox/pred/BiasAdd\"}" --export_path ./xxx --ckpt_meta_file_path /Volumes/UUI/models/maskrcnn-1.3.1/model_v1.2.1.ckpt.meta --ckpt_file_path /Volumes/UUI/models/maskrcnn-1.3.1/model_v1.2.1.ckpt

*注意*：这种方式适合checkpoint完整包含最终inference时候的tensorflow graph，也就是说算法同事release的code中，没有在load checkpoint后，又用代码修改或者添加部分tensor
缺点是 1.导出的tensorflow serving文件包含了checkpoint中所有的train好的参数值，但是可能实际inference的时候只需要其中的一部分 2.需要咨询训练模型的同事先找到input的tensor和output的tensor


#### 使用patch session的方式 (*推荐*)

这种方式基本适合所有目前美研同事的模型release方式，使用方法简单，只需要在模型release的code的demo中，开头添加以下代码即可。

    tfsession_patch.patch("./xxx",model_type="predict", signature_key="the_signature_key")

其中 "./xxx" 表示你要将模型导出到路径，必须是不存在的路径
model_type的值 可以是predict/classify/regress，目前我们的模型无特别说明基本都属于tensorflow predict类型的，可以不传，这里默认也是predict
signature_key 表示部署后调用tensorflow serving时提供的signature key，可以不传，默认是the_signature_key

添加完后，运行demo code，完成一次inference的同时，模型也被自动导出了。导出过程中会打印出导出模型的input和output，以供调用的时候提供参数用。
