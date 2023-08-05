from importlib import import_module
from .parser import Parser
from .rule import rule_dict
import os
import click
import configparser
from termcolor import cprint
import sys
sys.path.append('.')


@click.group()
def main():
    """jr compiler 命令行工具"""

    pass


@main.command()
# 应用名, 根据应用名编译
@click.argument('app_name', required=False, default='.')
# 应用描述文件, 应用配置信息
@click.option('--ini', '-i', default=False)
def compile(app_name, ini):
    """编译"""
    cprint('开始编译...', 'blue')
    if not os.path.exists(app_name):
        cprint('编译失败', 'red')
        cprint('应用：' + app_name + ' 不存在', 'red')
        sys.exit(1)
    # 进入目录
    os.chdir(app_name)
    appinfo_dict = load_appinfo(ini)
    do_compile(appinfo_dict)
    cprint('编译完成', 'green')


def do_compile(appinfo):
    rule = appinfo['rule']
    # 读取规则文件
    if os.path.isfile(rule):
        with open(rule, 'r', encoding='utf-8') as f:
            lang_tx_str = f.read()
    elif rule in rule_dict.keys():
        lang_tx_str = rule_dict.get(rule)
    else:
        cprint('编译失败', 'red')
        cprint('DSL 语法描述文件 ' + rule + ' 不存在', 'red')
        sys.exit(1)
    input_path = appinfo['input_path']
    output_path = appinfo['output_path']
    output_ext = appinfo.get('output_ext')
    output_prefix = appinfo['output_prefix']

    template_path = appinfo['template_path']
    # 动态导入 Extension
    extension = appinfo['extension']
    _LOAD_MODULE = import_module(extension.split(':')[0])
    module_object = getattr(_LOAD_MODULE, extension.split(':')[1])  # 获取Extension
    exec_module_object = module_object(template_path)  # 实例化 Extension
    for file_path, _, files in os.walk(input_path):
        for file in files:
            input_file = os.path.join(file_path, file)
            output_file = os.path.join(file_path.replace(input_path, output_path), output_prefix + file)
            if output_ext:
                output_file = output_file.replace(output_file.split('.')[-1], output_ext)
            with open(input_file, 'r', encoding='utf-8') as f:
                dsl_str = f.read()
            parser_obj = Parser(dsl_str, lang_tx_str, template_path, exec_module_object)
            parser_obj.parse()
            parser_obj.save_to(output_file)
            cprint(input_file + ' --> ' + output_file + ' 成功 ', 'blue')


def load_appinfo(ini):
    config_info = {}
    if not ini:
        ini = 'appinfo.ini'
    if os.path.isfile(ini):
        config = configparser.ConfigParser()
        try:
            config.read(ini)
            config_info = {x[0]: x[1] for x in config.items(config.sections()[0])}
        except Exception as e:
            cprint('编译失败', 'red')
            raise Exception(e)

    else:
        # 创建默认配置信息
        try:
            config_info['rule_file'] = os.path.join('rule', os.listdir('rule')[0])
            config_info['input_path'] = 'input'
            config_info['output_path'] = 'output'
            config_info['output_prefix'] = 'JR_'
            config_info['template_path'] = 'template'
        except Exception as e:
            cprint('编译失败', 'red')
            raise Exception(e)
    return config_info


if __name__ == '__main__':
    main()

