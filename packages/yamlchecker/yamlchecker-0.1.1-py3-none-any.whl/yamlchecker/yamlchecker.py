"""Module for verify test cases YAML-files."""
from itertools import chain
from pathlib import Path
import sys

import click
import markdown
import yaml
from yamllint.config import YamlLintConfig
import yamllint.linter as linter


@click.command()
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    """Command-line interface for YAMLchecker."""
    sys.exit(yaml_checker(path))


def yaml_checker(path):
    """Read all yaml files in the directory and verify structure.

    :param str path: Path to test cases.

    :return: Number of errors.
    :rtype: int
    """
    path_for_check = Path(path)
    if path_for_check.is_dir():
        file_list = chain(path_for_check.glob('**/*.yaml'), path_for_check.glob('**/*.yml'))
    else:
        file_list = [path_for_check]
    error_count = 0
    for file_name in file_list:
        print('=== Parsing {} ==='.format(file_name))
        with open(file_name) as file:
            text = file.read()
        conf = YamlLintConfig('document-start:\n'
                              '  present: false\n'
                              'rules:\n'
                              '  line-length:\n'
                              '    max: 250\n'
                              '    allow-non-breakable-words: false\n'
                              '    allow-non-breakable-inline-mappings: true\n')
        for err in linter.run(text, conf):
            print(err)
            error_count += 1
        try:
            test_case = yaml.load(text)
        except Exception:
            error_count += 1
            print('*** Error load YAML ***')
        else:
            error_count += check_section(test_case, 'Description', is_markdown=True)
            error_count += check_section(test_case, 'Requirements')
            if not check_section(test_case, 'Steps'):
                for step_count, step in enumerate(test_case['Steps'], 1):
                    error_count += check_section(step, 'Description', step_count, is_markdown=True)
                    error_count += check_section(step, 'Expected result', step_count, is_markdown=True)
            else:
                error_count += 1
    print('\n\t{} errors were found'.format(error_count))
    return error_count


def check_section(test_case, section, step=0, is_markdown=False):
    """Verify section.

    :param dict test_case: Test case or step of test case.
    :param str section: Test case or step section name.
    :param int step: Number of step for Steps section.
    :param bool is_markdown: True, if it is necessary to check of markdown.

    :return: Number of errors.
    :rtype: int
    """
    if step:
        msg_open = '*** Error open {} section for step {} ***'
        msg_parse = '*** Error parse {} section for step {} ***'
    else:
        msg_open = '*** Error open {} section ***'
        msg_parse = '*** Error parse {} section ***'
    try:
        text = test_case[section]
    except (KeyError, IndexError):
        print(msg_open.format(section, step))
        return 1
    if is_markdown and not markdown.markdown(text):
        print(msg_parse.format(section, step))
        return 1
    return 0


if __name__ == '__main__':
    cli()
