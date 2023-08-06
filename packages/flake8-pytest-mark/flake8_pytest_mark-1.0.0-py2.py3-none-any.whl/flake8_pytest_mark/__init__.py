# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import ast
import re
from flake8_pytest_mark import rules

# ======================================================================================================================
# Globals
# ======================================================================================================================
__author__ = 'rpc-automation'
__email__ = 'rpc-automation@rackspace.com'
__version__ = '1.0.0'


# ======================================================================================================================
# Classes
# ======================================================================================================================
class MarkChecker(object):
    """
    Flake8 plugin to check the presence of test marks.
    """

    name = 'flake8-pytest-mark'
    version = __version__
    min_mark = 1
    max_mark = 50
    test_def_regex = re.compile(r'^(test_)|(Test)')
    pytest_marks = dict.fromkeys(["pytest_mark{}".format(x) for x in range(min_mark, max_mark)], {})

    # noinspection PyUnusedLocal,PyUnusedLocal
    def __init__(self, tree, filename, *args, **kwargs):
        """Required by flake8

        Args:
            tree (ast.AST): An AST tree. (Required by flake8, but never used by this plug-in)
            filename (str): The name of the file to evaluate.
            args (list): A list of positional arguments.
            kwargs (dict): A dictionary of keyword arguments.
        """

        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        """Required by flake8
        add the possible options, called first

        Args:
            parser (OptionsManager):
        """
        kwargs = {'action': 'store', 'default': '', 'parse_from_config': True,
                  'comma_separated_list': True}
        for num in range(cls.min_mark, cls.max_mark):
            parser.add_option(None, "--pytest-mark{}".format(num), **kwargs)

    @classmethod
    def parse_options(cls, options):
        """Required by flake8
        parse the options, called after add_options

        Args:
            options (dict): options to be parsed
        """

        d = {}
        acceptable_params = ['name',
                             'value_match',
                             'value_regex',
                             'allow_duplicate',
                             'allow_multiple_args',
                             'enforce_unique_value',
                             'exclude_classes',
                             'exclude_methods',
                             'exclude_functions']

        for pytest_mark, dictionary in cls.pytest_marks.items():
            # retrieve the marks from the passed options
            mark_data = getattr(options, pytest_mark)
            if len(mark_data) != 0:
                parsed_params = {}
                for single_line in mark_data:
                    a = [s.strip() for s in single_line.split('=')]
                    # whitelist the acceptable params
                    if a[0] in acceptable_params:
                        parsed_params[a[0]] = a[1]
                d[pytest_mark] = parsed_params

        cls.pytest_marks.update(d)

        # delete any empty rules
        cls.pytest_marks = {x: y for x, y in cls.pytest_marks.items() if len(y) > 0}

    def run(self):
        """Required by flake8
        will be called after add_options and parse_options

        Yields:
            tuple: (int, int, str, type) the tuple used by flake8 to construct a violation
        """

        rule_funcs = \
            (rules.rule_m3xx, rules.rule_m5xx, rules.rule_m6xx, rules.rule_m7xx, rules.rule_m8xx, rules.rule_m9xx)

        if len(self.pytest_marks) == 0:
            message = "M401 no configuration found for {}, " \
                      "please provide configured marks in a flake8 config".format(self.name)
            yield (0, 0, message, type(self))

        for node in ast.walk(self.tree):
            if type(node) in (ast.FunctionDef, ast.ClassDef) and self.test_def_regex.match(node.name):
                for rule_func in rule_funcs:
                    for rule_name, rule_conf in self.pytest_marks.items():
                        # Skip nodes that fail process evaluation
                        if not self._process_node_evaluation(rule_conf, node):
                            continue

                        for err in rule_func(node=node,
                                             rule_name=rule_name,
                                             rule_conf=rule_conf,
                                             class_type=type(self),
                                             filename=self.filename):
                            yield err

    @classmethod
    def _process_node_evaluation(cls, rule_conf, node):
        """Evaluate whether a node should be processed or not based on configuration options specified by the user.

        Args:
            rule_conf (dict): The rules configuration to use for evaluation.
            node (ast.stmt): The node under evaluation.

        Returns:
            bool: True if node should be processed by rules otherwise False.
        """

        process_conditions = [  # process if any of these are true
            cls._is_class_def(node) and not cls._get_value_default_to_false('exclude_classes', rule_conf),
            cls._is_function_def(node) and not cls._get_value_default_to_false('exclude_functions', rule_conf),
            cls._is_method_def(node) and not cls._get_value_default_to_false('exclude_methods', rule_conf)
        ]
        process_rule_flag = True if any(process_conditions) else False
        return process_rule_flag

    @classmethod
    def _is_function_def(cls, node):
        """Test if a node is a function definition

        Args:
            node (ast.stmt): The node under evaluation.

        Returns:
            bool: True if node is a function definition
        """
        r = True if type(node) == ast.FunctionDef and not cls._is_method_def(node) else False
        return r

    @classmethod
    def _is_method_def(cls, node):
        """Test if a node is a method definition

        Args:
            node (ast.stmt): The node under evaluation.

        Returns:
            bool: True if node is a method definition
        """
        if type(node) == ast.FunctionDef:
            if len(node.args.args) == 0:  # must have more than 0 args to be a method
                return False
            class_first_position_arguments = [getattr(node.args.args[0], 'id', '') == 'self',
                                              getattr(node.args.args[0], 'id', '') == 'cls',
                                              getattr(node.args.args[0], 'arg', '') == 'self',
                                              getattr(node.args.args[0], 'arg', '') == 'cls']
            if any(class_first_position_arguments):
                return True
        return False

    @classmethod
    def _is_class_def(cls, node):
        """Test if a node is a class definition

        Args:
            node (ast.stmt): The node under evaluation.

        Returns:
            bool: True if node is a class definition
        """
        r = True if type(node) == ast.ClassDef else False
        return r

    @classmethod
    def _get_value_default_to_false(cls, key, rule_conf):
        """Get the value for a key in a rule_conf

        Args:
            key (str): the key to get the value for
            rule_conf (dict): the rule configuration

        Returns:
            bool
        """
        try:
            if rule_conf[key].lower() == 'true':
                return True
            else:
                return False
        except KeyError:
            return False  # if the key is not present the default is false
