import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid >= 1.9a',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'transaction',
    'waitress',
    'Markdown',
    'PyYAML',
    'python-frontmatter',
    'watchdog < 0.9.0',
    'pyramid-htmlmin',
    'pyramid-webpack',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='flatfilecms',
    version='0.1',
    description='Radium CMS',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Anton Kasimov',
    author_email='kasimov@radium-it.ru',
    url='http://www.radium.group',
    keywords='web pyramid pylons flat-file CMS',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = flatfilecms:main',
        ],
        'console_scripts': [
            'generate_static_site = flatfilecms.scripts.generate:main',
        ],
    },
)
