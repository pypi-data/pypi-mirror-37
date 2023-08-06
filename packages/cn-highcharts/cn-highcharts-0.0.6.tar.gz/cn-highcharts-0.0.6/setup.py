from setuptools import setup, find_packages

setup(
    name='cn-highcharts',
    version='0.0.6',
    description=('Python Highcharts wrapper for china.'),
    install_requires=["Jinja2", "future"],
    # long_description=open('README.rst').read(),
    author='liubola',
    author_email='lby3523@gmail.com',
    # maintainer='<维护人员的名字>',
    # maintainer_email='<维护人员的邮件地址',
    license='GNU General Public License v3.0',
    packages=find_packages(),
    package_data={
        'highcharts.highcharts': ['templates/*.html'],
        'highcharts.highmaps': ['templates/*.html'],
        'highcharts.highstock': ['templates/*.html']
    },
    platforms=["all"],
    keywords=[
        'python', 'ipython', 'highcharts', 'chart', 'visualization', 'graph',
        'javascript', 'html'
    ],
    url='https://github.com/liubola/cn-highcharts',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
