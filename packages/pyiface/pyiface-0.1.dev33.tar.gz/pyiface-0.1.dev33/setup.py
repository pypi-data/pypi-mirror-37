from setuptools import setup

def myversion():
    from setuptools_scm.version import get_local_dirty_tag
    def clean_scheme(version):
        return (get_local_dirty_tag(version) if version.dirty else '+clean').split('+')[0]

    return {'local_scheme': clean_scheme}


setup(
    name='pyiface',
    author='Sergey Kostov',
    author_email='bat.serjo@gmail.com',
    packages=['pyiface'],
    scripts=[],
    url='http://pypi.python.org/pypi/pyiface/',
    python_requires='>=2',
    license='LICENSE.txt',
    description='View and control network interfaces. Linux only currently! Join us lets make it available for other OSes',
    long_description=open('README.rst').read(),
    install_requires=[],
	use_scm_version=myversion,
    setup_requires=['setuptools_scm'],
)
