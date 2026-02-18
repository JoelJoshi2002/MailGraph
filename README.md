# MailGraph



---

## 📌 Table of Contents

- About
- Features
- Project Structure
- Getting Started
- Installation
- How to Use
- Configuration
- Contributing
- License

---

## 📙 About

MailGraph is aimed at parsing and visualizing email log data, generating insights or visual representations of mail statistics.  
It is structured modularly to help scale the project as complexity increases.

---

## 📌 Features

✔ Modular code structure  
✔ Separates agents, tools, and data processing  
✔ Clean virtual environment management  
✔ Designed for extension and experimentation

---

## 📂 Project Structure

.orch/ — orchestrator configs  
agents/ — logic modules  
data/ — raw or sample data  
outputs/ — generated graphs/results  
state/ — logs or state files  
tools/ — helper utilities  
main.py — main executable script  

---

## 🚀 Getting Started

Clone the repository:

git clone https://github.com/JoelJoshi2002/MailGraph.git  
cd MailGraph

---

## 🛠 Installation

Create virtual environment:

python -m venv .venv

Activate:

Windows:
.venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

---

## ▶ How to Use

Run the project:

python main.py

---

## ⚙️ Configuration

Store environment variables in a `.env` file:

MAIL_LOG_PATH=path/to/log  
OUTPUT_DIR=outputs/

Make sure `.env` is not tracked in Git.

---

## 🤝 Contributing

1. Fork the repo  
2. Create branch  
3. Commit changes  
4. Push  
5. Open PR

---

## 📄 License

MIT License — see LICENSE file.

---

Happy coding 🚀
