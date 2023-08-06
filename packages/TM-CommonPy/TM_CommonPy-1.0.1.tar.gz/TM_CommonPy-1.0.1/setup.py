from setuptools import setup

cRequires = ('dill','openpyxl')

setup(name='TM_CommonPy'
    ,version='1.0.1'
    ,description='Troy1010\'s common python library'
    ,author='Troy1010'
    #,author_email=''
    ,url='https://github.com/Troy1010/TM_CommonPy'
    ,license='MIT'
    ,packages=['TM_CommonPy']
    ,zip_safe=False
    ,test_suite='nose.collector'
    ,tests_require=['nose',*cRequires]
    ,python_requires=">=3.6"
    ,install_requires=[*cRequires]
    ,setup_requires=['nose',*cRequires]
    )
