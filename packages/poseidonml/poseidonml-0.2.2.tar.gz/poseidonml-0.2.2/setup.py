from setuptools import setup

setup(
    name='poseidonml',
    version='0.2.2',
    packages=['poseidonml'],
    package_dir={'poseidonml': 'utils'},
    package_data={'poseidonml': ['models/*']},
    install_requires=['numpy==1.15.1', 'pika==0.12.0', 'redis==2.10.6',
                      'scikit-learn==0.20.0', 'scipy==1.1.0', 'tensorflow==1.11.0'],
    license='Apache License 2.0',
    author='cglewis',
    author_email='clewis@iqt.org',
    maintainer='Charlie Lewis',
    maintainer_email='clewis@iqt.org',
    description=(
        'A utility package for extracting and analyzing features in network traffic.'),
    keywords='machine learning network analysis utilities',
    url='https://github.com/CyberReboot/PoseidonML',
)
