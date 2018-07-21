int val;
void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  
  val = analogRead(A0);
  Serial.println(val);
  if(digitalRead(2)==LOW){
    analogWrite(9, val/4);
    digitalWrite(11, HIGH);
    digitalWrite(10, LOW);
    delay(200);
  }
  if(digitalRead(3)==LOW){
    analogWrite(9, val/4);
    digitalWrite(11, LOW);
    digitalWrite(10, HIGH);
    delay(200);
  }
  else{
    analogWrite(9, 0);
    digitalWrite(11, LOW);
    digitalWrite(10, LOW);
  }
}
