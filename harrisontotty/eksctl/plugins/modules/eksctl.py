#!/usr/bin/env python3
'''
Runs eksctl
'''
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import subprocess
import yaml

from ansible.module_utils.basic import AnsibleModule

def run_module():
    '''
    Create an EKS
    '''
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        version=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        output='',
        exit_code=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    config = {
        'apiVersion': 'eksctl.io/v1alpha5',
        'kind': 'ClusterConfig',
        'metadata': {
            'name': module.params['name'],
            'version': module.params['version']
        },
        'managedNodeGroups': [{
                'name': 'default',
                'amiFamily': 'AmazonLinux2',
                'desiredCapacity': 3,
                'instanceType': 'r5.xlarge',
                'maxSize': 5,
                'minSize': 3
        }]
    }

    process = subprocess.Popen(
        'eksctl create cluster -f -',
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        shell = True
    )
    output = process.communicate(input=yaml.safe_dump(config).encode())[0].decode('ascii', 'ignore')
    exit_code = process.returncode

    result['changed'] = True
    result['output'] = output
    result['exit_code'] = exit_code

def main():
    run_module()


if __name__ == '__main__':
    main()
