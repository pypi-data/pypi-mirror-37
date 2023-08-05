#!/usr/bin/env python3
import argparse
import logging
from argparse import ArgumentParser
from collections import namedtuple
from os.path import abspath, basename
from os.path import realpath, dirname
from typing import List, Dict

from mlvtools.cmd import CommandHelper, ArgumentBuilder
from mlvtools.mlv_dvc.dvc_parser import get_dvc_cmds
from mlvtools.helper import to_bash_variable

ARG_IDENTIFIER = '-'

logging.getLogger().setLevel(logging.INFO)
CURRENT_DIR = realpath(dirname(__file__))

ExtractedArg = namedtuple('ExtractedArg', ('value', 'arg'))


#
# def get_configurable_cmds(cmds: List[str], work_dir: str) -> ConfigurableCmds:
#     """
#         Replace file arguments value with variables in command calls
#         cmd1 ./pos_arg_file.txt -p 8080
#         cmd2 --input ./input.csv
#         cmd3 --in ./input.csv --out ./metrics.txt
#
#         returned value:
#
#         cmd1 $POS_ARG_TXT -p 8080
#         cmd2 --input $INPUT
#         cmd3 --in $INPUT --out $OUT
#     """
#     replaced_cmds = []
#     variables = {}
#     for cmd in cmds:
#         repl_cmd = cmd
#         variables = {**extract_file_arguments(cmd, work_dir), **variables}
#         for var_value, var_name in variables.items():
#             repl_cmd = repl_cmd.replace(var_value, f'${var_name}')
#         replaced_cmds.append(repl_cmd)
#     return ConfigurableCmds(replaced_cmds, variables)


#
# def extract_arguments(cmd: str):
#     """
#         Extract arguments from command line, ignore positional parameters
#
#         example: ./my_cmp.py 'pos_arg' --arg1 ./param1.txt -p 8080
#         returned value : {'./param1.txt': 'arg1', '8080': 'p', 'pos_arg': None }
#     """
#     cmd_args = cmd.replace('\ ', '').split()[1:]
#     _, args = ArgumentParser().parse_known_args(args=cmd_args)
#
#     extracted_args = {}
#     for index, arg in enumerate(args):
#         if arg.startswith(ARG_IDENTIFIER):
#             continue
#         prec_idx = index - 1
#         value = args[prec_idx] if prec_idx > 0 and args[prec_idx].startswith(ARG_IDENTIFIER) \
#             else None
#         extracted_args[arg] = value
#     return extracted_args


def aggregate_arg(cmds: List[str]) -> dict:
    """
        Aggregate variables name fromm all commands.
        If a value is used more than once, first name is kept.
        Positional argument default name is built from the value.
    :return:
    """
    variables = {}
    for cmd in cmds:
        variables = {**extract_arguments(cmd), **variables}

    # Set default name on positional argument
    return variables


def get_variabilized_cmds(cmds: List[str], variables: Dict[str, str]) -> List[str]:
    replaced_cmds = []
    for cmd in cmds:
        repl_cmd = cmd
        for var_value, var_name in variables.items():
            if not var_name:
                var_name = to_bash_variable(var_name if var_name else basename(var_value))
            repl_cmd = repl_cmd.replace(var_value, var_name)
        replaced_cmds.append(repl_cmd)
    return replaced_cmds


def get_export_pipeline_data(cmds: List[str]):


def export_pipeline(dvc_meta_file: str, output: str, work_dir: str):
    """
    TODO
    """

    dvc_cmds = get_dvc_cmds(work_dir, dvc_meta_file)

    variables = aggregate_arg(dvc_cmds)

    template_data = {'call': get_variabilized_cmds(dvc_cmds, variables),
                     'variables': variables}


class ExportPipeline(CommandHelper):

    def run(self, *args, **kwargs):
        args = ArgumentBuilder(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                               description='Export a DVC pipeline to sequential execution') \
            .add_force_argument() \
            .add_argument('--mlv_dvc', type=str, required=True, help='DVC pipeline metadata') \
            .add_argument('-o', '--output', type=str, help='The Python pipeline script output path',
                          required=True) \
            .parse(args)

        export_pipeline(args.dvc, args.output)

        logging.info(f'Python pipeline script is generated in {abspath(args.output)}')
