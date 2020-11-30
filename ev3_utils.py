from threading import Thread
import rpyc


class MotorThread(Thread):

    conn = rpyc.classic.connect('192.168.0.11')
    ev3dev2_motor = conn.modules['ev3dev2.motor']

    def __init__(self):
        Thread.__init__(self)
        self._motor_l_speed = 0
        self._motor_r_speed = 0
        self.motor_l = self.ev3dev2_motor.MediumMotor(self.ev3dev2_motor.OUTPUT_C)
        self.motor_r = self.ev3dev2_motor.MediumMotor(self.ev3dev2_motor.OUTPUT_B)
        self.running = True

    def run(self):
        while self.running:
            self.motor_l.on(self.ev3dev2_motor.SpeedDPS(-self._motor_l_speed))
            self.motor_r.on(self.ev3dev2_motor.SpeedDPS(self._motor_l_speed))
        self.motor_r.stop()
        self.motor_l.stop()

    @property
    def motor_l_speed(self):
        return self._motor_l_speed

    @property
    def motor_r_speed(self):
        return self._motor_r_speed

    @motor_l_speed.setter
    def motor_l_speed(self, value):
        self._motor_l_speed = value

    @motor_r_speed.setter
    def motor_r_speed(self, value):
        self._motor_r_speed = value