## 📁 Project Name: `XReconAI`

### 🔥 Description:

> **XReconAI** is a fully autonomous offensive security toolkit designed for bug bounty hunters and security researchers. It automates reconnaissance, vulnerability scanning, exploitation, and report generation — and uses GPT to analyze and explain findings in human-readable format.

## 🚀 Features:

* Automated recon using **subfinder**
* Liveness check with **httpx**
* Vulnerability scanning via **nuclei**
* SQLi exploitation using **sqlmap**
* AI explanation of vulnerabilities using **GPT-4**
* Auto-generated markdown reports
* Docker-ready

## 📂 Folder Structure

```
XReconAI/
├── main.py
├── config.yaml
├── requirements.txt
├── Dockerfile
├── outputs/
└── README.md
```

## 📥 Prerequisites

* Python 3.9+
* Go (for ProjectDiscovery tools)
* OpenAI API Key
* Optional: Docker

## ⚙️ Installation

### 🔧 Install ProjectDiscovery tools:

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```

### 🐍 Install Python requirements:

```bash
pip install -r requirements.txt
```

### 🛠️ Create `config.yaml`

```yaml
openai_api_key: "sk-..."  # Insert your OpenAI API key
```


## ▶️ Usage

### ✅ Basic Run:

```bash
python3 main.py --domain example.com
```

This will:

* Run recon with subfinder
* Check live hosts with httpx
* Scan vulnerabilities with nuclei
* Run sqlmap exploitation
* Use GPT to explain findings
* Save report in `outputs/example.com_report.md`

## 🐳 Docker Support (Optional)

### 📦 Build & Run:

```bash
docker build -t xreconai .
docker run --rm -v $(pwd)/outputs:/app/outputs xreconai --domain example.com
```

## 📄 Sample Output

* `outputs/example.com_subs.txt`
* `outputs/example.com_live.txt`
* `outputs/example.com_nuclei.txt`
* `outputs/example.com_nuclei_explained.txt`
* `outputs/example.com_report.md`


## 🧠 AI Integration

* Uses GPT-4 to explain vulnerabilities in plain English
* Summarizes raw scan results for easier analysis


## 🔐 Disclaimer

This tool is intended for **legal, ethical use only**. Do not scan or exploit systems without proper authorization.
