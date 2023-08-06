from setuptools import setup, find_packages

setup(
    name='tmux_list_learner',
    version='0.0.2',
    description='List learning tool using tmux windows',
    url='https://github.com/flaxandteal/tmux_list_learner',
    author='Phil Weir',
    author_email='phil.weir@flaxandteal.co.uk',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='tmux learning',
    install_requires=[
        'Click',
        'pyyaml',
        'appdirs'
    ],
    entry_points='''
        [console_scripts]
        tmux-list-learner=tmux_list_learner.scripts.tmux_list_learner:cli
    '''
)
