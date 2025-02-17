void setup() {
    Serial.begin(115200);
}

void loop() {
    int msg = random(0,3);
    int x = random(0, 300);
    int y = random(0, 400);

    Serial.print(1);
    Serial.print(',');
    Serial.print(msg);
    Serial.print(',');
    Serial.print(x);
    Serial.print(',');
    Serial.println(y);
    delay(1000); // Send update every second
}
