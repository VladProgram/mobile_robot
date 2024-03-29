#include <Servo.h>    //Servo motor library. This is standard library //Robot Lk
#include <NewPing.h>  //Ultrasonic sensor function library. You must install this library //Robot Lk
//Robot Lk YouTube Channel-https://www.youtube.com/c/RobotLk
//our L298N control pins
const int LeftMotorForward = 7;
const int LeftMotorBackward = 6;
const int RightMotorForward = 5;
const int RightMotorBackward = 4;

//sensor pins
#define trig_pin A1  //analog input 1
#define echo_pin A2  //analog input 2
//#define LED_PIN 13

//#define maximum_distance 200
boolean loopstop = false;
//int distance = 100;

//NewPing sonar(trig_pin, echo_pin, maximum_distance); //sensor function
Servo servo_motor;  //our servo name
byte val = 0;

//Last time received serial
unsigned long PreviousTime = 0;

// timeout interval for stop automatically (millsec)
const long timeoutInterval = 500; 

//Robot Lk
void setup() {
  pinMode(RightMotorForward, OUTPUT);
  pinMode(LeftMotorForward, OUTPUT);
  pinMode(LeftMotorBackward, OUTPUT);
  pinMode(RightMotorBackward, OUTPUT);
  //pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  servo_motor.attach(10);  //our servo pin

  //servo_motor.write(115);
  //delay(2000);
  //distance = readPing();
  //delay(100);
  //distance = readPing();
  //delay(100);
  //distance = readPing();
  //delay(100);
  //distance = readPing();
  //delay(100);
}

void loop() {
  //int distanceRight = 0;
  //int distanceLeft = 0;
  //delay(50);

  if (Serial.available() > 0) {
    val = Serial.read();

    switch (val) {
      case 'F':
        loopstop = false;
        moveForward();
        PreviousTime = millis(); 
        break;
      case 'B':
        loopstop = false;
        moveBackward();
        PreviousTime = millis(); 
        break;
      case 'R':
        loopstop = false;
        turnRight();
        PreviousTime = millis(); 
        break;
      case 'L':
        loopstop = false;
        turnLeft();
        PreviousTime = millis(); 
        break;
      case 'S':
        moveStop();
        loopstop = true;
        break;
      //default: // When received unknown command
        //moveStop();
        //loopstop = true;
        //break;
    }

    //distance = readPing();

    //int readPing(){
    //  delay(70);
    //  int cm = sonar.ping_cm();
    //  if (cm==0){
    //    cm=250;
    //  }
    //  return cm;
    //}
  }

  // Get current now
  unsigned long CurrentTime = millis();

  if (loopstop == false) {
    if (CurrentTime - PreviousTime >= timeoutInterval) {
      moveStop();
      loopstop = true;
    }
  }
}


void moveStop() {
  digitalWrite(RightMotorForward, LOW);
  digitalWrite(LeftMotorForward, LOW);
  digitalWrite(RightMotorBackward, LOW);
  digitalWrite(LeftMotorBackward, LOW);
}


void moveForward() {
    digitalWrite(LeftMotorForward, HIGH);
    digitalWrite(RightMotorForward, HIGH);
    digitalWrite(LeftMotorBackward, LOW);
    digitalWrite(RightMotorBackward, LOW);
}

void moveBackward() {
  digitalWrite(LeftMotorBackward, HIGH);
  digitalWrite(RightMotorBackward, HIGH);
  digitalWrite(LeftMotorForward, LOW);
  digitalWrite(RightMotorForward, LOW);
}


void turnRight() {
  digitalWrite(LeftMotorBackward, HIGH);
  digitalWrite(RightMotorForward, HIGH);
  digitalWrite(LeftMotorForward, LOW);
  digitalWrite(RightMotorBackward, LOW);
}


void turnLeft() {
  digitalWrite(LeftMotorForward, HIGH);
  digitalWrite(RightMotorBackward, HIGH);
  digitalWrite(LeftMotorBackward, LOW);
  digitalWrite(RightMotorForward, LOW);
}