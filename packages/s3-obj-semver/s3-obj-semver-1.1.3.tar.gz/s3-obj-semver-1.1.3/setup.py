from setuptools import setup, find_packages

def long_description():
    with open('README.rst', 'r') as fileobj:
        return fileobj.read()

setup(
    name='s3-obj-semver',
    version='1.1.3',
    url='https://newops.cn',
    license='MIT',
    author='wangsir',
    author_email='wanglin@dbca.cn',
    description=u'从对象存储中，按semver规则获取最大版本号',
    long_description=long_description(),
    packages=find_packages(),
    install_requires=[
	'boto3==1.9.18',
	'cos-python-sdk-v5==1.5.8',
	'minio==4.0.5',
	'semver==2.8.1'
    ],
    entry_points={
        'console_scripts': [
            's3-obj-semver=s3pkg.cmd:main'
        ]
    }
)
