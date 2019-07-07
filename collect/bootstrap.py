# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import yaml
import argparse
from workflow import Workflow


def __arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        help=' config file',
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
  args = __arg_parse()
  print(args)
  config_file = open(args.config, encoding='utf-8')
  configs = yaml.load(config_file)
  workflow = Workflow(configs)
  workflow.run(1)