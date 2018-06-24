from setuptools import setup

setup(name='roboemotion',
	version='1.0.2',
	description='emotion expressing for robotic arms',
	url='https://github.com/chengjovy/RoboEmotion',
	author='Jovy Cheng',
	author_email='chengjovy83@gmail.com',
	license='MIT',
	packages=['roboemotion'],
	install_requires=[
		'serial',
	],
	data_files=[
		('roboemotion', ['robo_emotion_config.json'])
	],
	zip_safe=False)
