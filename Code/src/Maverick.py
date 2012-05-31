import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
 
class ExitListener(ogre.FrameListener):
 
	def __init__(self, keyboard):
		ogre.FrameListener.__init__(self)
		self.keyboard = keyboard
 
	def frameStarted(self, evt):
		self.keyboard.capture()
		return not self.keyboard.isKeyDown(OIS.KC_ESCAPE)
 
	def __del__(self):
		del self.renderer
		del self.system
		del self.exitListener
		del self.root
 
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
		
		sceneManager.ambientLight = (0, 0, 0)
		sceneManager.shadowTechnique = ogre.SHADOWTYPE_STENCIL_ADDITIVE
 
		# Setup a mesh object.
		ent = sceneManager.createEntity('Ninja', 'ninja.mesh')
		ent.castShadows = True
		sceneManager.getRootSceneNode().createChildSceneNode().attachObject(ent)
 
		# Setup a ground plane.
		plane = ogre.Plane ((0, 1, 0), 0)
		meshManager = ogre.MeshManager.getSingleton ()
		meshManager.createPlane ('Ground', 'General', plane,
									 1500, 1500, 20, 20, True, 1, 5, 5, (0, 0, 1))
		ent = sceneManager.createEntity('GroundEntity', 'Ground')
		sceneManager.getRootSceneNode().createChildSceneNode ().attachObject (ent)
		ent.setMaterialName ('Examples/Rockwall')
		ent.castShadows = False
 
		# Setup a point light.
		light = sceneManager.createLight ('PointLight')
		light.type = ogre.Light.LT_POINT
		light.position = (150, 300, 150)
		light.diffuseColour = (.5, .0, .0)    # Red
		light.specularColour = (.5, .0, .0)
 
		# Setup a distant directional light.
		light = sceneManager.createLight ('DirectionalLight')
		light.type = ogre.Light.LT_DIRECTIONAL
		light.diffuseColour = (.5, .5, .0)    # yellow
		light.specularColour = (.75, .75, .75)
		light.direction = (0, -1, 1)
 
		# Setup a spot light.
		light = sceneManager.createLight ('SpotLight')
		light.type = ogre.Light.LT_SPOTLIGHT
		light.diffuseColour = (0, 0, .5)    # Blue
		light.specularColour = (0, 0, .5)
		light.direction = (-1, -1, 0)
		light.position = (300, 300, 0)
		light.setSpotlightRange (ogre.Degree (35), ogre.Degree (50))

		camera = sceneManager.createCamera("Camera")
		camera.position = (0, 150, -500)
		camera.lookAt ((0, 0, 0))
		camera.nearClipDistance = 5
		
		viewPort = self.root.getAutoCreatedWindow().addViewport(camera)
		camera.aspectRatio = float (viewPort.actualWidth) / float (viewPort.actualHeight)


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
			self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, False)
			self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, False)
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
		self.exitListener = ExitListener(self.keyboard)
		self.root.addFrameListener(self.exitListener)
 
	# This is the rendering loop
	def startRenderLoop(self):
		self.root.startRendering()
 
	# In the end, clean everything up (= delete)
	def cleanUp(self):
		self.inputManager.destroyInputObjectKeyboard(self.keyboard)
		self.inputManager.destroyInputObjectMouse(self.mouse)
		OIS.InputManager.destroyInputSystem(self.inputManager)
		self.inputManager = None
 
if __name__ == '__main__':
	try:
		ta = Application()
		ta.go()
	except ogre.OgreException, e:
		print e