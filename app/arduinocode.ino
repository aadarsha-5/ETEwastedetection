#include <Servo.h>

#define SERVO_PIN_1 9 // Digital PWM pin for servo motor 1
#define SERVO_PIN_2 10 // Digital PWM pin for servo motor 2

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600); // Initialize serial communication
  servo1.attach(SERVO_PIN_1); // Attach servo motor 1 to its pin
  servo2.attach(SERVO_PIN_2); // Attach servo motor 2 to its pin
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available to read
    char signal = Serial.read(); // Read the incoming signal
    
    if (signal == 'B') { // If signal is 'B', rotate motors in one direction
      servo1.write(180); // Rotate servo motor 1 in one direction
      servo2.write(0); // Rotate servo motor 2 in the same direction
      delay(5000); // Wait for 5 seconds (adjust as needed)
    } else if (signal == 'N') { // If signal is 'N', rotate motors in opposite direction
      servo1.write(0); // Rotate servo motor 1 in opposite direction
      servo2.write(180); // Rotate servo motor 2 in the same opposite direction
      delay(5000); // Wait for 5 seconds (adjust as needed)
    }
  }
}
