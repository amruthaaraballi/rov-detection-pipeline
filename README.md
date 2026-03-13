# Submarine Gate Detection and Navigation System

## Overview

This project implements a **vision-based gate detection system for an Autonomous Underwater Vehicle (AUV)** using **ROS 2 (Humble)** and **OpenCV**.

The goal of the system is to detect a **rectangular gate structure** in camera images and compute the **center coordinates of the detected gate**, which can later be used for **autonomous navigation of the submarine**.

The system is designed as a **ROS2 perception pipeline** where images are published, processed, and converted into navigation information.

This project is part of the development pipeline for an **ROV vision navigation system**, where the vehicle must detect and pass through underwater gates.

---

# System Architecture

The perception pipeline consists of the following components:

```
Image Source
    ↓
Image Publisher Node
    ↓
ROS Topic (/camera/image_raw)
    ↓
Gate Detection Pipeline
    ↓
Gate Center Coordinates
    ↓
Navigation / Control (future step)
```

---

# ROS2 Nodes

## 1. Image Publisher Node

Publishes images to the ROS topic:

```
/camera/image_raw
```

This node simulates a camera by publishing test images from a folder.

Purpose:

* Allows testing of the perception pipeline without hardware
* Useful for debugging detection algorithms

---

## 2. Gate Perception Pipeline Node

Subscribes to:

```
/camera/image_raw
```

Processes the image using computer vision techniques to detect the gate and compute the center.

Publishes:

```
/gate_center
```

Which contains:

```
x : gate center x coordinate
y : gate center y coordinate
z : estimated depth / placeholder value
```

---

# Computer Vision Techniques Used

## 1. Image Preprocessing

The input image is converted to grayscale to simplify processing.

Purpose:

* Reduce computation
* Remove color variations

---

## 2. Edge Detection

Edge detection is applied to detect strong intensity changes in the image.

Typical techniques used:

* Canny Edge Detection
* Sobel gradients

Purpose:

* Detect boundaries of objects
* Identify structural features of the gate

---

## 3. Line Detection

After detecting edges, line detection algorithms are used.

Technique used:

Hough Line Transform

Purpose:

* Identify straight lines in the image
* Extract edges that belong to the rectangular gate

---

## 4. Plane / Shape Estimation

Detected lines are grouped to identify the rectangular gate structure.

Purpose:

* Confirm the structure resembles a gate
* Filter noise from other edges

---

## 5. Center Coordinate Computation

Once the gate boundary is identified, the system calculates the center.

```
center_x = (x_min + x_max) / 2
center_y = (y_min + y_max) / 2
```

The center represents the **target direction for the submarine**.

---

# Output

Example output:

```
Gate Center: [319.75 249.68 5.0]
```

Meaning:

```
x = 319.75 pixels
y = 249.68 pixels
z = estimated depth
```

For a 640x480 image this indicates the gate is near the center.

---

# Testing Pipeline

## Step 1 – Build ROS Workspace

```
cd ~/sub_ws
colcon build
source install/setup.bash
```

---

## Step 2 – Run Image Publisher

Terminal 1:

```
ros2 run gate_perception image_publisher
```

This publishes images to:

```
/camera/image_raw
```

---

## Step 3 – Run Gate Detection

Terminal 2:

```
ros2 run gate_perception gate_pipeline_node
```

This processes images and computes the gate center.

---

## Step 4 – Monitor Output

Terminal 3:

```
ros2 topic echo /gate_center
```

Expected output:

```
x: 319.75
y: 249.6875
z: 5.0
```

---

## Step 5 – View Image Stream

Terminal 4:

```
ros2 topic echo /camera/image_raw
```

---

# Testing with Multiple Images

Multiple test images can be placed inside:

```
images/
```

The image publisher node sequentially publishes each image.

This allows testing the robustness of the detection pipeline.

---

# Live Camera Testing (Future Work)

The system can be connected to a **RealSense camera**.

Steps:

1 Install RealSense ROS package

2 Launch camera node

3 Replace the test image publisher with camera output

The pipeline will then process **live underwater video feed**.

---

# Integration with Submarine Control

The detected gate center coordinates will be used for navigation.

Future pipeline:

```
Gate Detection
     ↓
Center Coordinates
     ↓
Navigation Controller
     ↓
Velocity Commands
     ↓
MAVROS
     ↓
ArduSub SITL / Real Submarine
```

This allows the submarine to automatically align itself with the gate.

---

# Future Improvements

Possible enhancements include:

* Plane fitting optimization
* Robust gate detection in noisy underwater environments
* Deep learning based object detection
* Integration with sonar and depth sensors
* Autonomous navigation through gates

---

# Technologies Used

* ROS 2 Humble
* OpenCV
* Python
* CV Bridge
* ArduSub SITL (for simulation)
* MAVROS

---

# Repository Structure

```
sub
│
├── images
│   └── test images
│
├── report
│   └── project documentation
│
├── src
│   ├── gate_perception
│   ├── gate_navigator
│   └── sub_navigation
│
└── README.md
```

---

# Author

Project developed as part of an **Autonomous Underwater Vehicle perception and navigation system**.

Focus:

* Vision based gate detection
* ROS2 perception pipeline
* AUV autonomous navigation
