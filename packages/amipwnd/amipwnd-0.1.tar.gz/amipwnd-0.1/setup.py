from setuptools import setup

setup(
    name="amipwnd",
    version='0.1',
    py_modules=['amipwnd'],
    install_requires=[
        'Click',
        'ascii-graph',
        'numpy',
        'requests',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        amipwnd-cli=amipwnd.amipwnd_cli:cli
    ''',
)
