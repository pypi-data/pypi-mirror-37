from django.contrib.staticfiles.management.commands.runserver import (
    Command as BaseRunserverCommand
)
from django.core.management.base import CommandError
from django.conf import settings


class Command(BaseRunserverCommand):

    default_remote_debug_port = 3000
    default_remote_debug_addr = '0.0.0.0'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument(
            '--remote-debug', action='store_true', dest='remote_debug',
            help='Starts remote debugging server.',
        )

    def handle(self, *args, **options):
        self.remote_debug_port = getattr(
            settings, 'REMOTE_DEBUG_PORT', self.default_remote_debug_port)
        self.remote_debug_addr = getattr(
            settings, 'REMOTE_DEBUG_ADDR', self.default_remote_debug_addr)

        super(Command, self).handle(*args, **options)

    def inner_run(self, *args, **options):
        if options['remote_debug']:
            try:
                import ptvsd
            except ImportError:
                raise CommandError('PTVSd not installed')
            else:
                ptvsd.enable_attach(
                    address=(self.remote_debug_addr, self.remote_debug_port),
                    redirect_output=True
                )

        super(Command, self).inner_run(*args, **options)
