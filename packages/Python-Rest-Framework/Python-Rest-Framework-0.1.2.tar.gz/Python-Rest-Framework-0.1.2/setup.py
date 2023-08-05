import rest_framework
import os

from setuptools import setup, find_packages


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(
    name=rest_framework.__title__,
    version=rest_framework.__version__,
    packages=find_packages(exclude=('tests', 'docs')),  # Выбрасываем из сборки лишнее.
    include_package_data=True,  # Включаем данные пакета.
    test_suite='rest_framework.tests',  # Включаем тесты.
    license='Apache 2.0',  # Ставим лицензию
    description='Python Rest Framework. Box utils for easy makes rest api on python',
    long_description=README,
    url=rest_framework.__url__,
    author=rest_framework.__author__,
    author_email=rest_framework.__email__,
    maintainer=rest_framework.__author__,
    maintainer_email=rest_framework.__email__,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'six>=1',
    ]
)
