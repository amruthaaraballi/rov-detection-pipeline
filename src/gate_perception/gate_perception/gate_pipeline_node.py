import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge

import cv2
import numpy as np

from .mask_refine import refine_mask
from .line_detection import hough_lines
from .plane_fitting import fit_plane
from .gate_center import compute_centroid


class GatePipeline(Node):

    def __init__(self):

        super().__init__('gate_pipeline')

        self.bridge = CvBridge()

        self.sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.pub = self.create_publisher(
            Point,
            '/gate_center',
            10
        )


    def image_callback(self,msg):

        frame = self.bridge.imgmsg_to_cv2(msg)

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        _,mask = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

        mask = refine_mask(mask)

        lines = hough_lines(mask)

        points = []

        if lines is not None:

            for line in lines:

                x1,y1,x2,y2 = line[0]

                points.append([x1,y1,5])
                points.append([x2,y2,5])

        points = np.array(points)

        if len(points) < 3:
            return

        a,b,c,d = fit_plane(points)

        centroid = compute_centroid(points)

        point_msg = Point()
        point_msg.x = float(centroid[0])
        point_msg.y = float(centroid[1])
        point_msg.z = float(centroid[2])

        self.pub.publish(point_msg)

        self.get_logger().info(f'Gate Center: {centroid}')


def main():

    rclpy.init()

    node = GatePipeline()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()