from setuptools import setup, find_packages
import io

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name='semversioner',
    version='0.2.0',
    description='Manager properly semver in your repository',
    long_description=readme,
    tests_require=['nose'],
    url='http://github.com/raulgomis/semversioner',
    author='Raul Gomis',
    author_email='rgomis@atlassian.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),

    entry_points={
        'console_scripts': [
            'semversioner = semversioner.__main__:main'
        ]
    },

    install_requires=[
        'click'
    ],
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'Topic :: Software Development :: Libraries :: Python Modules',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Operating System :: OS Independent',

    ],

)