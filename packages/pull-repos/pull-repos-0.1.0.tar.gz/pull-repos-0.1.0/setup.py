from setuptools import setup


setup(
    name='pull-repos',
    version='0.1.0',
    author='Sergei Pikhovkin',
    author_email='s@pikhovkin.ru',
    license='MIT',
    description='Pull and update repositories',
    url='https://github.com/pikhovkin/pull-repos',
    scripts=[
        'pull_repos.py'
    ],
    entry_points={
        'console_scripts': [
            'pull-repos = pull_repos:execute_from_command_line'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
