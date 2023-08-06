import argparse
from dophon_manager.actions import *

parser = argparse.ArgumentParser(description='dophon project manager')
parser.add_argument('action', type=str, default='-h')
parser.add_argument('--action_arg', type=str, default='dophon_project')
FLAGS = parser.parse_args()

ARG_DICT = {
    'new': ActionObj().new_action
}

__version__ = '0.1.0'


def main():
    # 执行项目管理初始化
    action = FLAGS.action
    if action in ARG_DICT:
        print(ARG_DICT[action])
        ARG_DICT[action](FLAGS.action_arg)
