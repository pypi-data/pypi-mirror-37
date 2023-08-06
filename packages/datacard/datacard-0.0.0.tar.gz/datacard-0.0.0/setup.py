import os

from setuptools import find_packages, setup

import versioneer


install_requires = [
    # 'numpy', #etc
]

docs_extras = ['ipykernel', 'jupyter', 'matplotlib', 'pillow', 'sphinx', 'sphinx-gallery']
dev_extras = [
    'check-manifest', 'coverage', 'isort', 'mypy', 'pylint', 'pytest', 'yapf',
]

extras_require = {
    'dev': dev_extras,
    'docs': docs_extras,
}

# Add a `pip install .[all]` target:
all_extras = set()
for extras_list in extras_require.values():
    all_extras.update(extras_list)
extras_require['all'] = list(all_extras)

version = versioneer.get_version()

project_repo_dir = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(project_repo_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='datacard',
    version=version,
    cmdclass=versioneer.get_cmdclass(),
    description='Generate a report card for your data.',
    long_description=long_description,
    # The project's main homepage.
    url='https://mindfoundry.ai',
    # Author details
    author='Mind Foundry Ltd',
    author_email='tim.staley@mindfoundry.ai',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    license="MIT",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
)
