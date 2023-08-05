import pybullet_utils.bullet_client as bc
import pybullet_utils.urdfEditor as ed
import pybullet
import pybullet_data
import time

p0 = bc.BulletClient(connection_mode=pybullet.DIRECT)
p0.setAdditionalSearchPath(pybullet_data.getDataPath())

objects= p0.loadMJCF("ant.xml")
ant=objects[0]
ed0 = ed.UrdfEditor()
ed0.initializeFromBulletBody(ant, p0._client)
ed0.saveUrdf("ant.urdf")

orn=[0,0,0,1]
pgui = bc.BulletClient(connection_mode=pybullet.GUI)

ed0.createMultiBody([0,0,0],orn, pgui._client)
pgui.setRealTimeSimulation(1)

while (pgui.isConnected()):
	pgui.getCameraImage(320,200, renderer=pgui.ER_BULLET_HARDWARE_OPENGL)
	time.sleep(1./240.)
