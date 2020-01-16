#!/usr/bin/env python
#
# Copyright (C) 2016-2020 Jingcheng Yang <yjcyxky@163.com>
#

import os
import re
import sys
import click
import jinja2
import yaml


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


def matched(line):
    regex_rule = [
        r'^127.0.0.1',
        r'^255',
        r'^#',
        r'^::1'
    ]
    
    return bool(len([rule for rule in regex_rule if re.match(rule, line)]))


def not_matched(line):
    return not matched(line)


def gen_map(node_name, ip_addr, port, user):
    return {
        "node_name": node_name,
        "ip_addr": ip_addr,
        "port": port,
        "user": user
    }


def parse_hosts(hosts, port=22, user="root"):
    hosts = list(filter(not_matched, hosts))
    legal_host_lst = []
    for host in hosts:
        items = host.split()
        nodes = [gen_map(item, items[0], port, user) for item in items[1:]]
        legal_host_lst.extend(nodes)
        
    return legal_host_lst


def render(config_vars, template_file, template_dir="."):
    jinja2.filters.FILTERS["zip"] = zip
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    if not os.path.isfile(os.path.join(template_dir, template_file)):
        print("No such file: %s" % template_file)
        sys.exit(1)
    template = template_env.get_template(template_file)
    rendered_text = template.render(config_vars)
    return rendered_text


@click.group()
def config_cli():
    pass


@config_cli.command(help="Config cluster manager.")
@click.option("--node-name", "-n", help="Node name", default="manager")
@click.option("--ip-addr", "-i", help="IP address", default="127.0.0.1")
@click.option("--port", "-p", help="SSH Port", default="22")
@click.option("--user", "-u", help="Username", default="root")
def config(node_name, ip_addr, port, user):
    import json

    manager = {
        "node_name": node_name,
        "ip": ip_addr,
        "port": port,
        "user": user
    }

    with open("/etc/hosts", "r") as f:
        hosts = f.readlines()

    nodes = parse_hosts(hosts, port, user)
    rendered_text = render({ "manager": manager, "nodes": nodes }, 'hosts', template_dir=TEMPLATE_DIR)

    with open(os.path.join(BASE_DIR, "playbook", "hosts"), "w") as f:
        f.write(rendered_text)

    print("Manager: \n", json.dumps(manager, indent=2, sort_keys=True))
    print("\nCompute Nodes: \n", json.dumps(nodes, indent=2, sort_keys=True))
    print("\nGenerate hosts successfully.")


@click.group()
def version_cli():
    pass


@version_cli.command(help="Show version.")
def version():
    from manager.version import get_version
    print("Cluster Manager: %s" % get_version())


@click.group()
def useradd_cli():
    pass


@useradd_cli.command(help="Create a new user.")
@click.option("--username", "-u", help="Username", default=None)
@click.option("--home-directory", "-h", help="Home Directory", default=None)
def useradd(username, home_directory):
    if username:
        import subprocess

        current_user = os.getlogin()
        if current_user != 'root':
            print("You may need to login as root.")
            sys.exit(1)

        if home_directory is None:
            home = "/home/%s" % username

        password = username
        playbook = os.path.join(BASE_DIR, "playbook")

        cmd = 'cd %s && ansible-playbook deploy_useradd.yml --extra-vars "username=%s password=%s home=%s" --ask-become-pass' % (playbook, username, password, home)

        try:
            # Create a new user.
            subprocess.run(cmd, shell=True, universal_newlines=True, check=True)
        except Exception as err:
            print(str(err))
    else:
        print("You must specify username.")


@click.group()
def trust_cli():
    pass


@trust_cli.command(help="Set SSH trust.")
@click.option("--username", "-u", help="Username", default=None)
def trust(username):
    import subprocess
    import  socket
    from getpass import getpass

    if not username:
        username = os.getlogin()

    management_console = socket.gethostname()
    # TODO: how to deal with custom ssh port
    port = 22

    playbook = os.path.join(BASE_DIR, "playbook")
    password = getpass("Enter %s's password (connect to %s): " % (username, management_console))

    cmd = 'cd %s && ansible-playbook deploy_trust.yml --extra-vars "username=%s ssh_port=%s management_console=%s password=%s"' % (playbook, username, port, management_console, password)

    try:
        # Set SSH trust for the user (username)
        subprocess.run(cmd, shell=True, universal_newlines=True, check=True)
    except Exception as err:
        print(str(err))


cli = click.CommandCollection(sources=[version_cli, useradd_cli, config_cli, trust_cli])

if __name__ == "__main__":
    cli()
