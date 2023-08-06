from setuptools import find_packages,setup

packages=find_packages()
print('found packages:',packages)
setup(
    name='brainnetworks',
    version='0.3.1',
    packages=packages,
    include_package_data=True,
    license='MIT License',
    long_description=open('README.md').read(),
)
