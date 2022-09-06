
from turtle import distance
import rclpy 
from rclpy.node import Node 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class Turtle_node(Node):
  def __init__(self):
    
    super().__init__('goal')
      
    self.pub = self.create_publisher(Twist,'/turtle1/cmd_vel', 10)
      
    self.timer = self.create_timer(0.5, self.value)
     
    self.pose_sub = self.create_subscription(Pose,'/turtle1/pose',self.pose_callback,10)
    self.pose=Pose()
  
  def pose_callback(self,data):

    msg = 'X: {:.3f}, Y: {:.3f}, Theta: {:.3f}'.format(data.x,data.y,data.theta)
    self.get_logger().info(msg)     
    self.pose.x=data.x
    self.pose.y=data.y
    self.pose.theta=data.theta
      
    
      
  def distance(self,goal):
    print((self.pose.x))
    return sqrt(pow((goal.x-self.pose.x),2)+pow((goal.y-self.pose.y),2))
  
  def Linear_Vel(self,goal):
    return .5 * self.distance(goal)

  def angle(self,goal):
    return atan2(goal.y-self.pose.y,goal.x-self.pose.x)

  def Angle_Vel(self,goal):
     return .5 * (self.angle(goal)-self.pose.theta)

  def value(self):
    goal=Pose()
    goal.x=8.0
    goal.y=8.0
    goal.theta=1.5
    velocity_massage= Twist()
    distancee=self.distance(goal)
    
  
    if (self.angle(goal) - self.pose.theta) > 0.01:
        velocity_massage.linear.x=0.0
        velocity_massage.angular.z=self.angle(goal)-self.pose.theta
        if (velocity_massage.angular.z) < 0.1:
            velocity_massage.linear.x=self.Linear_Vel(goal)
    if (distancee) < 2 :
        velocity_massage.angular.z=goal.theta-self.pose.theta

    self.pub.publish(velocity_massage)
    
  
      
def main(args=None):
  
  rclpy.init(args=args)
  
  node=Turtle_node()
  
  rclpy.spin(node)
  
  
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()