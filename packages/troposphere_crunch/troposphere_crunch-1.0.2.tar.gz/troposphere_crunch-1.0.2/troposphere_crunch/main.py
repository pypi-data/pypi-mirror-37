import argparse
import importlib
import os
import pathlib
import shutil
import subprocess
import sys

import toml
from tqdm import tqdm

from .types import Stack

BAR_FMT = '{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} [{elapsed}]'


def main() -> int:
    # Needed for the config file to be able to define "myaws.myfile" and have
    # this script actually be able to access it (since "myaws.myfile" is not
    # part of site-packages or troposphere-crunch itself
    sys.path.insert(0, os.getcwd())

    parser = argparse.ArgumentParser(description=(
        'A tool to compile and (optionally) deploy Troposphere templates with AWS CLI and a very '
        'opinionated structure'
    ))
    parser.add_argument(
        '-c', '--config',
        type=str, help='path to TOML config file', required=True,
    )
    parser.add_argument(
        '-C', '--clean', action='store_true',
        help='remove output_dir before building templates', required=False,
    )
    parser.add_argument(
        '-d', '--deploy', action='store_true',
        help='after building, actually deploy stacks with awscli', required=False,
    )
    parser.add_argument(
        '-o', '--output-dir',
        type=str, help='default output directory (overridable per stack in config)',
        required=False, default='cloudformation',
    )

    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = toml.load(config_file)

    stacks = []

    for stack in config['stacks']:
        stack_kwargs = {
            'module': importlib.import_module(stack['module']),
            'output_dir': args.output_dir,
        }

        if 'capabilities' in stack:
            stack_kwargs['capabilities'] = tuple(stack['capabilities'])

        if 'region' in stack:
            stack_kwargs['region'] = stack['region']

        if 'output_dir' in stack:
            stack_kwargs['output_dir'] = stack['output_dir']

        if 'parameters' in stack:
            stack_kwargs['parameters'] = stack['parameters']

        stacks.append(Stack(**stack_kwargs))

    if args.clean:
        output_dirs = {stack.output_dir for stack in stacks}

        for output_dir in output_dirs:
            try:
                shutil.rmtree(output_dir)
            except FileNotFoundError:
                pass

    for stack in tqdm(stacks, desc='Building stacks', unit='stacks', bar_format=BAR_FMT):
        pathlib.Path('cloudformation').mkdir(parents=True, exist_ok=True)

        with open(stack.json_filename, 'w') as cf_file:
            cf_file.write(stack.module.template.to_json())

    if args.deploy:
        deploy_results = []

        for stack in tqdm(stacks, desc='Deploying stacks', unit='stacks', bar_format=BAR_FMT):
            command = [
                'aws',
                'cloudformation',
                'deploy',
                '--region',
                stack.region,
                '--stack-name',
                stack.name,
                '--template-file',
                stack.json_filename,
            ]

            for capability in stack.capabilities:
                command.append('--capabilities')
                command.append(capability)

            if stack.parameters:
                command.append('--parameter-overrides')
                command.append(' '.join(
                    f'{k}={v}'
                    for k, v in stack.parameters.items()
                ))

            deploy_results.append((stack.name, subprocess.run(command, capture_output=True)))

        errors = []

        for r in deploy_results:
            _, result = r

            if result.returncode != 0:
                stderr = result.stderr.decode('utf-8')

                if 'No changes to deploy' in stderr:
                    continue

                errors.append(r)

        if errors:
            print('Some stacks failed to deploy!', file=sys.stderr)

            for stack_name, result in errors:
                if result.returncode != 0:
                    stdout = result.stdout.decode('utf-8')
                    if stdout:
                        print(f'---> {stack_name} stdout', file=sys.stderr)
                        print(stdout)
                        print()

                    stderr = result.stderr.decode('utf-8')
                    if stderr:
                        print(f'---> {stack_name} stderr', file=sys.stderr)
                        print(stderr)
                        print()

            return 1

    return 0
