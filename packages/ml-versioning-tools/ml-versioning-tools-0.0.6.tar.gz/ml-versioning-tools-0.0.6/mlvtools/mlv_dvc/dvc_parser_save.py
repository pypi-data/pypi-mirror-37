from collections import namedtuple
from os.path import relpath, basename
from typing import List

import networkx
import yaml
from dvc.exceptions import DvcException
from dvc.project import Project

from mlvtools.exception import MlVToolConfException, MlVToolException

DvcMeta = namedtuple('DvcMeta', ('name', 'cmd', 'deps', 'outs'))


def parse_dvc_meta(dvc_meta_file: str) -> DvcMeta:
    try:
        with open(dvc_meta_file, 'r') as fd:
            raw_data = yaml.load(fd.read())
            deps = [v['path'] for v in raw_data.get('deps', [])]
            outs = [v['path'] for v in raw_data.get('outs', [])]
            return DvcMeta(basename(dvc_meta_file), raw_data.get('cmd', ''), deps, outs)
    except yaml.error.YAMLError as e:
        raise MlVToolConfException(f'Cannot load DVC meta file {dvc_meta_file}. Wrong format') from e
    except IOError as e:
        raise MlVToolConfException(f'Cannot load DVC meta file {dvc_meta_file}') from e


def get_dvc_cmds(work_dir, meta_file_path):
    try:
        graph = Project(work_dir).graph()[0]
        input_node = relpath(meta_file_path, work_dir)
        stages = networkx.get_node_attributes(graph, 'stage')
        return (stages[dvc_meta].cmd
                for dvc_meta in networkx.dfs_postorder_nodes(graph, input_node))
    except FileNotFoundError as e:
        print(e)
        raise MlVToolException(f'Can not find {meta_file_path}.') from e
    except DvcException as e:
        raise MlVToolException('Can not get DVC pipeline commands.') from e


def get_dvc_dependencies(target_file_path: str, dvc_files: List[str]):
    targeted_step = parse_dvc_meta(target_file_path)
    dvc_metas = get_meta_info(dvc_files)

    dag = networkx.DiGraph()
    for step in dvc_metas.values():
        dag.add_node(step.name, step=step)
        for dep in step.deps:
            if dep not in dvc_metas:
                continue
            dag.add_node(dvc_metas[dep].name, step=dvc_metas[dep])
            dag.add_edge(step.name, dvc_metas[dep].name, name=dep)
    dag.nodes()
    topological_sort = networkx.topological_sort(dag)
    # Remove not target_steps
    has_changed = True
    nodes = list(topological_sort)
    while has_changed and nodes:
        has_changed = False
        for node in nodes:
            if dag.out_degree(node) < 1 and node != targeted_step:
                nodes.remove(node)
                has_changed = True
    return [dag[n] for n in nodes]


#
# def get_dvc_dependencies(last_file_path: str, dvc_files: List[str]):
#     last_step = parse_dvc_meta(last_file_path)
#     dvc_metas = get_meta_info(dvc_files)
#     ordered_steps = []
#     stack = [last_step]
#     while stack:
#         step = stack.pop()
#         ordered_steps.append(step)
#         for dep in step.get('deps', []):
#             if dep['path'] not in dvc_metas:
#                 continue
#             stack.append(dvc_metas[dep['path']])
#     return ordered_steps


def get_meta_info(dvc_files: List[str]):
    dvc_data = {}
    for dvc_file in dvc_files:
        dvc_meta = parse_dvc_meta(dvc_file)
        for out in dvc_meta.outs:
            dvc_data[out] = dvc_meta
    return dvc_data


def extract_file_arguments(cmd: str, work_dir: str):
    """
        Extract file arguments from command line, ignore positional parameters

        example: ./my_cmp.py 'pos_arg.txt' --arg1 ./param1.txt -p 8080
        returned value : {'./param1.txt': 'ARG1', 'pos_arg.txt': 'POS_ARG_TXT' }
    """
    cmd_args = cmd.replace('\ ', '').split()[1:]
    _, args = ArgumentParser().parse_known_args(args=cmd_args)

    extracted_args = {}
    for index, arg in enumerate(args):
        if arg.startswith(ARG_IDENTIFIER):
            continue
        prec_idx = index - 1
        is_positional = prec_idx < 0 or not args[prec_idx].startswith(ARG_IDENTIFIER)
        name = args[prec_idx] if is_positional else basename(arg)
        variable_name = to_bash_variable(name)
        # Keep arg value and name only if it is a file from the work directory
        if exists(join(work_dir, arg)):
            extracted_args[arg] = variable_name
    return extracted_args
