from setuptools import find_namespace_packages


try:  
  from setuptools import setup
except Exception as e:
    print(e)
    exit()

setup(
    name='project',
    version="0.0.1",
    packages=find_namespace_packages(where='scripts/modules'),
    package_dir={"": "scripts/modules"},
    entry_points={
        'console_scripts' : [
            'mycommand = scripts.__main__:main',
        ]
    },
    install_requires=[
        'requests',
    ]
)