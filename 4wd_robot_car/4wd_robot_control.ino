#include <WiFi.h>
#include <WebServer.h>

WebServer server(80);

// AP credentials
const char* ssid = "ESP32_Robot";
const char* password = "12345678";

// Motor pins
#define IN1 5
#define IN2 18
#define IN3 19
#define IN4 21
#define IN5 26
#define IN6 25
#define IN7 33
#define IN8 32

// ================= MOTOR FUNCTIONS =================

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW); digitalWrite(IN6, LOW);
  digitalWrite(IN7, LOW); digitalWrite(IN8, LOW);
}

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  digitalWrite(IN5, HIGH); digitalWrite(IN6, LOW);
  digitalWrite(IN7, HIGH); digitalWrite(IN8, LOW);
}

void backward() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  digitalWrite(IN5, LOW); digitalWrite(IN6, HIGH);
  digitalWrite(IN7, LOW); digitalWrite(IN8, HIGH);
}

void left() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  digitalWrite(IN5, HIGH); digitalWrite(IN6, LOW);
  digitalWrite(IN7, HIGH); digitalWrite(IN8, LOW);
}

void right() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW); digitalWrite(IN6, HIGH);
  digitalWrite(IN7, LOW); digitalWrite(IN8, HIGH);
}

// ================= WEB UI =================


void handleRoot() {
  String html = R"rawliteral(
  <!DOCTYPE html>
  <html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body { text-align: center; font-family: Arial; }
      button {
        width: 120px; height: 60px;
        font-size: 16px; margin: 8px;
      }
    </style>
  </head>
  <body>
    <h2>Robot Control</h2>

    <div>
      <button ontouchstart="send('forward')" ontouchend="send('stop')">FORWARD</button>
    </div>

    <div>
      <button ontouchstart="send('left')" ontouchend="send('stop')">LEFT</button>
      <button onclick="send('stop')">STOP</button>
      <button ontouchstart="send('right')" ontouchend="send('stop')">RIGHT</button>
    </div>

    <div>
      <button ontouchstart="send('backward')" ontouchend="send('stop')">BACKWARD</button>
    </div>

    <script>
      function send(cmd) {
        fetch("/" + cmd);
      }
    </script>
  </body>
  </html>
  )rawliteral";

  server.send(200, "text/html", html);
}


// ================= SETUP =================

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(IN5, OUTPUT); pinMode(IN6, OUTPUT);
  pinMode(IN7, OUTPUT); pinMode(IN8, OUTPUT);

  stopMotors();

  // Start Access Point
  WiFi.softAP(ssid, password);

  // Routes
  server.on("/", handleRoot);
  server.on("/forward", [](){ forward(); server.send(200, "text/plain", "OK"); });
  server.on("/backward", [](){ backward(); server.send(200, "text/plain", "OK"); });
  server.on("/left", [](){ left(); server.send(200, "text/plain", "OK"); });
  server.on("/right", [](){ right(); server.send(200, "text/plain", "OK"); });
  server.on("/stop", [](){ stopMotors(); server.send(200, "text/plain", "OK"); });

  server.begin();
}

void loop() {
  server.handleClient();
}
