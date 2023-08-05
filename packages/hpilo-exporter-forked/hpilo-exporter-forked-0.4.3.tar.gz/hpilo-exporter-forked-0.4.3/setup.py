import io
from setuptools import setup, find_packages

VERSION = "0.4.3"
PACKAGE_NAME = "hpilo-exporter-forked"
SOURCE_DIR_NAME = "src"


def readme():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Prometheus exporter for HP iLO metrics",
    author="Example Name",
    author_email="example.name@infinityworks.com",
    long_description=readme(),
    url="https://github.com/ivorcheung/hpilo-exporter",
    package_dir={'': SOURCE_DIR_NAME},
    packages=find_packages(SOURCE_DIR_NAME, exclude=('*.tests',)),
    include_package_data=True,
    zip_safe=False,
    package_data={},
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        "prometheus-client",
        "python-hpilo",
        "lmdb",
        "pandas",
        "Paver",
    ],
    entry_points={
        'console_scripts': [
            'hpilo-exporter = hpilo_exporter.main:main',
        ],
    }
)
