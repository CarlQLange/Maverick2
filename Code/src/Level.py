import ogre.renderer.OGRE as ogre

def	newLevel(sceneManager):
		sceneManager.ambientLight = (0, 0, 0)
		sceneManager.shadowTechnique = ogre.SHADOWTYPE_STENCIL_ADDITIVE
 
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