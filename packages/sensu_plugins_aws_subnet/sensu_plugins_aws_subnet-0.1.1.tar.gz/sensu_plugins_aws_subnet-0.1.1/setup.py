from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='sensu_plugins_aws_subnet',
    version='0.1.1',
    author='Binh Nguyen',
    author_email='binhnguyen@ebates.com',
    packages=['sensu_plugins_aws_subnet'],
    scripts=['bin/sensu-check-aws-subnet'],
    url='https://github.com/supernova106/sensu_plugins_aws_subnet',
    license='BSD',
    python_requires='>=3',
    description='A extention from Python sensu plugins framework to check aws subnet available IPs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'boto3',
        'ipaddress',
        'sensu_plugin'
    ],
)
