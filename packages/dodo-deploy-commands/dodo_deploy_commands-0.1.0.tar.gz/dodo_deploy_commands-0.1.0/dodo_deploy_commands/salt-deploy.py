from argparse import ArgumentParser
from dodo_commands.framework import Dodo
import os
import uuid
from dodo_ssh_agent_commands._utils import (add_ssh_agent_args, run_ssh_server,
                                            commit_ssh_server)


def _args():  # noqa
    parser = ArgumentParser(
        description=('Deploys a salt script to a ssh server'))
    parser.add_argument(
        "--src",
        dest="salt_src_dir",
        help='Source directory to share with the salt container')
    parser.add_argument(
        "--top",
        dest="top_dir",
        help='Path relative to salt_src_dir with the salt top file')
    parser.add_argument("--docker-image", dest="target_docker_image")
    parser.add_argument(
        "--debug", action="store_true", help='Only apply the debug.sls state')
    parser.add_argument(
        "--bash",
        action="store_true",
        help='Drop into a bash shell instead of calling salt')
    parser.add_argument("hostname")

    args = Dodo.parse_args(parser)
    args.salt_src_dir = args.salt_src_dir or Dodo.get_config('/SALT/src_dir')
    args.top_dir = args.top_dir or Dodo.get_config('/SALT/top_dir', '.')
    args.salt_top_dir = os.path.join(args.salt_src_dir, args.top_dir)
    args.target_docker_image = args.target_docker_image or Dodo.get_config(
        '/SALT/target_docker_image', None)
    if args.target_docker_image:
        args.ssh_public_key = os.path.expandvars(
            '$HOME/.ssh/%s.pub' % Dodo.get_config('/SSH/key_name'))
    args.salt_master_docker_image = Dodo.get_config('/SALT/docker_image')
    args.srv_salt_src_dir = '/srv/salt-deploy/src'
    args.srv_salt_top_dir = os.path.join(args.srv_salt_src_dir, args.top_dir)

    return args


def _write_roster_file(target_ip, target_container_name, salt_top_dir,
                       hostname):
    roster_filename = os.path.join(salt_top_dir,
                                   '.roster.%s' % target_container_name)
    with open(roster_filename, 'w') as ofs:
        ofs.write("%s:\n" % hostname)
        ofs.write("    host: %s\n" % target_ip)
        ofs.write("    priv: agent-forwarding\n")
    return roster_filename


salt_master_template = """
file_roots:
  base:
    - {srv_salt_top_dir}

pillar_roots:
  base:
    - {srv_salt_top_dir}/pillar
"""


def _write_salt_master_file(salt_top_dir, srv_salt_top_dir):
    salt_master_filename = os.path.join(salt_top_dir,
                                        '.master.%s' % uuid.uuid4().hex)
    with open(salt_master_filename, 'w') as ofs:
        ofs.write(
            salt_master_template.format(srv_salt_top_dir=srv_salt_top_dir))
    return salt_master_filename


if Dodo.is_main(__name__):
    args = _args()

    if args.target_docker_image:
        target_ip, target_container_name = run_ssh_server(
            args.ssh_public_key, args.target_docker_image)
        salt_master_container_name = (
            'salt_master_deploying_to_%s' % target_container_name)
        roster_filename = _write_roster_file(target_ip, target_container_name,
                                             args.salt_top_dir, args.hostname)
    else:
        salt_master_container_name = 'salt_master_deploying_to_%s' % args.hostname
        roster_filename = "roster"

    salt_master_filename = _write_salt_master_file(
        args.salt_top_dir,
        args.srv_salt_top_dir,
    )

    Dodo.config['DOCKER']['options'] = {
        Dodo.command_name:
        add_ssh_agent_args({
            'volume_map': {
                args.salt_src_dir: args.srv_salt_src_dir,
                salt_master_filename: '/etc/salt/master'
            },
            'name': salt_master_container_name,
            'image': 'vegtech/salt'
        })
    }

    if args.bash:
        cmd = ['/bin/bash']
    else:
        cmd = ([
            'salt-ssh',  # '-l', 'debug',
            '-i',
            '--roster-file=./%s' % os.path.basename(roster_filename),
            args.hostname
        ] + (['state.sls', 'debug'] if args.debug else ['state.apply']))

    decorators = Dodo.config['ROOT']['decorators'].setdefault('docker', [])
    decorators.append(Dodo.command_name)
    Dodo.runcmd(cmd, cwd=args.srv_salt_top_dir)
    decorators.remove(Dodo.command_name)

    os.unlink(salt_master_filename)
    if args.target_docker_image:
        commit_ssh_server(target_container_name, args.target_docker_image)
        os.unlink(roster_filename)
