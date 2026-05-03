#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pines
int pinSensor = 2;
int pinLED = 3;

// Estado sonido
int estado = 0;
// Estado Led
int estadoAnterior = HIGH;

bool iniciado = false;
bool terminado = false;

unsigned long inicio = 0;
unsigned long ultimaResp = 0;

int respiraciones = 0;
bool apneaDetectada = false;

int tiempoMinResp = 2000;

unsigned long tiempoLED = 0;
bool ledEncendido = false;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);

  pinMode(pinSensor, INPUT);
  pinMode(pinLED, OUTPUT);
  digitalWrite(pinLED, HIGH);

  lcd.print("Respira...");
}

void loop() {
  if (terminado) return;

  estado = digitalRead(pinSensor);

   // ENCENDER LED
  if (estado == LOW && estadoAnterior == HIGH) {
    digitalWrite(pinLED, LOW);
    ledEncendido = true;
    tiempoLED = millis();
  }

  // APAGAR LED
  if (ledEncendido && millis() - tiempoLED >= tiempoMinResp) {
    digitalWrite(pinLED, HIGH);
    ledEncendido = false;
  }

  estadoAnterior = estado;

  // iniciar cuando detecta sonido (respiración)
  if (!iniciado && estado == LOW) {
    iniciado = true;
    inicio = millis();
    ultimaResp = millis();
    respiraciones = 1;
    Serial.println("RESP");

    lcd.clear();
  }

  if (iniciado) {
    // detectar respiración (con tiempo mínimo)
    if (estado == LOW && millis() - ultimaResp > tiempoMinResp) {
      respiraciones++;
      ultimaResp = millis();

      Serial.println("RESP");
    }

    // tiempo
    int tiempo = (millis() - inicio) / 1000;

    // mostrar
    lcd.setCursor(0, 0);
    lcd.print("Tiempo:");
    lcd.print(60 - tiempo);
    lcd.print("s ");

    lcd.setCursor(0, 1);
    lcd.print("Resp:");
    lcd.print(respiraciones);
    lcd.print("   ");

    // apnea
    if (millis() - ultimaResp > 10000) {
      apneaDetectada = true;
    }

    // fin en 60s
    if (tiempo >= 60) {
      lcd.clear();

      lcd.setCursor(0, 0);
      lcd.print("RPM:");
      lcd.print(respiraciones);

      lcd.setCursor(0, 1);

      String estadoResp = "";

      if (apneaDetectada) {
        lcd.print("Apnea detectada");
        estadoResp = "Apnea detectada";
      } else {
        if (respiraciones < 12) {
          lcd.print("Bradipnea");
          estadoResp = "Bradipnea";
        } else if (respiraciones > 20) {
          lcd.print("Taquipnea");
          estadoResp = "Taquipnea";
        } else {
          lcd.print("Eupnea");
          estadoResp = "Eupnea";
        }
      }

      Serial.print("RPM:");
      Serial.print(respiraciones);
      Serial.print(",ESTADO:");
      Serial.println(estadoResp);

      terminado = true;
    }
  }

  delay(50);
}