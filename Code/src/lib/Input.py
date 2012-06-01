import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI

_keyDict = {
	'Q': OIS.KC_Q,
	'W': OIS.KC_W,
	'E': OIS.KC_E,
	'R': OIS.KC_R,
	'T': OIS.KC_T,
	'Y': OIS.KC_Y,
	'U': OIS.KC_U,
	'I': OIS.KC_I,
	'O': OIS.KC_O,
	'P': OIS.KC_P,
	'A': OIS.KC_A,
	'S': OIS.KC_S,
	'D': OIS.KC_D,
	'F': OIS.KC_F,
	'G': OIS.KC_G,
	'H': OIS.KC_H,
	'J': OIS.KC_J,
	'K': OIS.KC_K,
	'L': OIS.KC_L,
	'Z': OIS.KC_Z,
	'X': OIS.KC_X,
	'C': OIS.KC_C,
	'V': OIS.KC_V,
	'B': OIS.KC_B,
	'N': OIS.KC_N,
	'M': OIS.KC_M
}
_keyFuncDict = {}
_keyboard = False
_mouse = False
_frameListener = False

def init(keyboard, mouse):
	global _keyboard
	_keyboard = keyboard
	global _mouse
	_mouse = mouse
	global _frameListener
	_frameListener = InputListener(_keyboard)

def onKey(which, func):
	_keyFuncDict[which] = func

def getFrameListener():
	return _frameListener

class InputListener(ogre.FrameListener):
 
	def __init__(self, keyboard):
		ogre.FrameListener.__init__(self)
		self.keyboard = keyboard
 
	def frameStarted(self, evt):
		self.keyboard.capture()

		for k,v in _keyDict.items():
			if self.keyboard.isKeyDown(v) and k in _keyFuncDict:
				_keyFuncDict[k]()
		return not self.keyboard.isKeyDown(OIS.KC_ESCAPE)