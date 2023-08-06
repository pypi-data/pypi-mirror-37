# Copyright 2011 webapp3 AUTHORS.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from codecs import open

from setuptools import setup


LONG_DESCRIPTION = open('README.rst', 'r', encoding='utf-8').read()

REQUIREMENTS = [
    'webob>=1.2.0',
    'six>=1.10.0'
]

EXTRA_REQUIREMENTS = {
    'jinja2>=2.4',
    'Babel>=2.2',
    'pytz>=2015.7'
}

setup(
    name='webapp3',
    version='1.0.2',
    license='Apache Software License',
    description="Taking Google App Engine's webapp to the next next level!",
    long_description=LONG_DESCRIPTION,
    author='The Webapp3 Maintainers',
    author_email='camille.tolsa@gmail.com',
    zip_safe=False,
    platforms='any',
    py_modules=[
        'webapp3',
    ],
    packages=[
        'webapp3',
        'webapp3_extras',
        'webapp3_extras.appengine',
        'webapp3_extras.appengine.auth',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require={'extras': EXTRA_REQUIREMENTS},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
