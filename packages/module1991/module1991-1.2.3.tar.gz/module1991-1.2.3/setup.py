from setuptools import setup,find_packages
__version__ = "1.2.3"
setup(name= "module1991",
	version="1.2.3",
	description="description",
	long_description="long_description",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3.6"],
	keywords='keywoards',
	url='http://vk.com',
	author='name lastname',
	author_email='email@gmail.com',
	license='Apache Software ',
	packages=find_packages(),
	install_requires=['opencv-python', 'bot_vk'],
	include_package_data=True,
	zip_safe=False
)