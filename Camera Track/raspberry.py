import pickle
import socket
import RPi.GPIO as GPIO


fPWM = 50  # Hz (PWM方式下的频率，值不能设置过高)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 去除GPIO警告

#smp18BCM接口
GPIO.setup(18, GPIO.OUT)

# pwm设置
pwm = GPIO.PWM(18, fPWM)
pwm.start(0)


pwm_a=90

def math(d):
    return 10 / 270 * d + 2.5

data_list=[0,0]
angel_max=50
angle_min=-50

def main():
    global pwm_a
    global n_servo
    global data_list
    #初始化
    host = '192.168.3.31'  # 服务器IP地址 可以在windows上通过ipconfig查找到
    port = 12345  # 服务器端口号
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  # 这行代码创建了一个 socket 对象。socket.AF_INET 指定了地址族为 IPv4，socket.SOCK_STREAM 表明这是一个 TCP socket。
    client_socket.connect((host, port))  # 这行代码用之前设置的 IP 地址和端口号来连接服务器。

    pwm.ChangeDutyCycle(math(90))
    while True:
        data = client_socket.recv(1024)
        data_list = pickle.loads(data)
        #简易的追踪
        if data_list[0] -320 > angel_max and pwm_a >0:
            print("z")
            pwm_a -=2
        if data_list[0]  -320 < angle_min and pwm_a <180:
            pwm_a +=2
            print("y")
        print(pwm_a)
        pwm.ChangeDutyCycle(math(pwm_a))

if __name__ == '__main__':
    main()
    GPIO.cleanup()
