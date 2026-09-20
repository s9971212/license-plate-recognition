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

[English](./README.md) | 中文

## <br/> 📋 目錄

- ✨ [簡介](#introduction)
- ⚙️ [技術堆疊](#tech-stack)
- 🚀 [快速入門](#quick-start)

## <br/> <a name="introduction">✨ 簡介</a>

這是一套以 Python 開發的即時車牌辨識系統，主要用於處理來自監控攝影機的串流影像。系統可透過 RTSP 等協定連接 IP Camera，定期擷取影像畫面，偵測畫面中的車輛與車牌，並透過光學字元辨識（OCR）技術辨識車牌號碼。

系統採用模組化架構設計，方便整合或替換不同的攝影機來源、車輛/車牌偵測模型以及文字辨識引擎。可應用於停車場管理、門禁控制、交通監控、自動車輛辨識等相關場景。

在資料儲存方面，採用 MySQL 作為關聯式資料庫管理系統 (RDBMS)。MySQL 的高可靠性和高效率可確保有效管理和查詢大型資料集。

<br/>**主要功能**

- 透過 RTSP 連接 IP Camera 並擷取即時影像串流

- 定期擷取並處理攝影機畫面

- 偵測影像中的車輛與車牌

- 使用 OCR 辨識車牌文字

- 支援即時或近即時的車牌辨識流程

- 採用模組化架構，方便整合不同的偵測與辨識模型

- 使用環境變數管理可調整的執行設定

## <br/> <a name="tech-stack">⚙️ 技術堆疊</a>

- Python
- opencv-python [📄](https://pypi.org/project/opencv-python/)
- ultralytics [📄](https://www.ultralytics.com/)
- pytest
- SQLAlchemy [📄](https://www.sqlalchemy.org/=)
- MySQL [📄](https://www.mysql.com/)

## <br/> <a name="quick-start">🚀 快速入門</a>

請依照以下步驟在您的電腦本機設定專案：

<br/>**必備條件**

確保您的電腦已安裝以下軟體：

- [Python](https://www.python.org/downloads/)
- [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows) | [Visual Studio Code](https://code.visualstudio.com/download?_exp_download=d53503e735)
- [MySQL](https://www.mysql.com/downloads/)
- [Git](https://git-scm.com/)

<br/>**複製儲存庫**

```bash
git clone {git remote url}
```

<br/>**建立虛擬環境**

```bash
python -m venv .venv
```

<br/>**安裝專案相依套件**

```bash
pip install -e .
```

<br/>**建立 .env**

以下是如何複製 .env.example 並在您的電腦上建立新的 .env：

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

<br/>**執行測試**

安裝完所有內容並設定 .env 後，請執行：

```bash
pytest
```

如果所有測試都通過，您的環境很可能已正確設定。

<br/>**啟動應用程式**

```bash
python -m license_plate_recognition.main
```
