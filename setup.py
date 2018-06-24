from setuptools import setup

setup(name='roboemotion',
	version='1.0.5',
	description='emotion expressing for robotic arms',
	url='https://github.com/chengjovy/RoboEmotion',
	author='Jovy Cheng',
	author_email='chengjovy83@gmail.com',
	license='MIT',
	packages=['roboemotion'],
	install_requires=[
		'serial',
	],
	package_data={
		'roboemotion': ['robo_emotion_config.json',],
	},
	include_package_data=True,
	zip_safe=False)
