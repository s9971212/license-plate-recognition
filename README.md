# license-plate-recognition

![LICENSE](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PyCharm](https://img.shields.io/badge/PyCharm-blue)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-blue)  
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.2.3-orange)
![opencv-python](https://img.shields.io/badge/opencv--python-5.0.0.93-orange)
![ultralytics](https://img.shields.io/badge/ultralytics-8.4.150-orange)
![paddleocr](https://img.shields.io/badge/paddleocr-3.7.0-orange)
![paddlepaddle](https://img.shields.io/badge/paddlepaddle-3.3.1-orange)
![pytest](https://img.shields.io/badge/pytest-9.1.1-orange)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.53-orange)
![PyMySQL](https://img.shields.io/badge/PyMySQL-1.2.0-orange)  
![MySQL](https://img.shields.io/badge/MySQL-8.0.33-green)

English | [中文](./README_zh-TW.md)

## <br/> 📋 Table of Contents

- ✨ [Introduction](#introduction)
- ⚙️ [Tech Stack](#tech-stack)
- 🚀 [Quick Start](#quick-start)

## <br/> <a name="introduction">✨ Introduction</a>

A Python-based real-time license plate recognition system designed to process video streams from surveillance cameras. The system connects to camera streams using protocols such as RTSP, periodically captures video frames, detects vehicles and license plates, and extracts license plate numbers using optical character recognition (OCR).

The system is designed with a modular architecture, allowing different camera sources, detection models, and recognition engines to be integrated or replaced easily. It can serve as a foundation for applications such as parking management, access control, traffic monitoring, and automated vehicle identification.

For data storage, MySQL is used as the Relational Database Management System (RDBMS). The high reliability and efficiency of MySQL ensures that large datasets can be managed and queried efficiently.

<br/>**Key Features**

- Connect to IP cameras and real-time video streams via RTSP.

- Periodically capture and process video frames.

- Detect license plates from captured frames.

- Recognize and extract license plate numbers using OCR.

- Support real-time or near-real-time license plate recognition workflows.

- Provide a modular architecture for integrating different detection and recognition models.

- Use environment variables for configurable runtime settings.

## <br/> <a name="tech-stack">⚙️ Tech Stack</a>

- Python
- opencv-python [📄](https://pypi.org/project/opencv-python/)
- ultralytics [📄](https://www.ultralytics.com/)
- pytest
- SQLAlchemy [📄](https://www.sqlalchemy.org/=)
- MySQL [📄](https://www.mysql.com/)

## <br/> <a name="quick-start">🚀 Quick Start</a>

Follow these steps to set up the project locally on your machine.

<br/>**Prerequisites**

Make sure you have the following installed on your machine:

- [Python](https://www.python.org/downloads/)
- [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows) | [Visual Studio Code](https://code.visualstudio.com/download?_exp_download=d53503e735)
- [MySQL](https://www.mysql.com/downloads/)
- [Git](https://git-scm.com/)

<br/>**Cloning Repository**

```bash
git clone {git remote url}
```

<br/>**Create virtual environment**

```bash
python -m venv .venv
```

<br/>**Install project dependencies**

```bash
pip install -e .
```

<br/>**Create .env file**

Here is how you can copy .env.example to create a new .env on your computer:

macOS / Linux
```bash
cp .env.example .env
```

Windows (Command Prompt / CMD)
```bash
copy .env.example .env
```

Windows (PowerShell)
```bash
Copy-Item .env.example .env
```

<br/>**Run tests**

After installing everything and configuring .env, run:

```bash
pytest
```

If all tests pass, your environment is probably set up correctly.

<br/>**Start application**

```bash
python -m license_plate_recognition.main
```
