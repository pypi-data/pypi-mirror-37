# -*- coding: utf-8 -*-

"""
Populates a provided Cloudbreak Instance with resources for Demos

Warnings:
    Experimental
"""

from __future__ import absolute_import
import logging
import os
import sys
import nipyapi

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.getLogger('nipyapi.deploy').setLevel(logging.INFO)


# 'horton' is a shared state function to make deployment more readable
# to non-python users
horton = nipyapi.deploy.Horton()


def step_1_init(secrets_file='.secrets.yaml'):
    log.info("------------- Loading Horton's Secrets")
    horton.secret = nipyapi.utils.load(nipyapi.utils.fs_read(secrets_file))
    log.info("Fetching Horton's Resources")
    if horton.find('secret:control:defs:filepath'):
        log.info("Loading demo definitions from file path [%s]:[%s]",
                 horton.find('secret:control:defs:filepath'),
                 horton.find('secret:control:defs:resources'))
        horton.resources = nipyapi.utils.load_resources_from_files(
            os.path.join(
                horton.find('secret:control:defs:filepath'),
                horton.find('secret:control:defs:resources')
            )
        )
    elif horton.find('secret:control:defs:repo'):
        log.info("loading demo definitions from repo [%s]",
                 horton.find('secret:control:defs:repo'))
        horton.resources = nipyapi.utils.load_resources_from_github(
            repo_name=horton.find('secret:control:defs:repo'),
            username=horton.find('secret:github:username'),
            token=horton.find('secret:github:token'),
            tgt_dir=horton.find('secret:control:defs:resources')
        )
    else:
        raise ValueError("control defs must point to a resource dir of demo "
                         "defs")
    log.info("Populating Horton's demo definitions")
    horton.defs = [
        y for x, y in horton.find('resources:demo').items()
    ]

    # --- Set Cloudbreak Server
    url = 'https://' + horton.find('secret:cloudbreak:hostname') + '/cb/api'
    log.info("Setting endpoint to %s", url)
    nipyapi.utils.set_endpoint(url)

    # --- Login
    log.info("------------- logging into cloudbreak")
    auth_success = nipyapi.security.service_login(
        service='cloudbreak',
        username=horton.find('secret:cloudbreak:username'),
        password=horton.find('secret:cloudbreak:password'),
        bool_response=False
    )
    if not auth_success:
        raise ConnectionError("Couldn't login to Cloudbreak")
    else:
        log.info('Logged into Cloudbreak at [%s]', url)


def step_2_prepare_dependencies():
    # --- Create credential if not exists
    log.info("------------- Creating Horton's Credential, if not exists")
    name = horton.find('secret:deploycred:name')
    prefix = horton.find('secret:control:namespace')
    name = prefix + name if prefix else name
    if name not in [x.name for x in nipyapi.deploy.list_credentials()]:
        horton.cred = nipyapi.deploy.create_credential(
            horton=horton
        )
    else:
        horton.cred = nipyapi.deploy.get_credential(name)
    log.info("Got Credential [%s]", horton.cred.name)

    log.info("------------- Preparing Horton's Demo Dependencies")
    nipyapi.deploy.prep_dependencies(horton=horton)


def step_3_create_specs():
    log.info("------------- Preparing Horton's Stack Specs")
    nipyapi.deploy.prep_stack_specs(horton=horton)


def step_4_deploy_stacks(priority_only=True):
    # --- Deploy Demos
    log.info("------------- Creating Prioritised list of Demo Specs")
    to_deploy = {}
    to_delay = {}
    for demo_def in horton.defs:
        name = demo_def['name']
        spec = horton.specs[name]
        control = demo_def['control']
        if 'priority' in demo_def and demo_def['priority'] is not None:
            priority = demo_def['priority']
            log.info("Found Priority [%d] for Demo [%s], prioritising...",
                     priority, name)
            to_deploy[priority] = name, spec, control
        else:
            if priority_only:
                log.info("Priority-Only is True and No Priority found for "
                         "Demo [%s], skipping...", name)
            else:
                log.info("Priority-Only is False and No Priority found for "
                         "Demo [%s], delaying...", name)
                to_delay[name] = name, spec, control
    if to_delay:
        p_index = sorted(to_deploy.keys())[-1] + 1
        for name, details in to_delay.items():
            to_deploy[p_index] = details
            p_index += 1
    log.info("List of Demos to deploy is [%s]",
             str(sorted(to_deploy.keys())))
    for li in sorted(to_deploy):
        name, spec, control = to_deploy[li]
        log.info("submitting stack creation request for demo [%s]", name)
        if control['deploywait']:
            max_wait = control['deploywait']
        else:
            max_wait = False
        horton.stacks.append(
            nipyapi.deploy.create_stack(
                spec=spec,
                wait=max_wait
            )
        )


def autorun(secrets_file='.secrets.yaml'):
    step_1_init(secrets_file=secrets_file)
    step_2_prepare_dependencies()
    step_3_create_specs()
    step_4_deploy_stacks()


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'script accepts only 1 argument as the path to'\
                               ' a secrets yaml file'
    autorun(secrets_file=sys.argv[1])
    exit(0)
