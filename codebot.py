import vk_api
import time
import rospy
from clever import srv

import rospy
import math
from clever import srv
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import SetMode
from std_srvs.srv import Trigger

rospy.init_node('foo')
navigate = rospy.ServiceProxy('/navigate', srv.Navigate)
set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
get_telemetry = rospy.ServiceProxy('/get_telemetry', srv.GetTelemetry)
arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)

vk = vk_api.VkApi(token="c00b07592783dda8b7cad33619b111a7577f3f9502b5173992631b24d915ac622c895a651df4ede2c0ded")
vk._auth_token()

def mode_to(mode):
	return set_mode(base_mode=0, custom_mode=mode)

def land():
	mode_to("AUTO.LAND")
	rospy.sleep(4)
	arming(False)
	print('-----LANDED-----')

def take_off(h, speed=1.0, delta=0.2):
	navigate(x=0, y=0, z=h, yaw=float('nan'), speed=speed, frame_id='fcu_horiz', update_frame=False, auto_arm=True)
	rospy.sleep(4)
	print('\tReached', h)

while True:
	try:
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
		if messages["count"] >= 1:
			id = messages["items"][0]["last_message"]["from_id"]
			body = messages["items"][0]["last_message"]["text"]
			if body.lower() == "takeoff":
				print('takeoff')
				take_off(1.5, 4.0)
				vk.method("messages.send", {"peer_id": id, "message": "Takeoff"})
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = str(telemetry.x)
				y1 = str(telemetry.y)
				vk.method("messages.send", {"peer_id": id, "message": "Telemetry x: " + x1 + " Telemetry y: " + y1})
			elif body.lower() == "help":
				print('help')
				vk.method("messages.send", {"peer_id": id, "message": "Commands: \n 1) takeoff \n 2) land \n 3) forward \n 4) back \n 5) right \n 6) left \n 7) home "})
			elif body.lower() == "forward":
				print('forward')
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = telemetry.x
				y1 = telemetry.y
				xt = (x1+1)
				navigate(x= xt, y=y1, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', update_frame=True, auto_arm=False)
				vk.method("messages.send", {"peer_id": id, "message": "Forward"})
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = str(telemetry.x)
				y1 = str(telemetry.y)
				vk.method("messages.send", {"peer_id": id, "message": "Telemetry x: " + x1 + " Telemetry y: " + y1})
			elif body.lower() == 'back':
				print('back')
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = telemetry.x
				y1 = telemetry.y
				xt = (x1-1)
				navigate(x=xt, y=y1, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', update_frame=True, auto_arm=False)
				vk.method("messages.send", {"peer_id": id, "message": "Back"})
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = str(telemetry.x)
				y1 = str(telemetry.y)
				vk.method("messages.send", {"peer_id": id, "message": "Telemetry x: " + x1 + " Telemetry y: " + y1})
			elif body.lower() == 'left':
				print('left')
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = telemetry.x
				y1 = telemetry.y
				yt = (y1+1)
				navigate(x=x1, y=yt, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', update_frame=True, auto_arm=False)
				vk.method("messages.send", {"peer_id": id, "message": "Left"})
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = str(telemetry.x)
				y1 = str(telemetry.y)
				vk.method("messages.send", {"peer_id": id, "message": "Telemetry x: " + x1 + " Telemetry y: " + y1})
			elif body.lower() == 'right':
				print('right')
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = telemetry.x
				y1 = telemetry.y
				yt = (y1-1)
				navigate(x=x1, y=yt, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', update_frame=True, auto_arm=False)
				vk.method("messages.send", {"peer_id": id, "message": "Right"})
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = str(telemetry.x)
				y1 = str(telemetry.y)
				vk.method("messages.send", {"peer_id": id, "message": "Telemetry x: " + x1 + " Telemetry y: " + y1})
			elif body.lower() == "land":
				print('land')
				land()
				vk.method("messages.send", {"peer_id": id, "message": "Land"})
				telemetry = get_telemetry(frame_id='aruco_map')
				x1 = str(telemetry.x)
				y1 = str(telemetry.y)
				vk.method("messages.send", {"peer_id": id, "message": "Telemetry x: " + x1 + " Telemetry y: " + y1})
				break
			elif body.lower() == "home":
				print('home')
				navigate(x=0, y=0, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', update_frame=True, auto_arm=False)
				vk.method("messages.send", {"peer_id": id, "message": "Home"})
			else:
				print('error')
				vk.method("messages.send", {"peer_id": id, "message": "unknown command"})
	except Exception as E:
		time.sleep(1)
