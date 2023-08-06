from setuptools import setup, find_packages

setup(
    name='quartet_templates',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    url='https://gitlab.com/serial-lab/quartet_templates',
    license='GPLv3',
    author='SerialLab Corp',
    author_email='slab@serial-lab.com',
    description='Template package for QU4RTET',
    keywords=('seriallab, quartet '
              'level-4 quartet'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
