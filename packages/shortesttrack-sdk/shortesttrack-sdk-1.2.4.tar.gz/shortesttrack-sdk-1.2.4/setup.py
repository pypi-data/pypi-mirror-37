from setuptools import setup, find_packages

setup(
    name='shortesttrack-sdk',
    version='1.2.4',
    description='SDK for work with ShortestTrack API',
    packages=find_packages(),
    install_requires=[
        'URLObject',
        'requests',
        'setuptools',
        'shortesttrack-tools==0.1.2'
    ],
    author='Stanislav Pospelov',
    author_email='stpospelov@shtr.io',
    license='MIT'
)
