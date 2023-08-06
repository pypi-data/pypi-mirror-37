# noqa
from plumbum.cmd import docker, grep, awk
import os
import sys
from argparse import ArgumentParser
from dodo_commands.framework import Dodo, CommandError


def _args():  # noqa
    parser = ArgumentParser(
        description=('Runs ssh-agent in a docker container'))
    parser.add_argument(
        "command", choices=['start', 'stop', 'restart', 'status'])
    args = Dodo.parse_args(parser)
    args.image_name = Dodo.get_config('/SSH_AGENT/docker_image')
    return args


if Dodo.is_main(__name__):
    args = _args()

    for i in range(2):
        try:
            # Find agent container id
            try:
                container_id = (docker['ps', '-a'] | grep['ssh-agent']
                                | awk['{print $1}'])()[:-1]
            except:
                container_id = None

            # Stop command
            if args.command in ('stop', 'restart') and container_id:
                Dodo.runcmd(
                    [
                        'docker', 'run', '--rm', '--volumes-from=ssh-agent',
                        '-it', args.image_name, 'ssh-add', '-D'
                    ],
                    quiet=True)

                Dodo.runcmd(['docker', 'rm', '-f', container_id])
                if args.command in ('stop', ):
                    sys.exit(0)

            elif args.command == 'status':
                print("running" if container_id else "stopped")

            elif args.command in ('start', 'restart'):
                # If container is already running, exit.
                if container_id:
                    raise CommandError(
                        "A container named 'ssh-agent' is already running.")

                # Run ssh-agent
                Dodo.runcmd([
                    'docker', 'run', '-d', '--name=ssh-agent', args.image_name
                ], )

                # Add ssh keys to the ssh-agent container
                ssh_host_dir = os.path.expandvars('$HOME/.ssh')

                for key in Dodo.get_config("/SSH_AGENT/key_names"):
                    Dodo.runcmd([
                        'docker', 'run', '--rm', '--volumes-from=ssh-agent',
                        '-v',
                        '%s:/.ssh' % ssh_host_dir, '-it', args.image_name,
                        'ssh-add', key
                    ])

                print("ssh-agent is now ready to use")
                break
        except:
            pass
