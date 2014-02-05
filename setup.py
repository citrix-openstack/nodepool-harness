from setuptools import setup


setup(
    name='nodepool_harness',
    version='0.1dev',
    description='Nodepool harness',
    packages=['nodepool_harness', 'statsd', 'apscheduler'],
    install_requires=["PyYAML", "python-novaclient", "paramiko", "sqlalchemy"],
    entry_points = {
        'console_scripts': [
            'nh-install-node = nodepool_harness.scripts:install_node',
        ]
    }
)