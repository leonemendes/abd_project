from flask import Flask, render_template, Response, request
from picamera import PiCamera
from flask import jsonify,json

from camera_pi import Camera


import sys
import wave
import contextlib
import time
import cv2
import pygame
import RPi.GPIO as GPIO


app = Flask(__name__)
cam = Camera()



@app.route('/', methods=['GET','POST'])
def index():
    """Video streaming home page."""

    if request.method == 'POST' :
        GPIO.cleanup()
        angle = request.form['angle']
        x = (int(angle) +72)/18
        print(int(angle))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setwarnings(False)
        pwm=GPIO.PWM(26,50)
        pwm.start(x)
        time.sleep(1)
    return render_template('index.html')

@app.route('/button', methods=['GET','POST'])
def button():
    print("Coucou")
    return jsonify({})

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(cam),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pic', methods=['GET','POST'])
def pic():
    print("Pic taken")
    cam.save_frame()
    num_pic = cam.nbPic
    return jsonify({'num_pic' : str(num_pic)+ " pictures"})

@app.route('/sound', methods=['GET','POST'])
def sound():
    pygame.init()
    pygame.mixer.music.load("output.wav")
    pygame.mixer.music.play()
    length=pygame.mixer.Sound('output.wav').get_length()
    time.sleep(length+10)
    return jsonify({})


@app.route('/servo', methods=['GET','POST'])
def servo():
    if request.method == 'POST':
        angle = request.form['angle']
    print(angle)

@app.route('/5')
def move5():
    GPIO.cleanup()
    angle = 5
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/10')
def move10():
    GPIO.cleanup()
    angle = 10
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/15')
def move15():
    GPIO.cleanup()
    angle = 15
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/20')
def move20():
    GPIO.cleanup()
    angle = 20
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/25')
def move25():
    GPIO.cleanup()
    angle = 25
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/30')
def move30():
    GPIO.cleanup()
    angle = 30
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/35')
def move35():
    GPIO.cleanup()
    angle = 35
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/40')
def move40():
    GPIO.cleanup()
    angle = 40
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/45')
def move45():
    GPIO.cleanup()
    angle = 45
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l5')
def movel5():
    GPIO.cleanup()
    angle = -5
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l10')
def movel10():
    GPIO.cleanup()
    angle = -10
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l15')
def movel15():
    GPIO.cleanup()
    angle = -15
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l20')
def movel20():
    GPIO.cleanup()
    angle = -20
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l25')
def movel25():
    GPIO.cleanup()
    angle = -25
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l30')
def movel30():
    GPIO.cleanup()
    angle = -30
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l35')
def movel35():
    GPIO.cleanup()
    angle = -35
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l40')
def movel40():
    GPIO.cleanup()
    angle = -40
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/l45')
def movel45():
    GPIO.cleanup()
    angle = -45
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})
@app.route('/l0')
def movel0():
    GPIO.cleanup()
    angle = -0
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})

@app.route('/0')
def move0():
    GPIO.cleanup()
    angle = 0
    x = (int(angle) +72)/18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(26,50)
    pwm.start(x)
    time.sleep(1)
    return jsonify({})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)

