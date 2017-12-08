char incoming;

void setup() {
	Serial.begin(9600);
}

void loop() {
	incoming = Serial.read();
	if (incoming = 's') {
		Serial.println(incoming);
	}
}

