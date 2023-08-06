from setuptools import setup

setup(
        name='statsd_logger',
        version=open('VERSION').read(),
        install_requires=[
            'termcolor'
        ],
        author='Kaustubh Gadkari',
        author_email='kaustubh.gadkari@gmail.com',
        url='https://gitlab.com/kpgadkari/statsd-echo-server',
        description='Simple StatsD Echo Server',
        license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        packages=['statsd_logger'],
        zip_safe=False,
        python_requires='>=3.0.0, >=2.7.0',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
        long_description=open('README.md').read(),
        entry_points={
            'console_scripts': [
                'statsd_logger=statsd_logger.__main__:main'
            ]
        }
)
