#include <Servo.h>

Servo servo_base;
Servo servo_top;

int pos = 0;
char command;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo_base.attach(7);
  servo_top.attach(6);
  servo_base.write(105);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  /*servo_top.write(105);
  delay(800);
  servo_top.write(90);
  servo_base.write(80);
  delay(300);
  servo_base.write(110);
  delay(300);
  */
  while (Serial.available() == 0){}
      command = Serial.read();
      if (command == 'b'){
       /* servo_top.attach(6);
        servo_top.write(105);
        delay(4300);
        servo_top.detach();
        */
          Serial.println("Start");
          servo_top.attach(6);
          servo_top.write(105);
          delay(2250);
          servo_top.detach();
          delay(500);
          servo_base.write(75);
          delay(1000);
          servo_base.write(105);
          delay(1000);
          servo_top.attach(6);
          servo_top.write(105);
          delay(2050);
          servo_top.detach();
        }
    
  

}
