from setuptools import setup, find_packages
from saltant_cli.version import NAME, DESCRIPTION, VERSION


# Parse readme to include in PyPI page
with open('README.md') as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mwiens91/saltant-cli',
    author='Matt Wiens',
    author_email='mwiens91@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['saltant-cli = saltant_cli.main:main'],
    },
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        'Click',
        'click-completion',
        'click-spinner',
        'colorama',
        'PyYAML',
        'saltant-py',
        'tabulate',
    ],
)
