from os import path

from setuptools import setup, find_packages

BASE_PATH = path.abspath(path.dirname(__file__))

with open(path.join(BASE_PATH, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='slack-notifications',
    packages=find_packages(include=('slack_notifications', 'slack_notifications.*')),
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    description='Send notifications to slack channel with supporting attachments and fields',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Mikhail Trifonov',
    author_email='trifonov.net@gmail.com',
    url='https://github.com/qa-team-tools/slack-notifications',
    py_modules=['slack_notifications'],
    install_requires=[
        'requests',
    ],
    keywords='slack notifications',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
