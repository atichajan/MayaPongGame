try:
	from PySide6 import QtWidgets, QtCore, QtGui
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtWidgets, QtCore, QtGui
	from shiboken2 import wrapInstance

def get_maya_main_window():
	ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(ptr), QtWidgets.QWidget)

def clear_scene():
	cmds.select(all=True)
	try: cmds.delete()
	except: pass

def create_colored_cube(name, w=1, h=1, d=1, color=(1,1,1)):
	obj = cmds.polyCube(w=w, h=h, d=d, name=name)[0]
	cmds.polyColorPerVertex(obj, rgb=color, colorDisplayOption=True)
	cmds.setAttr(obj + ".displayColors", 1)
	return obj

def create_colored_sphere(name, r=1, color=(1,1,1)):
	obj = cmds.polySphere(r=r, name=name)[0]
	cmds.polyColorPerVertex(obj, rgb=color, colorDisplayOption=True)
	cmds.setAttr(obj + ".displayColors", 1)
	return obj