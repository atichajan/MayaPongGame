try:
	from PySide6 import QtWidgets, QtCore, QtGui
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtWidgets, QtCore, QtGui
	from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random

ROOT_RESOURCE_DIR = "C:/Users/user/Documents/maya/scripts/MayaPongGame/image"

class PongGame(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(PongGame, self).__init__(parent or get_maya_main_window())

		self.setWindowTitle("🏓Maya Pong Game")
		self.setFixedSize(430, 400)

		self.setStyleSheet("""
			QDialog {
				background-color: #ff8a65;
			}
			QPushButton {
				background-color: #ab47bc;
				color: white;
				border-radius: 8px;
				padding: 8px 14px;
				font-weight: bold;
				font-size: 16px;
			}
			QPushButton:hover {
				background-color: #ba68c8;
			}
			QPushButton:pressed {
				background-color: #8e24aa;
			}
		""")

		self.layout = QtWidgets.QVBoxLayout(self)

		self.info_label = QtWidgets.QLabel("🎮HOLD LEFT/RIGHT TO MOVE PADDLE🎮")
		self.info_label.setStyleSheet("color: #000000; font-size: 17px; font-weight: bold;")
		self.info_label.setAlignment(QtCore.Qt.AlignCenter)
		self.layout.addWidget(self.info_label)

		move_layout = QtWidgets.QHBoxLayout()
		self.left_btn = QtWidgets.QPushButton("⬅️ Left")
		self.right_btn = QtWidgets.QPushButton("Right ➡️")
		move_layout.addWidget(self.left_btn)
		move_layout.addWidget(self.right_btn)
		self.layout.addLayout(move_layout)

		self.start_btn = QtWidgets.QPushButton("😎Start Game😎")
		self.layout.addWidget(self.start_btn)

		self.status_label = QtWidgets.QLabel("")
		self.status_label.setStyleSheet("color: #000000; font-size: 16px; font-weight: bold;")
		self.status_label.setAlignment(QtCore.Qt.AlignCenter)
		self.layout.addWidget(self.status_label)

		self.start_btn.clicked.connect(self.start_game)

		self.left_timer = QtCore.QTimer()
		self.left_timer.timeout.connect(lambda: self.move_paddle(-0.3))
		self.right_timer = QtCore.QTimer()
		self.right_timer.timeout.connect(lambda: self.move_paddle(0.3))

		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f"{ROOT_RESOURCE_DIR}/Pong.jpg")
		scale_pixmap = self.imagePixmap.scaled(
			QtCore.QSize(400,200),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation
		)


		self.imageLabel.setPixmap(scale_pixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.layout.addWidget(self.imageLabel)

		self.imageLabel.setPixmap(self.imagePixmap)
		self.layout.addWidget(self.imageLabel)

		self.left_btn.pressed.connect(self.left_timer.start)
		self.left_btn.released.connect(self.left_timer.stop)
		self.right_btn.pressed.connect(self.right_timer.start)
		self.right_btn.released.connect(self.right_timer.stop)

		self.left_timer.setInterval(30)
		self.right_timer.setInterval(30)

		self.ball_timer = QtCore.QTimer()
		self.ball_timer.timeout.connect(self.update_ball)

		self.paddle = None
		self.ball = None
		self.ball_dir = [0.2, 0, 0.2]

	def reset_scene(self):
		cmds.select(all=True)
		try:
			cmds.delete()
		except:
			pass

		self.paddle = cmds.polyCube(w=2, h=0.5, d=0.5, name="paddle")[0]
		cmds.move(0, 0, -5, self.paddle)
		cmds.polyColorPerVertex(self.paddle, rgb=(0.8, 0.2, 0.2), colorDisplayOption=True)
		cmds.setAttr(self.paddle + ".displayColors", 1)

		self.ball = cmds.polySphere(r=0.3, name="ball")[0]
		cmds.move(0, 0, 0, self.ball)

		cmds.polyColorPerVertex(self.ball, rgb=(1.0, 0.4, 0.2), colorDisplayOption=True)
		cmds.setAttr(self.ball + ".displayColors", 1)


		top = cmds.polyCube(w=12, h=1, d=0.5, name="topWall")[0]
		cmds.move(0, 0, 6, top)
		bottom = cmds.polyCube(w=12, h=1, d=0.5, name="bottomWall")[0]
		cmds.move(0, 0, -6, bottom)
		left = cmds.polyCube(w=0.5, h=1, d=12, name="leftWall")[0]
		cmds.move(-6, 0, 0, left)
		right = cmds.polyCube(w=0.5, h=1, d=12, name="rightWall")[0]
		cmds.move(6, 0, 0, right)

		for wall in [top, bottom, left, right]:
			cmds.polyColorPerVertex(wall, rgb=(0.0, 0.4, 1.0), colorDisplayOption=True)
			cmds.setAttr(wall + ".displayColors", 1)


	def start_game(self):
		self.reset_scene()
		self.ball_dir = [random.choice([-0.2, 0.2]), 0, 0.2]
		self.ball_timer.start(30)
		self.status_label.setText("🟢GAME START🟢")

	def move_paddle(self, amount):
		if not self.paddle:
			return
		pos = cmds.xform(self.paddle, q=True, t=True, ws=True)
		new_x = pos[0] + amount
		if -5 < new_x < 5:
			cmds.move(new_x, pos[1], pos[2], self.paddle)

	def update_ball(self):
		if not self.ball:
			return

		pos = cmds.xform(self.ball, q=True, t=True, ws=True)
		new_pos = [pos[0] + self.ball_dir[0], pos[1] + self.ball_dir[1], pos[2] + self.ball_dir[2]]
		cmds.move(new_pos[0], new_pos[1], new_pos[2], self.ball)

		if abs(new_pos[0]) >= 5.5:
			self.ball_dir[0] *= -1
		if new_pos[2] >= 5.5:
			self.ball_dir[2] *= -1

		if new_pos[2] <= -5.5:
			self.ball_timer.stop()
			self.status_label.setText("🔴GAME OVER🔴")
			return

		paddle_pos = cmds.xform(self.paddle, q=True, t=True, ws=True)
		if (
			abs(new_pos[2] - paddle_pos[2]) < 0.5 and
			abs(new_pos[0] - paddle_pos[0]) < 1.2 and
			self.ball_dir[2] < 0
		):
			self.ball_dir[2] *= -1
			self.status_label.setText("🏓BOUNCE🏓")

def run():
	global ui
	try:
		ui.close()
	except:
		pass

	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = PongGame(parent=ptr)
	ui.show()