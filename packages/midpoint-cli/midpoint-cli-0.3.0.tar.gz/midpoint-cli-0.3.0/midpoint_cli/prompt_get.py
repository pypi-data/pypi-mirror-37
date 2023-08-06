from argparse import ArgumentParser, RawTextHelpFormatter

get_parser = ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    prog='get',
    description='Get a server object.',
    epilog='')
get_parser.add_argument('objectclass', help='Type of the object to fetch (Java Type).')
get_parser.add_argument('oid', help='Object ID.')
get_parser.add_argument('file', help='Save the XML data to this file.', nargs='?')


class GetClientPrompt:
    def do_get(self, inp):
        try:
            get_args = inp.split()
            ns = get_parser.parse_args(get_args)

            xml = self.client.get_xml(ns.objectclass, ns.oid)

            if ns.file is None:
                print(xml)
            else:
                with open(ns.file, 'w') as f:
                    f.write(xml)

        except AttributeError as e:
            print('Error:', e)
        except SystemExit:
            pass

    def help_get(self):
        get_parser.print_help()
