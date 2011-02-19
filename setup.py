from distutils.core import setup

setup(
    name='py-i2phosts',
    version='0.0.1',
    description='py-i2phosts is a host-add service application for I2P',
    author='Hidden Z',
    author_email='hiddenz@mail.i2p',
    url='http://py-i2phosts.i2p/',
    packages=['pyi2phosts',
	    'pyi2phosts.postkey',
	    'pyi2phosts.postkey.templatetags',
	    'pyi2phosts.jump',
	    'pyi2phosts.extsources',
	    'pyi2phosts.lib',
	    'pyi2phosts.search',
	    'pyi2phosts.latest'],
    package_dir = {'': ''},
    package_data = {
	    'pyi2phosts': ['templates/*.html', 'static/*', 'locale/*/*/*']},
    scripts=['py-i2phosts-master', 'py-i2phosts-builder', 'py-i2phosts-checker',
	    'py-i2phosts-fetcher', 'py-i2phosts-injector', 'py-i2phosts-maint'],
    data_files=[('/etc/py-i2phosts', ['conf/master.conf', 'conf/checker.conf', 'conf/fetcher.conf',
	    'conf/maintainer.conf', 'conf/builder.conf', 'conf/common.conf', 'conf/injector.conf'],),
	    ('/var/log/py-i2phosts', ['.placeholder'],)],
    classifiers=[
        'Development Status :: 4 - Beta',
	'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
	'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GPL License',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
