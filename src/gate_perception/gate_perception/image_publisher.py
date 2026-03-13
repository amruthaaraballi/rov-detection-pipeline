import os
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImagePublisher(Node):

    def __init__(self):

        super().__init__('image_publisher')

        self.publisher = self.create_publisher(Image,'/camera/image_raw',10)

        self.bridge = CvBridge()

        self.folder = "/home/amrutha/amrutha/gate_test/images"

        self.images = os.listdir(self.folder)

        self.index = 0

        self.timer = self.create_timer(1.0,self.publish_image)

    def publish_image(self):

        path = os.path.join(self.folder,self.images[self.index])

        img = cv2.imread(path)

        msg = self.bridge.cv2_to_imgmsg(img,encoding='bgr8')

        self.publisher.publish(msg)

        self.get_logger().info(f"Publishing {self.images[self.index]}")

        self.index = (self.index + 1) % len(self.images)

def main():

    rclpy.init()

    node = ImagePublisher()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()