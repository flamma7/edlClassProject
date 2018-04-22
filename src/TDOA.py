#!/usr/bin/env python

import rospy
import math
import numpy as np

from std_msgs.msg import Int8
from std_msgs.msg import Int16

class TDOA:
    def __init__(self):
        rospy.init_node("tdoa_node")
        rospy.Subscriber("/tdoa", Int16, self.tdoa_callback)
        self.pub = rospy.Publisher("/theta", Int8, queue_size=10)
        rospy.loginfo("tdoa_node ready")

        rospy.spin()
        

    def tdoa_callback(self, msg):
        # receive float from ros and store in tdoa variable
        tdoa = float(msg.data)

        # calculations
        t = tdoa/1000000 # convert tdoa from microseconds to seconds
        c = 343 # speed of sound
        d = t*c
        r = 0.1
        print('tdoa = '+ str(tdoa))

        #x_num = (-d*d*(d*d-4*r*r))
        #print('x_num = '+ str(x_num))
        #x_den = 4*(4*r*r-d*d)
        #print('x_den = '+ str(x_den))
        #x = np.sqrt(x_num/x_den)
        #print('x = '+ str(x))
        x = d/2
        print('x = '+ str(x))

        y_num = (2*x*((4*r*r/(d*d))-1))
        print('y_num = '+str(y_num))
        y_den = ((d*d/4)-r*r+x*x*((4*r*r/(d*d))-1))
        print('y_den = '+str(y_den))
        dy = (y_num/(2*np.sqrt(y_den)))
        print('dy/dx = '+str(dy))
        
        th = np.arctan(dy)
        print('th = '+ str(th))
        
        if th>0:
            theta = 90-th
        else:
            theta = -90-th
        
        # Send result back to ros network
        theta_msg = Float32()
        theta_msg.data = theta
        self.pub.publish(theta_msg)
        


        



if __name__ == "__main__":
    a = TDOA()


