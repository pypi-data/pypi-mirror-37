#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import click

from .main import main

from punica.compile.contract_compile import PunicaCompiler


@main.command('compile')
@click.argument('contract_name', required=1, nargs=1)
@click.option('--avm', nargs=1, type=str, default=False, help='Only generate avm file flag.')
@click.option('--abi', nargs=1, type=str, default=False, help='Only generate abi file flag.')
@click.pass_context
def compile_cmd(ctx, contract_name, avm, abi):
    """
    Compile the specified contracts to avm and abi file.
    """
    project_dir = ctx.obj['PROJECT_DIR']
    contract_path = os.path.join(project_dir, contract_name)
    print('Compile...')
    if avm:
        PunicaCompiler.generate_avm_file(contract_path)
        print('\tGenerate avm file successful...')
    if abi:
        PunicaCompiler.generate_abi_file(contract_path)
        print('\tGenerate abi file successful...')
    if not avm and not abi:
        PunicaCompiler.compile_contract(contract_path)
        print('\tGenerate abi file and avm file successful...')
    print('Enjoy your contract:)')
