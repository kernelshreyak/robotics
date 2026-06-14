#include <Servo.h>

Servo panServo;

const int leftButton  = 2;
const int rightButton = 3;

int angle = 180;

void setup() {
  panServo.attach(9);
  panServo.write(angle);

  pinMode(leftButton, INPUT_PULLUP);
  pinMode(rightButton, INPUT_PULLUP);
}

void loop() {

  if (digitalRead(leftButton) == LOW) {
    angle--;
    if (angle < 0) angle = 0;

    panServo.write(angle);
    delay(10);
  }

  if (digitalRead(rightButton) == LOW) {
    angle++;
    if (angle > 180) angle = 180;

    panServo.write(angle);
    delay(10);
  }
}
