jr 简介
=======

一个Python 语言开发的，基于
`textX <https://github.com/igordejanovic/textX>`__ 和
`jinja <https://github.com/pallets/jinja>`__ 的 DSL 研发平台

Installation
============

.. code:: python

   pip install jr


目录结构说明
============

.. code:: 

   ├── demo                        jr 插件示例 demo 目录
   │   └── pipeline                pipeline demo 目录
   │       ├── input               待编译DSL文件目录
   │       ├── output              编译输出的文件目录
   │       ├── rule                DSL 语法描述文件目录
   │       └── template            DSL 模板文件目录
   ├── doc                         jr 文档目录
   ├── jr                          jr 引擎所在的目录
   ├── requirements.txt            jr 项目依赖文件列表
   ├── setup.py                    setup 文件
   ├── LICENSE                     LICENSE 文件
   ├── MANIFEST.in                 MANIFEST 文件
   ├── README.md                   README 文件
   └── test                        单元测试目录

快速入门
============

新建文件夹，做为应用根目录

.. code::

    mkdir zion_demo
    cd zion_demo

创建应用描述文件

.. code::

    appinfo.ini

编写配置文件

.. code::

    [appinfo]
    app_name = zion_demo            # 应用名
    app_version = 1.0.0             # 应用版本号
    rule = python_tx                # DSL 语法描述文件, 默认支持 'python_tx', 'json_tx', 'pipeline_tx', 可自定义，指定自己的tx文件路径
    input_path = input              # 待编译 DSL 文件存放路径
    output_path = output            # 编译后输出文件存放路径
    output_prefix = JR_             # 编译后输出文件前缀
    output_ext = html               # 编译后输出文件后缀
    template_path = template        # 模板文件路径
    extension = jr:ZionExtension    # 使用的扩展类，默认支持 'jr:ZionExtension', 'jr:JsonExtension', 'jr:PipelineExtension', 可自定义，指定自己的扩展类, 格式 {module_name}:{class_name}

创建对应的文件夹

.. code::

    mkdir input output template

创建模板文件

.. code::

    ...

创建 DSL 文件

.. code::

    submit_demo.py

编写 DSL 文件

.. code::

    from ..lib.textbox import *
    from ..lib.submit import *

    mer_id = Textbox()
    mer_id.caption = "商户号"
    mer_id.id = "mer_id"
    mer_id.disabled = "true"

    op_id = Textbox()
    op_id.caption = "操作员号"
    op_id.id = "login_operator_id"
    op_id.disabled = "true"

    test_info_1 = Textbox()
    test_info_1.caption = "测试信息一"
    test_info_1.id = "test_info_1"

    test_info_2 = Textbox()
    test_info_2.caption = "测试信息二"
    test_info_2.id = "test_info_2"

    test_info_3 = Textbox()
    test_info_3.caption = "测试信息三"
    test_info_3.id = "test_info_3"

    btn_submit = Submit()
    btn_submit.text = "提交信息"
    btn_submit.callback = "showApiMsg"
    btn_submit.func = "post"
    btn_submit.url = "http://127.0.0.1/submit_demo"

编译 DSL 文件

.. code::

    jr compile
