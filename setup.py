from setuptools import setup, find_packages

setup(
    name="ipynbsrv-hostapi",
    description="Package containing the executable & library for the host API component.",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['ipynbsrv'],
    install_requires=[
        'ipynbsrv-backends',
        'ipynbsrv-contract',
        'Flask==0.10.1',
        'psutil==3.1.1'
    ],
    entry_points={'console_scripts': ['ipynbsrv_hostapi = ipynbsrv.hostapi.cli.server:main']}
)
