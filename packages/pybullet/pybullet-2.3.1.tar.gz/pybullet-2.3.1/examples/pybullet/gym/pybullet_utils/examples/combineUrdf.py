import pybullet_utils.bullet_client as bc
import pybullet_utils.urdfEditor as ed
import pybullet
import pybullet_data
import time

import types
def var_dump(obj, depth=4, l=""):
    #fall back to repr
    if depth<0: return repr(obj)
    #expand/recurse dict
    if isinstance(obj, dict):
        name = ""
        objdict = obj
    else:
        #if basic type, or list thereof, just print
        canprint=lambda o:isinstance(o, (int, float, str, unicode, bool, types.NoneType, types.LambdaType))
        try:
            if canprint(obj) or sum(not canprint(o) for o in obj) == 0: return repr(obj)
        except TypeError, e:
            pass
        #try to iterate as if obj were a list
        try:
            return "[\n" + "\n".join(l + var_dump(k, depth=depth-1, l=l+"  ") + "," for k in obj) + "\n" + l + "]"
        except TypeError, e:
            #else, expand/recurse object attribs
            name = (hasattr(obj, '__class__') and obj.__class__.__name__ or type(obj).__name__)
            objdict = {}
            for a in dir(obj):
                if a[:2] != "__" and (not hasattr(obj, a) or not hasattr(getattr(obj, a), '__call__')):
                    try: objdict[a] = getattr(obj, a)
                    except Exception, e: objdict[a] = str(e)
    return name + "{\n" + "\n".join(l + repr(k) + ": " + var_dump(v, depth=depth-1, l=l+"  ") + "," for k, v in objdict.iteritems()) + "\n" + l + "}"

p0 = bc.BulletClient(connection_mode=pybullet.DIRECT)
p0.setAdditionalSearchPath(pybullet_data.getDataPath())

p1 = bc.BulletClient(connection_mode=pybullet.DIRECT)
p1.setAdditionalSearchPath(pybullet_data.getDataPath())


body = p0.loadURDF("sphere_small.urdf", globalScaling=3)
leg = p1.loadURDF("capsule.urdf", flags=p0.URDF_USE_IMPLICIT_CYLINDER)

ed0 = ed.UrdfEditor()
ed0.initializeFromBulletBody(body, p0._client)

print(var_dump(ed0.urdfLinks))

ed1 = ed.UrdfEditor()
ed1.initializeFromBulletBody(leg, p1._client)

print(var_dump(ed1.urdfLinks))


ed1.saveUrdf("combined.urdf")

parentLinkIndex = 0

legOffset = 0.08
legOffsetZ=-0.05
legOffsetZchild = 0.01
jointPivotXYZInParent = [legOffset,legOffset,legOffsetZ]
jointPivotRPYInParent = [0,0,0]

jointPivotXYZInChild = [0,0,legOffsetZchild]
jointPivotRPYInChild = [0,0,0]

ed1.urdfLinks[0].link_name="leg0"
newjoint = ed0.joinUrdf(ed1, parentLinkIndex , jointPivotXYZInParent, jointPivotRPYInParent, jointPivotXYZInChild, jointPivotRPYInChild,  p0._client, p1._client)
#newjoint.joint_type = p0.JOINT_FIXED
newjoint.joint_axis_xyz = [1,0,0]

ed1.urdfLinks[0].link_name="leg1"
jointPivotXYZInParent = [-legOffset,legOffset,legOffsetZ]
newjoint = ed0.joinUrdf(ed1, parentLinkIndex , jointPivotXYZInParent, jointPivotRPYInParent, jointPivotXYZInChild, jointPivotRPYInChild,  p0._client, p1._client)
newjoint.joint_axis_xyz = [1,0,0]

ed1.urdfLinks[0].link_name="leg2"
jointPivotXYZInParent = [-legOffset,-legOffset,legOffsetZ]
newjoint = ed0.joinUrdf(ed1, parentLinkIndex , jointPivotXYZInParent, jointPivotRPYInParent, jointPivotXYZInChild, jointPivotRPYInChild,  p0._client, p1._client)
newjoint.joint_axis_xyz = [1,0,0]

ed1.urdfLinks[0].link_name="leg3"
jointPivotXYZInParent = [legOffset,-legOffset,legOffsetZ]
newjoint = ed0.joinUrdf(ed1, parentLinkIndex , jointPivotXYZInParent, jointPivotRPYInParent, jointPivotXYZInChild, jointPivotRPYInChild,  p0._client, p1._client)
newjoint.joint_axis_xyz = [1,0,0]

print("new creature:")
print(var_dump(ed0.urdfLinks))
print(var_dump(ed0.urdfJoints,2))

ed0.saveUrdf("combined.urdf")

print(p0._client)
print(p1._client)
print("p0.getNumBodies()=",p0.getNumBodies())
print("p1.getNumBodies()=",p1.getNumBodies())

pgui = bc.BulletClient(connection_mode=pybullet.GUI)
pgui.configureDebugVisualizer(pgui.COV_ENABLE_RENDERING, 0)

orn=[0,0,0,1]
for a in range (4):
	for b in range (4):
		ant = ed0.createMultiBody([a,b,1],orn, pgui._client)

ant = ed0.createMultiBody([-1,-1,1],orn, pgui._client)

for j in range (pgui.getNumJoints(ant)):
	pgui.setJointMotorControl2(ant,j,pgui.VELOCITY_CONTROL, targetVelocity=1, force=10)
pgui.setGravity(0,0,-10)
pgui.setRealTimeSimulation(1)
pgui.loadURDF("plane.urdf")

pgui.configureDebugVisualizer(pgui.COV_ENABLE_RENDERING, 1)
pgui.saveWorld("creatures.py")

while (pgui.isConnected()):
	#pgui.getCameraImage(320,200, renderer=pgui.ER_BULLET_HARDWARE_OPENGL)
	pgui.setGravity(0,0,-10)
	time.sleep(1./240.)
