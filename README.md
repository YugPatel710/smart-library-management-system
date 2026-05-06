# 📚 Smart Library Management System

An AI-powered Smart Library Management System that combines RFID technology, YOLOv8 object detection, OCR, and web technologies to automate book identification and misplaced book detection in libraries.

---

# 🚀 Project Overview

Traditional library systems manage digital records efficiently but cannot verify whether books are physically placed in the correct shelf locations.

This project solves that problem using:

- 📷 Computer Vision (YOLOv8 + OCR)
- 📡 RFID Technology
- 🌐 Web Dashboard
- ⚡ Real-time Detection
- 🧠 Intelligent Majority Rack Detection Algorithm

The system automatically detects misplaced books and improves library management efficiency.

Project developed as part of B.Tech CSE (AI/ML) Minor Project at GSFC University. :contentReference[oaicite:0]{index=0}

---

# ✨ Features

## 📷 AI-Based Book Detection
- YOLOv8 object detection for identifying books
- OCR fallback mechanism using Tesseract OCR
- Real-time shelf image processing

## 📡 RFID Integration
- ESP32 + MFRC522 RFID module
- Accurate RFID-based book identification
- Hybrid detection system

## 📊 Smart Dashboard
- Real-time scan results
- Misplaced book alerts
- Activity logs
- Shelf and rack tracking

## 🧠 Majority Rack Detection Algorithm
- Automatically identifies correct rack
- Detects misplaced books intelligently

## 🌐 Web Application
- Flask-based backend
- HTML/CSS/JavaScript frontend
- REST API integration

---

# 🏗️ System Architecture

The project uses a 5-layer architecture:

1. Presentation Layer
   - Web Interface
   - Mobile Application

2. Business Logic Layer
   - Spring Boot REST API

3. Detection & Processing Layer
   - Flask Microservice
   - YOLOv8
   - OCR

4. Data Layer
   - MySQL Database

5. Hardware Layer
   - ESP32
   - MFRC522 RFID Reader

Architecture details are explained in the project report. :contentReference[oaicite:1]{index=1}

---

# 🛠️ Technologies Used

## Programming Languages
- Python
- JavaScript
- Java
- SQL

## Frameworks & Libraries
- Flask
- Spring Boot
- OpenCV
- YOLOv8
- Tesseract OCR

## Frontend
- HTML
- CSS
- JavaScript

## Database
- MySQL

## Hardware
- ESP32
- MFRC522 RFID Reader

## Tools
- VS Code
- Arduino IDE
- GitHub
- Google Colab

---

# 📂 Project Structure

```text
smart-library-management-system/
│
├── backend/
├── frontend/
├── python-ocr-service/
├── database/
├── images/
├── uploads/
├── setup_database.sql
├── requirements.txt
└── README.md
