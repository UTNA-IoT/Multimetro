int SensorVoltaje = A0;
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:

}

void loop() {
  float voltaje=(float)25*analogRead(SensorVoltaje)/1023;
  Serial.println(voltaje);
  delay(1000);
  // put your main code here, to run repeatedly:

}
