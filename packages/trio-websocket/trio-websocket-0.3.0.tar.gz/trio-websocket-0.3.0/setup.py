from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

# Get version
version = {}
with (here / "trio_websocket" / "version.py").open() as f:
    exec(f.read(), version)


# Get description
with (here / 'README.md').open(encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='trio-websocket',
    version=version['__version__'],
    description='WebSocket library for Trio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HyperionGray/trio-websocket',
    author='Mark E. Haase',
    author_email='mehaase@gmail.com',
    classifiers=[
        # See https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires=">=3.5",
    keywords='websocket client server trio',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    install_requires=[
        'async_generator',
        'attrs>=18.2',
        'ipaddress',
        'sphinxcontrib-trio',
        'trio>=0.9,<0.10.0',
        'wsaccel',
        'wsproto>=0.12.0',
        'yarl'
    ],
    extras_require={
        'dev': [
            'coveralls',
            'pytest>=3.6',
            'pytest-cov',
            'pytest-trio>=0.5.0',
            'sphinx',
            'sphinx_rtd_theme',
            'trustme',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/HyperionGray/trio-websocket/issues',
        'Source': 'https://github.com/HyperionGray/trio-websocket',
    },
)
