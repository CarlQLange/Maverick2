# This code is in the Public Domain
# -----------------------------------------------------------------------------
# This source file is part of Python-Ogre
# For the latest info, see http://python-ogre.org/
#
# It is likely based on original code from OGRE and/or PyOgre
# For the latest info, see http://www.ogre3d.org/
#
# You may use this sample code for anything you like, it is not covered by the
# LGPL.
# -----------------------------------------------------------------------------
import sys
sys.path.insert(0,'..')
import PythonOgreConfig

import ogre.renderer.OGRE as ogre
import SampleFramework as sf

class MaverickApplication(sf.Application):
    def _createScene(self):
        sceneManager = self.sceneManager

        # Accept default settings: point light, white diffuse, just set position
        light = sceneManager.createLight('MainLight')
        self.rotationNode = sceneManager.getRootSceneNode().createChildSceneNode()
        self.rotationNode.createChildSceneNode((20,40,50)).attachObject(light)

        # create head entity
        entity = sceneManager.createEntity('head', 'ogrehead.mesh')
        self.camera.setPosition (20, 0, 100)
        self.camera.lookAt(0, 0, 0)

        sceneManager.getRootSceneNode().createChildSceneNode().attachObject(entity)
        self.renderWindow.getViewport(0).backgroundColour = (0.2, 0.2, 0.2)

    def _createFrameListener(self):
        self.frameListener = MaverickListener(self.renderWindow, self.camera, self.rotationNode)
        self.root.addFrameListener(self.frameListener)

class MaverickListener(sf.FrameListener):
    def __init__(self, renderWindow, camera, rotationNode):
        sf.FrameListener.__init__(self, renderWindow, camera)
        self.rotationNode = rotationNode

    def frameStarted(self, frameEvent):
        self.rotationNode.yaw(ogre.Radian(ogre.Degree(frameEvent.timeSinceLastFrame * 30)))
        return sf.FrameListener.frameStarted(self, frameEvent)

if __name__ == '__main__':
    try:
        application = MaverickApplication()
        application.go()
    except ogre.OgreException, e:
        print e
