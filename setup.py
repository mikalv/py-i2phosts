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
	    'pyi2phosts.jump',
	    'pyi2phosts.extsources',
	    'pyi2phosts.other',
	    'pyi2phosts.lib',],
    package_dir = {'pyi2phosts': 'web'},
    package_data = {
	    'pyi2phosts': ['templates/postkey.html', 'templates/success_submission.html',
		    'templates/local/policy.html', 'templates/base.html', 'templates/index.html',
		    'templates/404.html', 'templates/jump*', 'templates/admin/base_site.html']},
    scripts=['py-i2phosts-master', 'py-i2phosts-builder', 'py-i2phosts-checker',
	    'py-i2phosts-fetcher', 'py-i2phosts-injector', 'py-i2phosts-maint'],
    data_files=[('/etc/py-i2phosts', ['conf/master.conf', 'conf/checker.conf', 'conf/fetcher.conf',
	    'conf/maintainer.conf', 'conf/builder.conf', 'conf/common.conf', 'conf/injector.conf'],),],
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
