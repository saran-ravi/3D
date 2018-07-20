#include<EEPROM.h>
int a[2];
void blink(int a, int b){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(a*1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(b*1000);
}

char ser(){
  char ch;
  if(Serial.available()>0){
    ch = Serial.read();
  }
  ch = ch-48;
  if ((ch>0) && (ch <10))
    return ch;
}

void interupt(){
    delay(500);
    Serial.println("Reset EEPROM sucessfully");
    EEPROM.write(0, 1);
    EEPROM.write(1, 1);
    a[0] = EEPROM.read(0);
    a[1] = EEPROM.read(1);
}


void setup(){
  delay(5000);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), interupt, CHANGE);
  Serial.begin(9600);
  Serial.print("give th, tl\n");
  delay(8000);
  for(int i=0; i<2; i++){
    a[i] = ser();
  }
  if(((a[0]!=92)&&(a[1]!=92))&&((a[0]!=0)&&(a[1]!=0))){
    Serial.println("Wrote EEPROM sucessfully");
    EEPROM.write(0, a[0]);
    EEPROM.write(1, a[1]);
  }
  a[0] = EEPROM.read(0);
  a[1] = EEPROM.read(1);
}

void loop(){
  blink(a[0],a[1]);
  
  for(int i=0; i<2; i++){
    //a[i] = ser();
    Serial.print(a[i]);
    Serial.print(' ');
  }
  Serial.println();
  
}
