from setuptools import setup, find_packages

setup(
    name='yamlspellchecker',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'nltk',
    ],
    entry_points='''
        [console_scripts]
        spellchecker=spellchecker.spellchecker:cli
    ''',
    url='',
    license='',
    author='kodSIM',
    author_email='',
    description='Spell checker for YAML files'
)
