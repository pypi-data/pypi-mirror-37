from setuptools import setup, find_packages


setup(name='mroylib_min',
    version='1.9.2',
    description='some libs',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['redis','tornado', 'pymysql', 'xlrd','xlwt','bs4','requests','termcolor','bson','simplejson','pysocks','telethon'],
    entry_points={
        'console_scripts' : [
            'Mr=mroylib.cmd:main',
            'repo-upload=mroylib.api:repo_upload_client',
            'm-server=mroylib.servers.tornado:main',
        ]
    }
)


