
import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import socket
import pickle
import math


"""
#server-medaipipe-5改
"""
"""
通讯部分仍然是socket，树莓派性能差也懒得改了
"""
host = '0.0.0.0'  # 监听所有可用的接口
port = 12345  # 端口号
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)  # 使服务器开始监听连接请求
print("等待客户端连接...")
conn, address = server_socket.accept()
print("连接来自: " + str(address))
print(conn)

# 全局变量
list_p =[None for i in  range(2)]

# 函数
def socket_sever(message):
    conn.send(message)

#模型与设置默认摄像头
mp_face_detection = mp.solutions.face_detection
cap = cv.VideoCapture(0)

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detector:
    image_counter = 0
    fonts = cv.FONT_HERSHEY_PLAIN
    start_time = time.time()
    while cap.isOpened:
        success, image = cap.read()
        image_counter += 1
        if not success:
            print("Ignoring empty camera image.")
            break
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        results = face_detector.process(rgb_image)
        image_height, image_width, c = image.shape
        if results.detections:
            for face in results.detections:
                face_react = np.multiply(
                    [
                        face.location_data.relative_bounding_box.xmin,
                        face.location_data.relative_bounding_box.ymin,
                        face.location_data.relative_bounding_box.width,
                        face.location_data.relative_bounding_box.height,
                    ],
                    [image_width, image_height, image_width, image_height]).astype(int)
                cv.rectangle(image, face_react, color=(255, 255, 255), thickness=2)

                key_points = np.array([(p.x, p.y) for p in face.location_data.relative_keypoints])

                key_points_coords = np.multiply(key_points, [image_width, image_height]).astype(int)
                list_p[0]=int(key_points_coords[2][0])#鼻子x坐标
                list_p[1]=int(key_points_coords[2][1])#鼻子y坐标

                #列表打包
                pickled_list = pickle.dumps(list_p)
                socket_sever(pickled_list)
                for p in key_points_coords:
                    cv.circle(image, p, 4, (255, 255, 255), 2)
                    cv.circle(image, p, 2, (0, 0, 0), -1)

        fps = image_counter / (time.time() - start_time)
        cv.putText(image, f"FPS: {fps:.2f}", (30, 30), cv.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2, )
        cv.imshow("image", image)
        key = cv.waitKey(1)
        if key == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()
