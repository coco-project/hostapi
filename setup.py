from setuptools import setup, find_packages

setup(
    name="coco-hostapi",
    description="Package containing the executable & library for the host API component.",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['coco'],
    install_requires=[
        'coco-backends',
        'coco-contract',
        'Flask==0.10.1',
        'psutil==3.1.1'
    ],
    entry_points={'console_scripts': ['coco_hostapi = coco.hostapi.cli.server:main']}
)
