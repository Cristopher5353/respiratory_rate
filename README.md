# Sistema de Monitoreo Respiratorio en Tiempo Real (Arduino + Python)

Este proyecto es un sistema IoT/Embebido diseñado para medir, monitorear y diagnosticar la frecuencia respiratoria en tiempo real. Utiliza un microcontrolador **Arduino** conectado a un sensor de sonido/respiración y una pantalla LCD, integrado mediante comunicación serial con una interfaz gráfica (GUI) en **Python (Tkinter + Matplotlib)** para el registro de pacientes y la visualización de la gráfica respiratoria en vivo.

---

## 📋 Características Principales

* **Detección Automática de Respiración:** Captura impulsos de respiración/sonido y calcula las Respiraciones Por Minuto (RPM) en un intervalo de 60 segundos.
* **Diagnóstico Automatizado:** Clasifica el estado del paciente según sus lecturas:
  * **Eupnea:** Frecuencia normal (12 - 20 RPM).
  * **Bradipnea:** Frecuencia baja (< 12 RPM).
  * **Taquipnea:** Frecuencia elevada (> 20 RPM).
  * **Apnea Detectada:** Inactividad respiratoria continua por más de 10 segundos.
* **Feedback Visual Local:** Pantalla LCD I2C (16x2) y un indicador LED sincronizado con cada evento respiratorio.
* **Interfaz de Usuario Desktop (GUI):**
  * Gestión básica y selección de pacientes en una tabla interactiva (`ttk.Treeview`).
  * Visualización en tiempo real de la onda respiratoria utilizando `matplotlib` y buffers circulares (`collections.deque`).
  * Actualización automática del diagnóstico en la tabla al finalizar el ciclo de prueba.
* **Ejecución Multi-hilo:** Uso de `threading` en Python para evitar el congelamiento de la GUI mientras se reciben los datos por el puerto serial.

---

## 🛠️ Arquitectura del Sistema

```text
[ Sensor de Sonido / Proximidad ]
               │
               ▼
       [ Arduino Uno / Nano ] ──(I2C)──► [ LCD 16x2 (0x27) ]
               │             ──(Pin)──► [ LED Indicador ]
               │ (USB Serial / 9600 baud)
               ▼
    [ Aplicación Python GUI ]
      ├── Tkinter (Gestión Pacientes)
      └── Matplotlib (Gráfica en vivo)
```

---

## 🧰 Requisitos de Hardware y Software

### Hardware
* 1x Placa Arduino (Uno, Nano o Mega)
* 1x Sensor Digital de Sonido / Micrófono o Módulo de entrada digital (Pin D2)
* 1x Pantalla LCD 16x2 con adaptador I2C (Dirección `0x27`)
* 1x LED y resistencia de 220Ω (Pin D3)
* Cables de conexión (Jumper Wires)
* Cable USB para conexión Serial PC-Arduino

### Software y Librerías

#### En Arduino IDE:
* **Wire** (Incluida por defecto en Arduino)
* **LiquidCrystal_I2C** (Instalar desde el Gestor de Librerías)

#### En Python (3.8+):
Instalar las dependencias necesarias mediante `pip`:

```bash
pip install pyserial matplotlib
```
*(Nota: `tkinter`, `threading`, `time` y `collections` vienen incluidos de forma nativa en la instalación estándar de Python).*

---

## 🔌 Conexiones de Hardware (Diagrama de Pines)

| Componente | Pin Componente | Pin Arduino | Notas |
| :--- | :--- | :--- | :--- |
| **Sensor Digital** | OUT / DOUT | **D2** | Configurado como `INPUT` |
| **LED** | Ánodo (+) | **D3** | Lógica invertida (Active LOW) |
| **LCD I2C** | SDA | **A4** (Arduino Uno) | Bus I2C Data |
| **LCD I2C** | SCL | **A5** (Arduino Uno) | Bus I2C Clock |
| **LCD / Sensor** | VCC | **5V** | Alimentación general |
| **LCD / Sensor** | GND | **GND** | Tierra común |

---

## 📂 Estructura del Proyecto

```text
├── arduino_respiracion.ino  # Código fuente para la placa Arduino
├── app_monitoreo.py        # Código fuente de la interfaz gráfica en Python
└── README.md               # Documentación del proyecto
```

---

## 🚀 Guía de Instalación y Uso

### 1. Cargar el código en Arduino
1. Conecta la placa Arduino a tu PC vía USB.
2. Abre `arduino_respiracion.ino` en el **Arduino IDE**.
3. Verifica que la dirección I2C de la pantalla LCD sea `0x27` (si usas un modelo diferente, actualiza la línea `LiquidCrystal_I2C lcd(0x27, 16, 2);`).
4. Selecciona tu placa y la herramienta de puerto COM correspondiente.
5. Sube el código al Arduino.

### 2. Configurar y ejecutar la GUI en Python
1. Identifica el puerto COM asignado a tu Arduino (ej. `COM3`, `COM4` en Windows o `/dev/ttyUSB0` en Linux).
2. Abre el archivo `app_monitoreo.py` y actualiza la constante `PUERTO` según corresponda:
   ```python
   PUERTO = "COM4"  # Cambia por el puerto COM de tu sistema
   ```
3. Ejecuta la aplicación desde la terminal:
   ```bash
   python app_monitoreo.py
   ```

### 3. Operación
1. En la ventana principal, **selecciona un paciente** haciendo clic en una fila de la tabla.
2. Presiona el botón **"Iniciar Medición"**.
3. Se abrirá una ventana secundaria con la **gráfica en tiempo real**. El contador en el LCD del Arduino iniciará un conteo regresivo de **60 segundos**.
4. Al finalizar la prueba:
   * El LCD y la GUI mostrarán el resultado final (**RPM** y el **Estado / Diagnóstico**).
   * La tabla de pacientes en Python se actualizará automáticamente con las nuevas lecturas.

---

## 📄 Licencia

Proyecto desarrollado y prototipado mecatrónico/médico. Libre de modificar y distribuir.
