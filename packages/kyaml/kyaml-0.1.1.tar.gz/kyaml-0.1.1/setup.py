"""
Utility to manipulate Kubernetes YAML files.

Note: This is entirely experimental at this point. Development may or may not
continue. All it does is split Kubernetes YAML files. It may grow new features
in the future. Public repo Coming Soon."""
from setuptools import find_packages, setup

dependencies = [
        'click',
        'pyyaml',
        "pathlib2 ; python_version<'3.4'",
        ]

setup(
    name='kyaml',
    version='0.1.1',
    #url='https://github.com/tylerdave/kyaml',
    license='BSD',
    author='Dave Forgac',
    author_email='tylerdave@tylerdave.com',
    description='Utility to manipulate Kubernetes YAML files.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'kyaml = kyaml.cli:kyaml',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
