from setuptools import setup, find_packages
from os.path import join, dirname
import versioneer

project = "klocmod"
version = versioneer.get_version()

setup(
    name=project,
    version=version,
    cmdclass=versioneer.get_cmdclass(),
    description="A simple module providing facilities to localize small programs via textual files.",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    keywords="localization library",
    author="Leonid Kozarin",
    author_email="kozalo@sadbot.ru",
    url="https://github.com/kozalosev/klocmod",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'YAML': ['PyYAML']
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', project),
            'version': ('setup.py', version)
        }
    }
)
