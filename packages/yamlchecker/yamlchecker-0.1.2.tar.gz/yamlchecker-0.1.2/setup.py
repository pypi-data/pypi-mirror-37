from setuptools import setup, find_packages

setup(
    name='yamlchecker',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Markdown',
        'PyYAML',
        'yamllint',
    ],
    entry_points='''
        [console_scripts]
        yamlchecker=yamlchecker.yamlchecker:cli
    ''',
    url='',
    license='',
    author='kodSIM',
    author_email='',
    description='Checker for YAML test cases files'
)
