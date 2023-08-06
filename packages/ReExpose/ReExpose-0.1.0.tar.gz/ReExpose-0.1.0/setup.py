from distutils.core import setup

setup(
    name='ReExpose',
    version='0.1.0',
    author='Jeff Casavant',
    author_email='jeff.casavant@gmail.com',
    description='ReExpose HTTP basic auth endpoints on localhost as unauthenticated endpoints',
    url='https://github.com/jeffcasavant/reexpose',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'cachetools',
        'flask',
        'gevent',
        'requests',
        'pyyaml'
    ],
    extras_require={
        'dev': [
            'pylint',
            'twine'
        ]
    },
    packages=['reexpose',],
    scripts=['bin/reexpose'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
