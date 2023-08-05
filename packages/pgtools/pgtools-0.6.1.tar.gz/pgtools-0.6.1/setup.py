import setuptools

VER = '0.6.1'

print('*'*80)
print('* {:<76} *'.format('pgtools version {} by phageghost'.format(VER)))
print('*'*80)
print()

setuptools.setup(name='pgtools',
				version=VER,
				description='A collection of useful Python code, primarily focused on bioinformatics, with particular attention to working with HOMER', 
				url='http://github.com/phageghost/pg_tools',
				author='phageghost',
				author_email='pgtools@phageghost.net',
				license='MIT',
				packages=['pgtools'],
                install_requires=['numpy', 'scipy', 'pandas', 'seaborn', 'weblogo', 'intervaltree', 'matplotlib'],
				zip_safe=False)
