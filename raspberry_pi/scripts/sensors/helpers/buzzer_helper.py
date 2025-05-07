import pigpio
import time

pi = pigpio.pi()

BUZZER_PIN = 18  # BCM

pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)
pi.hardware_PWM(BUZZER_PIN, 2500, 500000)
time.sleep(5)

pi.hardware_PWM(BUZZER_PIN, 0, 0)  # Stop de toon
pi.stop()
