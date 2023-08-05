import logging
import argparse
import re
import json
import os.path
import sys
import warnings
import pkg_resources


__all__ = ['check_string', 'check_file']
__abs_path__ = os.path.abspath(os.path.dirname(__file__))
name = 'credsleuth'



class RulesEngine(object):
    __rules = []

    def __init__(self, rules=[]):
        self.rules = rules

    @property
    def rules(self):
        return self.__rules_json

    @rules.setter
    def rules(self, json=[]):
        self.__rules = []
        self.__rules_json = json

        for rule in json:
            # This template is used to expand matching to include the full line for non-multi line matches.
            template = "(.*{}.*)"
            try:
                if not rule['enabled']:
                    continue
            except KeyError:
                pass

            try:
                if rule['ignoreCase']:
                    flags = re.IGNORECASE
            except KeyError:
                flags = 0

            try:
                if rule['multi_line']:
                    flags |= re.DOTALL
                    template = "{}"
            except KeyError:
                pass

            self.__rules.append(
                {
                    "name": rule['name'],
                    "search": re.compile(template.format(rule['search']), flags)
                }
            )

        return self.rules

    def __iter__(self):
        self.n = 1
        while self.n < len(self.__rules):
            yield self.__rules[self.n]
            self.n += 1

    def __getitem__(self, item):
        return self.__rules[item]


class Matcher:

    def __init__(self, args):
        """
        :param filename: filename to parse
        """
        logging.debug("Running with {}".format(args))

        # Check that file provided exists is necessary.
        if args.type == "file":
            if not os.path.isfile(args.filename):
                logging.error("File not found {}".format(args.filename))
            data = open(args.filename, "r").read()
        elif args.type == "string":
            data = args.data
        else:
            raise NotImplemented("Available options are 'string' or 'file'.")

        rules = RulesEngine(json.loads(open(args.rules_file, 'r').read()))

        self.rules = rules
        self.rules.file = args.rules_file
        self.type = args.type
        self.data = data

    @staticmethod
    def __truncate_middle(data, length=80):
        if len(data) <= length:
            # string is already short-enough
            return data
        # half of the size, minus the 3 .'s
        tail = int(length) // 2 - 3
        # whatever's left
        prefix = length - tail - 3
        return '{0}...{1}'.format(data[:prefix], data[-tail:])

    def run(self):
        """

        :return:
        """

        issues = []

        for rule in self.rules:
            for match in rule['search'].finditer(self.data):
                line_number = self.data.count('\n', 0, match.start()) + 1

                try:
                    logging.info("{}:{}".format(line_number, match.group(0)))
                except IndexError:
                    pass

                issues.append({
                        'line_number' : line_number,
                        'match': match,
                        'name': rule['name'],
                        'data': self.__truncate_middle(match.group(0), 80)
                })

        return issues


class ConfigEngine(object):

    verbose = False
    rules_file = os.path.join(__abs_path__, "rules.json")
    filename = None
    data = None
    type = 'file'
    __verbose = False

    def __init__(self, attributes=False):
        """
        Leaving this as a placeholder to validate arguments provided.
        :param attributes: argparse parse object.
        """
        if not attributes:
            return

        for attr, value in vars(attributes).items():
            if hasattr(self, attr)\
                    and value != None:
                setattr(self, attr, value)

    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, value):
        if value:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)

        self.__verbose = value


def check_string(data, config=None):
    if not config:
        config = ConfigEngine()

    config.data = data
    config.type = 'string'

    matcher = Matcher(config)
    return matcher.run()


def check_file(filename, config=None):
    if not config:
        config = ConfigEngine()

    config.filename = filename
    config.type = 'file'

    matcher = Matcher(config)
    return matcher.run()


if not sys.warnoptions:
    warnings.simplefilter("ignore")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rules',         action="store", help="Custom rule file.", dest='rules_file')
    parser.add_argument('-v', '--verbose', action="store_true", help="Increase verbosity.")
    parser.add_argument('filename',        action="store", help="File to scan.")
    parser.parse_args()

    # Force type to be 'file'.
    parser.add_argument('--type', action="store", default="file")
    args = parser.parse_args()

    config = ConfigEngine(args)
    matcher = Matcher(config)
    print(matcher.run())
