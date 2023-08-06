import sys
import time
import firebase

from datetime import datetime
from threading import Thread
from django.conf import settings
from django.core.management.base import BaseCommand





class MonitoredCommand(BaseCommand):
    """
    Monitoring the running command.
    """

    def __init__(self):

        super(MonitoredCommand, self).__init__()

        self.command_name = ''
        self.arguments_passed = []
        self.command_id = ''

        # Logging
        self.started = self.utc_time
        self.finished = None
        self.alive = True

        # Settings
        self.ping_interval = 10.0  # secs

    @property
    def utc_time(self):

        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def run_from_argv(self, argv):

        self.arguments_passed = argv[2:]

        super(MonitoredCommand, self).run_from_argv(argv)

    def create_parser(self, prog_name, subcommand):

        parser = super(MonitoredCommand, self).create_parser(prog_name, subcommand)

        parser.add_argument(
            '--env',
            help='Define the type of the environment: dev, staging, prod.',
            type=str,
            choices=['dev', 'staging', 'prod'],
            dest='environment',
            default='dev'
        )

        parser.add_argument(
            "--disable_monitor",
            action='store_true',
            dest="disable_monitor",
            help="Disable monitoring in this command",
        )

        self.command_name = subcommand

        return parser

    def execute(self, *args, **options):

        def _handle_execute(self, progress_doc, results):
            failed = False
            output = None

            try:
                output = super(MonitoredCommand, self).execute(*args, **options)
            except Exception as e:
                failed = True
                progress_doc.update({
                    'status': 'FAILED',
                    'finished': self.utc_time,
                    'message': str(e),
                    'exeption_type': str(sys.exc_info()),
                })
                self._write_log(progress_doc)

            results.append([output, failed])

        # Disable monitoring
        if options['disable_monitor'] or \
                (not getattr(settings, 'MONITORING', True)) or \
                (getattr(settings, 'TESTING', False)):
            return super(MonitoredCommand, self).execute(*args, **options)

        # Check to see if the interval ping is set
        interval_ping = getattr(settings, 'INTERVAL_PING', 30)

        results = [['', False], ]

        self.command_id = self.command_name + '__' + '__'.join(
            [x.replace('-', '').replace('=', '_') for x in self.arguments_passed]
        )

        progress_doc = {
            'id': self.command_id,
            'name': self.command_name,
            'status': 'STARTED',
            'started': self.started,
            'latest': self.started,
            'finished': self.finished,
            'message': 'Command started',
            'exception_type': None,
            'params': ', '.join([x.replace('-', '') for x in self.arguments_passed])
        }

        # Initiate the command log in firebase
        current_index = self.initialize_firebase(progress_doc)

        if options['verbosity'] > 1:
            print('Monitoring command: %s' % self.command_id)

        # Run the command
        worker = Thread(target=_handle_execute, args=(self, progress_doc, results))
        worker.start()

        while worker.isAlive():
            for _ in range(0, interval_ping * 10):
                worker.join(0.1)

            if not results[-1][1]:
                progress_doc.update({
                    'status': 'RUNNING',
                    'latest': self.utc_time,
                    'message': 'Command running',
                })
                self._write_log(progress_doc, action_id=current_index)

        if not results[-1][1]:
            progress_doc.update({
                'status': 'FINISHED',
                'finished': self.utc_time,
                'message': 'Command finished',
            })
            self._write_log(progress_doc)

        return results[-1][0]

    def _write_log(self, progress_doc=None, action_id=0):
        """
        Write the log of the command to firebase
        :param progress_doc: dictionary
        :param method: string, one of post, patch, delete, etc
        """
        # results = self._read_write_firebase(method='get',
        #                                     data=None,
        #                                     action='%s/commands/%s/log' % (settings.FIREBASE_MONITORING_KEY,
        #                                                                    str(self.command_id)))
        try:
            # if len(results) > 1:
            #     new_progress = results[:-1]
            #     new_progress.append(progress_doc)
            # else:
            #     new_progress = [progress_doc]

            self._read_write_firebase(method='patch',
                                      data=progress_doc,
                                      action='%s/commands/%s/log/%d' % (settings.FIREBASE_MONITORING_KEY,
                                                                 str(self.command_id), action_id))
        except TypeError:
            self.initialize_firebase(progress_doc)

    def _read_write_firebase(self, method, data, action):
        app = firebase.FirebaseApplication(settings.FIREBASE_MONITORING['NAME'])

        # Make sure the folder we are writing to is monitoring
        action = 'monitoring/' + action

        tries = 3
        results = None

        while tries > 0:
            try:

                if method == 'get':
                    results = app.get(action, None)
                elif method == 'patch':
                    app.patch(action, data)
                else:
                    raise NotImplementedError('Invalid action: %s' % action)

                break
            except Exception as e:
                print(e)
                print('Retrying...')
            finally:
                tries -= 1

        return results

    def initialize_firebase(self, progress_doc):

        results = self._read_write_firebase(method='get',
                                            data=None,
                                            action='%s/commands/%s/log' % (settings.FIREBASE_MONITORING_KEY,
                                                                           str(self.command_id)))
        if not results:
            new_results = [progress_doc]
        else:
            new_results = results[::]
            if (new_results[-1].get('status', '') == 'RUNNING') or (new_results[-1].get('status', '') == 'STARTED'):
                new_results[-1]['status'] = 'SYSTEM_KILL'
                new_results[-1]['finished'] = self.utc_time
            new_results.append(progress_doc)

        current_index = len(new_results) - 1

        self._read_write_firebase(method='patch',
                                  data={'log': new_results},
                                  action='%s/commands/%s/' % (settings.FIREBASE_MONITORING_KEY, str(self.command_id)))

        return current_index
