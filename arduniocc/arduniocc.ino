int in1 = 7;
int in2 = 8;
int enA = 9;
int motorSpeed = 50;
int LED = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(LED, OUTPUT);
  analogWrite(enA, motorSpeed);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    int msg = Serial.read();
    Serial.println(msg);
    if (msg == 'B') {
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(LED, HIGH);
    } else if (msg == 'N') {
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(LED, HIGH);
    } else {
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      digitalWrite(LED, LOW);
    }
  }
}
