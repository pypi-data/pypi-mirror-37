from setuptools import setup, find_packages
from os import path


currdir = path.abspath(path.dirname(__file__))
with open(path.join(currdir, 'README.md')) as f:
    long_desc = f.read()
#long_rst_desc = convert(long_desc)

setup(
    name='Blask',
    version='0.1.0b15',
    packages=find_packages(exclude=['tests']),
    url='https://getblask.com',
    license='GPL 3.0',
    author='zerasul',
    author_email='zerasul@gmail.com',
    description='A simple Blog engine using Flask and Markdown.',
    classifiers=[
       'Development Status :: 4 - Beta',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
        [console_scripts]
        blaskcli=Blask.blaskcli:blaskcli
    ''',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=[
          'flask',
          'markdown',
          'markdown-full-yaml-metadata',
          'Pygments',
          'click'
          #'m2r'
    ],
    test_requires=[
        'pytest',
        'pytest-cov'
    ]
)
