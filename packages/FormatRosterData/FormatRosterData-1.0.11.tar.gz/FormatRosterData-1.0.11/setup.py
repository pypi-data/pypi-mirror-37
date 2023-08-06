from setuptools import setup
#from cx_Freeze import setup,Executable
import os

cRequires = ('TM_CommonPy','nose','openpyxl', 'requests', 'lxml')

setup(name='FormatRosterData'
    ,version='1.0.11'
    ,description=''
    ,author='Troy1010'
    #,author_email=''
    #,url=''
    ,license=''
    ,packages=['FormatRosterData']
    ,zip_safe=False
    ,test_suite='nose.collector'
    ,tests_require=[*cRequires]
    ,python_requires=">=3.6"
    ,install_requires=[*cRequires]
    ,setup_requires=[*cRequires]
    #,executables = [Executable("Main.py")]
    )
