from setuptools import setup

requires = ['pyyaml']
setup(
    name='paspas',
    version='0.0.1',
    packages=['paspas'],
    description='Simple password generator for CLI',
    url='https://github.com/hirokikana/paspas',
    author='Hiroki Takayasu',
    author_email='hiroki.kana@gmail.com',
    license='MIT',
    scripts=['bin/paspas'],
    install_requires=requires,
)
