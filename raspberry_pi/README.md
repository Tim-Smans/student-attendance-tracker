# 🧠 How to Set Up a New Device

This guide helps you set up a brand-new device for use in the smart monitoring system.

> You do **not** need to connect any hardware for the initial setup. Everything can be done without sensors or a camera plugged in.

---

## ✅ Prerequisites

- Raspberry Pi (Recommended: Pi 3 or newer)
- SD Card (at least 16GB!)
- Raspberry Pi Imager or Balena Etcher
- HDMI screen, keyboard and mouse (Or knowledge of SSH)
- Internet connection
- Valid API key

---

## 📦 Step 1: Flash the Custom OS Image

1. Visit the dashboard:  
   [Dashboard: New device](https://tracker.timsmans.be/new-device)

2. Click on the **“Download image”** button.

3. Save the image to your computer.

4. Open your imaging software (e.g., Raspberry Pi Imager).

5. Select your Raspberry Pi model and choose **Custom OS** under Operating System.

6. Select the image file you just downloaded.

7. Choose your SD card as the target storage.

8. When prompted, **do not enable custom settings**.

9. Let the flashing process complete, then safely eject the SD card.

---

## 🖥️ Step 2: Desktop Setup (Recommended)

1. Insert the flashed SD card into your Raspberry Pi.

2. Connect a screen, keyboard, and mouse.

3. Power up the device.

4. Once the OS boots, a terminal window will appear and automatically start the setup process.

5. You will be prompted to:
   - Set a **unique hostname**
   - Confirm/change Wi-Fi (should be pre-configured)
   - Enter the **room name**
   - Enter the **API key**

6. You may be asked to confirm with `'y'` during the process—go ahead and do so.

7. When completed, you should see:

Device setup correctly, ...


> 💡 **Headless setup (SSH)** is also supported. Just SSH into the Pi after flashing, and the same setup flow will run in your terminal.

---

## 🔌 Step 3: Connect Camera & Sensors

> ❗️Power **off** your Raspberry Pi before connecting any hardware. Some components do **not** support hot-plugging.

### 🧩 Required components:

- Raspberry Pi AI Camera
- PIR Motion Sensor

### 🧩 Optional supported sensors:

- Ultrasonic Ranger Sensor  
- RGB LED  
- LCD Screen (I2C 16x2 Grove-compatible)

These will be automatically detected and enabled at startup if connected.

---

## 🧷 GPIO Pin Connections

Use the [pinout.xyz](https://pinout.xyz/) map as a reference.

### PIR Motion Sensor

| Pin | GPIO |
|-----|------|
| GND | Ground |
| VCC | 5V |
| D1  | GPIO 17 |
| NC  | *Do not connect* |

### Ultrasonic Ranger

| Pin | GPIO |
|-----|------|
| GND | Ground |
| VCC | 5V |
| SIG | GPIO 26 |
| NC  | *Do not connect* |

### LCD Screen (I2C)

| Pin | GPIO |
|-----|------|
| GND | Ground |
| VCC | 5V |
| SDA | GPIO 2 |
| SCL | GPIO 3 |

### RGB LED

| Pin  | GPIO |
|------|------|
| GND  | Ground |
| Red  | GPIO 23 |
| Green| GPIO 24 |
| Blue | GPIO 25 |

---

## ✅ Final Step

1. Power the device back on with all hardware connected.

2. The system will now automatically enable the supported sensors and services.

3. You're ready to go 🎉

---
