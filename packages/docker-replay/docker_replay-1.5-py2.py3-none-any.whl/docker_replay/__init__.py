import os
import sys
import logging
from argparse import ArgumentParser

from docker_replay.version import version
from docker_replay.opts import config_disables

log = logging.getLogger('docker-replay')

class DockerReplay(object):
    def __init__(self, container_id, pretty_print=True):
        from docker import client, errors
        from docker_replay.parser import ConfigParser

        self.pretty_print = pretty_print

        c = client.from_env(version='auto')

        try:
            inspect = c.api.inspect_container(container_id)
            self.parser = ConfigParser(inspect)
        except errors.NotFound:
            print('no such container: %s' % container_id)
            sys.exit(1)

    def __str__(self):
        # remove conflicting options
        drop_opts = []
        for o in self.parser.opts:
            if o.name in config_disables:
                drop_opts += config_disables[o.name]

        output = sorted([ str(o) for o in self.parser.opts \
                if o.name not in drop_opts ])
        output += [ str(a) for a in self.parser.args ]

        if self.pretty_print:
            return 'docker run %s' % ' \\\n           '.join(output)
        return 'docker run %s' % ' '.join(output)

def main():
    argparser = ArgumentParser(description='docker-replay v%s' % version)
    argparser.add_argument('-d', '--debug', action='store_true',
                            help='enable debug output')
    argparser.add_argument('-p', '--pretty-print', action='store_true',
                            help='pretty-print output')
    argparser.add_argument('container',
                            help='container to generate command from')
    args = argparser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    print(DockerReplay(args.container, args.pretty_print))
