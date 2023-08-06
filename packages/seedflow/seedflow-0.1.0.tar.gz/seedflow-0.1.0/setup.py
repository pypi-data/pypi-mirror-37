"""Setup file for seedflow project."""


# [ Imports:Third Party ]
import setuptools


setuptools.setup(  # type: ignore
    name='seedflow',
    version='0.1.0',
    packages=setuptools.find_packages(),
    py_modules=['seedflow'],
    # a license
    license='MIT',
    # "classifiers", for reasons.  Below is adapted from the official docs at https://packaging.python.org/en/latest/distributing.html#classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    # keywords.  because classifiers are for serious metadata only?
    keywords="coroutines async side-effects data side-effects-as-data",
    install_requires=[
        'din',
        'rototiller',
    ],
    extras_require={
        'test': [
            'bandit',
            'better_exceptions',
            'blessed',
            'click',
            'dado',
            'flake8-assertive',
            'flake8-author',
            'flake8-blind-except',
            'flake8-bugbear',
            'flake8-builtins-unleashed',
            'flake8-commas',
            'flake8-comprehensions',
            'flake8-copyright',
            'flake8-debugger',
            'flake8-docstrings',
            'flake8-double-quotes',
            'flake8-expandtab',
            'flake8-imports',
            'flake8-logging-format',
            'flake8-mutable',
            'flake8-pep257',
            'flake8-self',
            'flake8-single-quotes',
            'flake8-super-call',
            'flake8-tidy-imports',
            'flake8-todo',
            'flake8',
            'mypy',
            'pylint',
            'pipe',
            'vulture',
        ],
        'dev': [
            'ptpython',
        ],
    },
)
