from setuptools import find_packages, setup


setup(
    name='qx-data-storage',
    version='1.0.5',
    author='Shawn',
    author_email='q-x64@live.com',
    url='https://github.com/qx-oo/qx-data-storage/',
    description='Django data storage apps.',
    long_description=open("README.md").read(),
    packages=find_packages(exclude=["tests", "qx_test"]),
    install_requires=[
        'oss2==2.7.0',
        'pillow>=8.0.0',
        'Django >= 4.0',
    ],
    python_requires='>=3.9',
    platforms='any',
)
