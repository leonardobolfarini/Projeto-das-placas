#include <Servo.h>

Servo servo_3;
const int servo = 3;

void setup() {
  Serial.begin(9600);
  servo_3.attach(servo);
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '1') {
      servo_3.write(90);
    } else if (receivedChar == '0') {
      servo_3.write(0);
    }
  }
}