# 🌐 Internet Speed Twitter Bot

A Python automation bot that:
1. Runs an internet speed test using [Speedtest.net](https://www.speedtest.net).  
2. Compares the results with your promised internet speed.  
3. Automatically posts a complaint to [X (Twitter)](https://x.com) if the speeds are below expectations.  

---

## 🚀 Features
- Measures **download** and **upload** speeds using Selenium.  
- Logs results in `Internet-Speed-bot.log`.  
- Automates login and posting on **X (Twitter)**.  
- Uses a **Chrome profile** to avoid repeated logins.  
- Keeps credentials safe using a `.env` file.  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo
```bash
git clone git@github.com:your-username/internet-speed-bot.git
cd internet-speed-bot

2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies

4️⃣ Setup .env file

Create a .env file in the project root:

x_email=your-email@example.com
x_password=your-password
x_username=your-username

5️⃣ Run the bot
python main.py

🛠 Requirements

Python 3.10+
Google Chrome (latest version)
ChromeDriver (matching Chrome version)
Packages:
    selenium
    python-dotenv

You can install them via:
  pip install selenium python-dotenv

📝 Logging

Logs are written to:
Console output
Internet-Speed-bot.log file

Example:
2025-09-26 20:15:23 - INFO - Download speed 52.34
2025-09-26 20:15:23 - INFO - Upload speed 7.89
2025-09-26 20:15:45 - INFO - Successfully entered the post - Hay Internet Provider...

🙌 Acknowledgments
**Udemy course inspiration

📜 License
MIT © <Anuruddika P>

👋 Contact

Anuruddika Punchihewage
Email: anuruddika.codes@gmail.com · LinkedIn: linkedin.com/in/anuruddika-p-883372385
