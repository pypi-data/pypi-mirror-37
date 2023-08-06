from argparse import ArgumentParser, RawTextHelpFormatter

import tabulate

# Task command wrapper parser

task_parser = ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    prog='task',
    description='Manage server tasks.',
    epilog='''
Available commands:
  ls       List all server tasks.
  run      Run task(s) sequentially.
  suspend  Suspend task(s).
  resume   Resume task(s).
''')
task_parser.add_argument('command', help='Task command to execute.')
task_parser.add_argument('arg', help='Optional command arguments.', nargs='*')

# Task RUN parser

task_run_parser = ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    prog='task run',
    description='Run tasks synchronously.',
)
task_run_parser.add_argument('task', help='Task to be run. Can be an OID or a task name.', nargs='+')


class TaskClientPrompt:

    def do_task(self, inp):
        try:
            task_args = inp.split()
            ns = task_parser.parse_args(task_args)

            if ns.command == 'ls':
                tasks = self.client.get_tasks()
                print(tabulate.tabulate(tasks, headers='keys'))
            if ns.command in ['run', 'resume', 'suspend']:
                run_ns = task_run_parser.parse_args(task_args[1:])
                tasks = self.client.get_tasks()

                for task_id in run_ns.task:
                    print('Handling task', task_id, '...')
                    task_obj = tasks.find_object(task_id)

                    if task_obj is None:
                        print('Task reference not found:', task_id)

                    self.client.task_action(task_obj.get_oid(), ns.command)


        except SystemExit:
            pass

    def help_task(self):
        task_parser.print_help()

    def do_tasks(self, inp):
        self.do_task('ls')

    def help_tasks(self):
        print('List all server tasks. This is a shortcut for "task ls"')
