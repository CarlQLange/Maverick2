import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI

import lib.Input as Input

import Level as Level

class Application(object):
 
	def go(self):
		self.createRoot()
		self.defineResources()
		self.setupRenderSystem()
		self.createRenderWindow()
		self.initializeResourceGroups()
		self.setupScene()
		self.setupInputSystem()
		self.setupCEGUI()
		self.createFrameListener()
		self.startRenderLoop()
		self.cleanUp()
 
	# The Root constructor for the ogre
	def createRoot(self):
		self.root = ogre.Root()
 
	# Here the resources are read from the resources.cfg
	def defineResources(self):
		cf = ogre.ConfigFile()
		cf.load("resources.cfg")
 
		seci = cf.getSectionIterator()
		while seci.hasMoreElements():
			secName = seci.peekNextKey()
			settings = seci.getNext()
 
			for item in settings:
				typeName = item.key
				archName = item.value
				ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
 
	# Create and configure the rendering system (either DirectX or OpenGL) here
	def setupRenderSystem(self):
		if not self.root.restoreConfig() and not self.root.showConfigDialog():
			raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")
 
 
	# Create the render window
	def createRenderWindow(self):
		self.root.initialise(True, "Maverick 2")
 
	# Initialize the resources here (which were read from resources.cfg in defineResources()
	def initializeResourceGroups(self):
		ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
		ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
 
	# Now, create a scene here. Three things that MUST BE done are sceneManager, camera and
	# viewport initializations
	def setupScene(self):
		sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")

		level = Level.newLevel(sceneManager)

		self.camera = sceneManager.createCamera("Camera")
		self.camera.position = (0, 150, -500)
		self.camera.lookAt ((0, 0, 0))
		self.camera.nearClipDistance = 5

		Input.onKey('W', self.forward)
		Input.onKey('S', self.back)
				
		viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
		self.camera.aspectRatio = float (viewPort.actualWidth) / float (viewPort.actualHeight)

	def forward(this):
		this.camera.position = (
			this.camera.position.x,
			this.camera.position.y,
			this.camera.position.z + 10
		)

	def back(this):
		this.camera.position = (
			this.camera.position.x,
			this.camera.position.y,
			this.camera.position.z - 10
		)


	# here setup the input system (OIS is the one preferred with Ogre3D)
	def setupInputSystem(self):
		windowHandle = 0
		renderWindow = self.root.getAutoCreatedWindow()
		windowHandle = renderWindow.getCustomAttributeInt("WINDOW")
		paramList = [("WINDOW", str(windowHandle))]
		self.inputManager = OIS.createPythonInputSystem(paramList)
 
		# Now InputManager is initialized for use. Keyboard and Mouse objects
		# must still be initialized separately
		try:
			Input.init(
				self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, False), 
				self.inputManager.createInputObjectMouse(OIS.OISMouse, False)
			)
		except Exception, e:
			raise e
 
 
	# CEGUI library is used for creating graphical user interfaces (options menus, etc)
	def setupCEGUI(self):
		sceneManager = self.root.getSceneManager("Default SceneManager")
		renderWindow = self.root.getAutoCreatedWindow()
		
		# CEGUI setup
		# The newer version of CEGUI has different syntax, so this tutorial code results 
		# in runnable program when used
		if CEGUI.Version__.startswith("0.6"):
			self.renderer = CEGUI.OgreCEGUIRenderer(renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, sceneManager)
			self.system = CEGUI.System(self.renderer)
		else:
			self.renderer = CEGUI.OgreRenderer.bootstrapSystem()
			self.system = CEGUI.System.getSingleton()
 
	# Create the frame listeners
	def createFrameListener(self):
		self.root.addFrameListener(Input.getFrameListener())
		
	# This is the rendering loop
	def startRenderLoop(self):
		self.root.startRendering()
 
	# In the end, clean everything up (= delete)
	def cleanUp(self):
		self.inputManager.destroyInputObjectKeyboard(Input._keyboard)
		self.inputManager.destroyInputObjectMouse(Input._mouse)
		OIS.InputManager.destroyInputSystem(self.inputManager)
		self.inputManager = None
 
if __name__ == '__main__':
	try:
		ta = Application()
		ta.go()
	except ogre.OgreException, e:
		print e