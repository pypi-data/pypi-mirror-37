import click
import sys
import os
import re
import inspect

from bamboo_lib.models import BasePipeline


def expander(path_str):
    return os.path.expanduser(os.path.expandvars(path_str))


def parse_value(v):
    if v in ["True", "true"]:
        return True
    elif v in ["False", "false"]:
        return False
    if v.isdecimal():
        try:
            return int(v)
        except ValueError:
            return float(v)
    return v


def parse_params(raw_params):
    my_dict = {}
    for p in raw_params:
        m = re.search(r"--([^(?:\s|\t|=)]+)=([A-Za-z0-9-_./+()]+)", p)
        key, value = m.group(1), m.group(2)
        print(key, value)
        my_dict[key] = parse_value(value)

    return my_dict


def get_pipeline_class(module_obj):
    for name, obj in inspect.getmembers(module_obj):
        if inspect.isclass(obj) and BasePipeline in inspect.getmro(obj) and obj is not BasePipeline:
            return obj


@click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
@click.option('--entry', prompt='Point of entry as module_name.method or simply module_name',
              help='This should be provided in the form of <module name>.<method name>')
@click.option('--folder', prompt='Folder containing the target pipeline to run')
@click.pass_context
def runner(ctx, **kwargs):
    entry = expander(kwargs['entry'])
    folder = expander(kwargs['folder'])
    sys.path.append(folder)

    param_values = parse_params(ctx.args)

    if "." in entry:
        module_str, func_str = entry.rsplit(".", 1)
        module_obj = __import__(module_str)
        func_obj = getattr(module_obj, func_str)
        return func_obj(param_values)
    else:
        module_str = entry
        module_obj = __import__(module_str)
        pipeline_class = get_pipeline_class(module_obj)
        if not hasattr(pipeline_class, "run"):
            raise ValueError(pipeline_class, "does not have a proper run(params) method")
        pipeline_obj = pipeline_class()
        pipeline_obj.run(param_values)


if __name__ == '__main__':
    runner()
