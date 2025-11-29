# 🕵️‍♂️ RTLO Extension Spoofer (Educational Tool)

This project is a Python tool developed to demonstrate the **"Extension Spoofing"** technique for cybersecurity education and awareness training.

It simulates the method used by attackers to disguise executable files (e.g., `.exe`, `.bat`) as harmless documents (e.g., `.pdf`, `.jpg`) by leveraging the **Unicode Right-to-Left Override (RTLO - U+202E)** character.

---

## ⚠️ Disclaimer

> **WARNING:** This software is for **EDUCATIONAL AND TESTING PURPOSES ONLY.**
>
> This tool is designed to demonstrate to students, security professionals, and system administrators how file extensions can be obfuscated. Misuse of this code to gain unauthorized access, deceive users, or disseminate malware is strictly prohibited and illegal. The developer assumes no liability for any misuse of this tool.

---

## 🎯 Features

* **GUI-Based File Selection:** Easy file selection using the `tkinter` interface.
* **Multi-Format Support:** Pre-configured options for common formats like PDF, JPG, PNG, and TXT.
* **Manual Input:** Ability to test custom extensions (e.g., `docx`, `xlsx`, `mp3`) via manual entry.
* **Visual Simulation:** Displays a simulation of how the file will look to the **victim** vs. how the file is named in the **system** before applying changes.
* **Sanitization Bypass:** Includes specific logic to allow the RTLO character (`\u202e`) for educational demonstration.

## 🛠️ Installation

You only need Python 3.x installed on your machine. No external dependencies are required as it uses standard libraries.

