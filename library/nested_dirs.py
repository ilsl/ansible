#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
import os
from functools import reduce
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nested_dirs

description: This module takes a path as a parameter and returns a nested dictionary as output. 

author:
    - Isobel Jones
'''

EXAMPLES = r'''
# pass in a message and have changed true
- name: run the new module
  nested_dirs:
    root_path: "{{ role_path }}/code_ci/tests/"
  register: testout
'''

RETURN = r'''
# These are examples of possible return values.
nested_dict:
    description: The
    type: dict
    returned: always
    sample: {'integration': {}, 'performance': {'scheduler': {}}}}
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        root_path=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        nested_dict='',
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    """
    Creates a nested dictionary that represents the folder structure of root_path
    """
    try:
        dir = {}
        rootdir = module.params['root_path'].rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1

        for path, dirs, _ in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(dirs)
            parent = reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir

        nested_dir = list(dir.values())[0]

        result["nested_dict"] = nested_dir

    except OSError as error:
        module.fail_json(msg='os Exception: ' + error, **result)


    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if result["nested_dict"]:
        result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
