Wrapper for Ansible cli.
========================

Usage
=====

*  `pm-execute [ansible command name] [args]` - calls any ansible cli tool.
*  `pm-cli-reference [ansible command name,...] [--exclude key]` -
    output cli keys for command. Default - all. Exclude keys by names (support many).
    Now support output only __'ansible'__, __'ansible-playbook'__ and
    __'ansible-galaxy'__.
*  `python -m pm_ansible [reference/ansible_command]` - run as module. 
   For output reference use __'reference'__, or full ansible command. 
*  `python -m pm_ansible [--detail] [--get]` -
    Output modules reference. 

Contribution
============

We use `tox` for tests and deploy. Just run `tox -e py27-coverage,py36-coverage,flake`
for full tests with coverage output. It's small project and 
we strictly adhere to the full (__100%__) code coverage.
