from distutils.core import setup
#from pip.req import parse_requirements
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]
install_reqs = parse_requirements("ros/requirements.txt") #, session="i")
requirements = [str(r) for r in install_reqs]
setup(
    name = 'ros',
    packages = [ 'ros' ], # this must be the same as the name above
    package_data={ 'ros' : [
        'requirements.txt',
        '*.ros',
        '*.yaml',
        'bin/*',
        'lib/*',
        'workflow/*',
        'dag/*'
    ]},
    version = '0.096',
    description = 'Ros Knowledge Network',
    author = 'Steve Cox',
    author_email = 'scox@renci.org',
    install_requires = requirements,
    include_package_data=True,
    entry_points = {
        'console_scripts': ['ros=ros.dag.run_tasks:main'],
    },
    url = 'http://github.com/NCATS-Tangerine/ros.git',
    download_url = 'http://github.com/NCATS-Tangerine/ros/archive/0.1.tar.gz',
    keywords = [ 'knowledge', 'network', 'graph', 'biomedical' ],
    classifiers = [ ],
)
