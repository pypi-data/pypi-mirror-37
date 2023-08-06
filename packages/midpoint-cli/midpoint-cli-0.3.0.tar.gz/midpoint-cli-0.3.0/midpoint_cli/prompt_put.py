from argparse import ArgumentParser, RawTextHelpFormatter

put_parser = ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    prog='put',
    description='Create or update a server object.',
    epilog='')
put_parser.add_argument('-p', '--patch', help='Patch the object according to the following patch file.', action='store')
put_parser.add_argument('file', help='Load XML data from this file.')


class PutClientPrompt:
    def do_put(self, inp):
        try:
            put_args = inp.split()
            ns = put_parser.parse_args(put_args)

            self.client.put_xml(ns.file, ns.patch)

        except SystemExit:
            pass

    def help_put(self):
        put_parser.print_help()
