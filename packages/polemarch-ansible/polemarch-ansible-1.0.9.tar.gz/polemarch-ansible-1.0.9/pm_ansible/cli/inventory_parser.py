import sys
import json
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager


def parse_inventory(path):
    loader = DataLoader()
    inventory = InventoryManager(
        loader=loader,
        sources=path
    )
    data = dict(groups=[], hosts=[])

    for group in inventory.groups:
        if group == 'all' or group == 'ungrouped':
            continue
        group_data = dict(
            name=group,
            hosts=[],
            groups=[],
            vars=inventory.groups[group].vars
        )
        for host in inventory.groups[group].hosts:
            group_data['hosts'].append(host.name)
        for child_group in inventory.groups[group].child_groups:
            group_data['groups'].append(child_group.name)
        data['groups'].append(group_data)

    for host in inventory.hosts:
        host_data = dict(name=host, vars=inventory.hosts[host].vars)
        del host_data['vars']['inventory_file']
        del host_data['vars']['inventory_dir']
        data['hosts'].append(host_data)

    return json.dump(data, sys.stdout, indent=4)


def handler(args=sys.argv[1:]):
    return parse_inventory(args[0])
