from __future__ import print_function

import sys, json, thread, pkg_resources
from time import sleep
from util import SerialCorrespondent, StandardErrorCorrespondent
from move import Move


class RoboEmotion(object):

	_DEFAULT_EMOTION_MOVES = {
		"happy":    None,
		"sad":      None,
		"fear":     None,
		"anger":    None,
		"surprise": None,
		"disgust":  None
	}
	_DEFAULT_EMOTION_CONFIG = "robo_emotion_config.json"

	def __init__(self, defaultEmotionConfig=None, correspondent=None):
		#
		# initialize _DEFAULT_EMOTION_MOVES
		#
		if defaultEmotionConfig is not None:
			RoboEmotion._DEFAULT_EMOTION_CONFIG = defaultEmotionConfig
		f = pkg_resources.resource_stream(__name__, RoboEmotion._DEFAULT_EMOTION_CONFIG)
		# fileContent = json.load(open(RoboEmotion._DEFAULT_EMOTION_CONFIG, 'r'))
		fileContent = json.load(f)
		try:
			assert type(fileContent) == type({})
		except:
			raise ValueError("should be a dictionary mapping emotion name to its move (%s)" % (RoboEmotion._DEFAULT_EMOTION_CONFIG))
		for emotionName in fileContent:
			RoboEmotion._DEFAULT_EMOTION_MOVES[emotionName.lower()] = Move(fromServoConfig=fileContent[emotionName])
		#
		# initialize correspondent if necessary
		#
		if correspondent:
			self.correspondent = correspondent
		else:
			self.correspondent = StandardErrorCorrespondent()
		#
		# performing
		#
		self.currentMove = None
		self.finishCriteria = None
		#
		# start communication
		#
		thread.start_new_thread(self._communicate, ())

	def perform(self, move, finishCriteria=Move._FINISH_CRITERIA_ALL, noReset=False):
		if noReset:
			self.currentMove = move
		else:
			move.reset()
			self.currentMove = move
		self.finishCriteria = finishCriteria

	def performEmotion(self, emotionName, finishCriteria=Move._FINISH_CRITERIA_ALL):
		emotionMove = RoboEmotion._DEFAULT_EMOTION_MOVES.get(emotionName.lower())
		if emotionMove is not None:
			emotionMove.reset()
			self.currentMove = emotionMove
			self.finishCriteria = finishCriteria
		else:
			raise ValueError('cannot recognize this emotion: %s' % (emotionName))

	def getNext(self):
		if self.currentMove is not None:
			return self.currentMove.getNext()
		else:
			return RoboEmotion._DEFAULT_EMOTION_MOVES['init'].getNext()

	def isFinished(self):
		return (self.currentMove is None) or (self.currentMove.isFinished(criteria=self.finishCriteria))

	def _communicate(self):
		lastPositions = None
		while True:
			positions = self.getNext()
			positions = " ".join([str(p) for p in positions])
			if lastPositions is None or lastPositions != positions:
				lastPositions = positions
				self.correspondent.write(positions + "\n")
			sleep(0.1)

def communicate(serialCorrespondent=None):
	if roboEmotion is not None:
		lastPositions = None
		while True:
			positions = roboEmotion.getNext()
			positions = " ".join([str(p) for p in positions])
			if lastPositions is None or lastPositions != positions:
				lastPositions = positions
				print(positions)
				if serialCorrespondent is not None:
					serialCorrespondent.write(positions + "\n")
			sleep(0.1)

if __name__ == "__main__":
	import tkinter as tk
	roboEmotion = RoboEmotion()
	try:
		serialCorrespondent = SerialCorrespondent(serialIdentifier=sys.argv[1], baudRate=9600)
	except:
		serialCorrespondent = SerialCorrespondent(serialIdentifier="/dev/cu.usbmodem95", baudRate=9600)
	serialCorrespondent.connect()

	root = tk.Tk()

	w = tk.Button(root, text='init', command=lambda: roboEmotion.performEmotion('init'))
	w.pack(padx=10)
	w = tk.Button(root, text='happy', command=lambda: roboEmotion.performEmotion('happy'))
	w.pack(padx=10)
	w = tk.Button(root, text='sad', command=lambda: roboEmotion.performEmotion('sad'))
	w.pack(padx=10)
	w = tk.Button(root, text='fear', command=lambda: roboEmotion.performEmotion('fear'))
	w.pack(padx=10)
	w = tk.Button(root, text='anger', command=lambda: roboEmotion.performEmotion('anger'))
	w.pack(padx=10)
	w = tk.Button(root, text='surprise', command=lambda: roboEmotion.performEmotion('surprise'))
	w.pack(padx=10)
	w = tk.Button(root, text='disgust', command=lambda: roboEmotion.performEmotion('disgust'))
	w.pack(padx=10)

	thread.start_new_thread(communicate, (serialCorrespondent,))
	# start Tkinter
	root.mainloop()
