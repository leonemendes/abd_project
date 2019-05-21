from flask import Flask, render_template, Response, request
from picamera import PiCamera
from flask import jsonify,json
import numpy as np
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
#This application allows to play a sound
@app.route('/sound', methods=['GET','POST'])
def sound():
    pygame.init()
    pygame.mixer.music.load("output.wav")
    pygame.mixer.music.play()
    length=pygame.mixer.Sound('output.wav').get_length()
    time.sleep(length+10)
    return jsonify({})


#This application allows to choose a time where laser is turned on
@app.route('/switch', methods=['GET','POST'])
def switch():
    out1 = 40
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out1,GPIO.OUT)
    val_switch = request.args.get('val_switch',0 , type = int)
    GPIO.output(out1,GPIO.HIGH)
    time.sleep(val_switch)
    value = GPIO.input(out1)
    print(value)
    GPIO.output(out1,GPIO.LOW)
    print(GPIO.input(out1))
    GPIO.cleanup()
    return jsonify({})

#This application allows to make a full turn of the servo of the ball launcher
@app.route('/shoot', methods=['GET','POST'])
def shoot():
    GPIO.cleanup()
    x =10
    print('shot')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(36,50)
    pwm.start(x)
    time.sleep(0.4)
    GPIO.cleanup()
    return jsonify({})

#This application is useless but allows you tu use buttons to control a servo 
@app.route('/servo', methods=['GET','POST'])
def servo():
    if request.method == 'POST':
        angle = request.form['angle']
    print(angle)

#This application allows to control the servo for the laser :set the right GPIO of RPi
@app.route('/servo_las', methods=['GET','POST'])
def servo_las():
    GPIO.cleanup() 
    angle_las = request.args.get('angle_las',0 , type = int)
    print(angle_las)
    x = (-float(angle_las)+135)*12/180
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(38,50)
    pwm.start(0)
    time.sleep(1)
    pwm.ChangeDutyCycle(x)
    time.sleep(0.5)
    GPIO.cleanup()
    return jsonify({})

#This application allows to control the servo to move the ball launcher. Set the right pin 
@app.route('/servo_ball', methods=['GET','POST'])
def servo_ball():
    GPIO.cleanup() 
    angle_ball = request.args.get('angle_ball',0 , type = int)
    print(angle_ball)

    x =( int(angle_ball) +77)/18
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32, GPIO.OUT)
    GPIO.setwarnings(False)
    pwm=GPIO.PWM(32,50)
    pwm.start(x)
    time.sleep(0.5)
    GPIO.cleanup()
    return jsonify({})

# This application allows to control the stepper motor of the station . Set the right pin
@app.route('/step', methods=['GET','POST'])
def step():
    angle = request.args.get('angle',0 , type=int)
    print(angle)

    t = 0.02
    step_out1=37
    step_out2=35
    step_out3=33
    step_out4=31

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(step_out1,GPIO.OUT)
    GPIO.setup(step_out2,GPIO.OUT)
    GPIO.setup(step_out3,GPIO.OUT)
    GPIO.setup(step_out4,GPIO.OUT)

    GPIO.output(step_out1,GPIO.LOW)
    GPIO.output(step_out2,GPIO.LOW)
    GPIO.output(step_out3,GPIO.LOW)
    GPIO.output(step_out4,GPIO.LOW)

    y=angle*25/180
    if y>0 and angle <= 360 :

         for i in range(0,int(y)):

            GPIO.output(step_out1,GPIO.HIGH)
            GPIO.output(step_out2,GPIO.LOW)
            GPIO.output(step_out3,GPIO.LOW)
            GPIO.output(step_out4,GPIO.LOW)
            time.sleep(t)

            GPIO.output(step_out1,GPIO.LOW)
            GPIO.output(step_out2,GPIO.LOW)
            GPIO.output(step_out3,GPIO.HIGH)
            GPIO.output(step_out4,GPIO.LOW)
            time.sleep(t)

            GPIO.output(step_out1,GPIO.LOW)
            GPIO.output(step_out2,GPIO.HIGH)
            GPIO.output(step_out3,GPIO.LOW)
            GPIO.output(step_out4,GPIO.LOW)
            time.sleep(t)

            GPIO.output(step_out1,GPIO.LOW)
            GPIO.output(step_out2,GPIO.LOW)
            GPIO.output(step_out3,GPIO.LOW)
            GPIO.output(step_out4,GPIO.HIGH)
            time.sleep(t)
            
    if y<0 and abs(angle) <= 360: 
        for i in range(0,-int(y)):

            GPIO.output(step_out1,GPIO.LOW)
            GPIO.output(step_out2,GPIO.LOW)
            GPIO.output(step_out3,GPIO.LOW)
            GPIO.output(step_out4,GPIO.HIGH)
            time.sleep(t)

            GPIO.output(step_out1,GPIO.LOW)
            GPIO.output(step_out2,GPIO.HIGH)
            GPIO.output(step_out3,GPIO.LOW)
            GPIO.output(step_out4,GPIO.LOW)
            time.sleep(t)

            GPIO.output(step_out1,GPIO.LOW)
            GPIO.output(step_out2,GPIO.LOW)
            GPIO.output(step_out3,GPIO.HIGH)
            GPIO.output(step_out4,GPIO.LOW)
            time.sleep(t)

            GPIO.output(step_out1,GPIO.HIGH)
            GPIO.output(step_out2,GPIO.LOW)
            GPIO.output(step_out3,GPIO.LOW)
            GPIO.output(step_out4,GPIO.LOW)
            time.sleep(t)

     
    return jsonify({})


#@app.route('/5')
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

