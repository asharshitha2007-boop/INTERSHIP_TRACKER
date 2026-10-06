# 🎓 AI Internship Tracker

An AI-powered web application that helps students discover and manage internship opportunities in one place. The application uses **Streamlit, Python, SQLite, and Gemini AI** to provide a simple and useful internship-tracking experience.

## 🚀 Features

- 🔍 Search and find internship opportunities
- 🤖 AI-powered assistance using Google Gemini
- 📋 Store internship details in a database
- 🏢 Save company and job role information
- 🛠️ Store required skills
- 📍 Store internship location
- 🔗 Save application links
- 📊 Track internship application status
- 💻 Simple and user-friendly Streamlit interface

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – Web application interface
- **Google Gemini API** – AI functionality
- **SQLite** – Database
- **Pandas** – Data handling
- **python-dotenv** – Environment variable management

## 📁 Project Structure

```text
PROJECT_AI/
│
├── app.py
├── requirements.txt
├── key.env.example
├── internships.db
├── README.md
└── ...
```

> ⚠️ The `venv` folder should not be uploaded to GitHub or included in the project ZIP.

## ⚙️ Installation

### 1. Clone or download the project

Download the project and open the project folder in PowerShell or Command Prompt.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project without activating the environment by using:

```bash
venv\Scripts\python.exe -m streamlit run app.py
```

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

## 🔑 Gemini API Key Setup

The application uses the **Google Gemini API**.

Create a file named:

```text
key.env
```

Inside the file, add:

```text
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Replace `YOUR_API_KEY_HERE` with your own Gemini API key.

### ⚠️ Security

Never upload your actual API key to GitHub or share it publicly.

The project includes `key.env.example` as a template:

```text
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

## ▶️ Run the Application

After installing the required packages, run:

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## 🗄️ Database

The project uses **SQLite** to store internship information.

Database:

```text
internships.db
```

The internship table stores information such as:

- Company
- Role
- Skills
- Location
- Application Link
- Application Status

## 🎯 Project Objective

The main objective of this project is to create a simple platform that helps students manage internship opportunities efficiently.

Instead of searching for internships and maintaining information manually in different places, students can use one application to organize and track internship opportunities.

## 👩‍💻 Developed For

This project was developed as a **student AI/Software Development project** to demonstrate practical knowledge of:

- Python programming
- AI API integration
- Database management
- Streamlit application development
- Environment variable management
- Basic software project structure

## 🔮 Future Enhancements

Possible future improvements include:

- 🔔 Internship deadline reminders
- 🎯 Resume-based internship recommendations
- 📧 Email notifications
- 📊 Application progress dashboard
- 🔎 Advanced internship filtering
- 📄 Resume upload and skill matching
- 🌐 Automatic internship data collection from supported sources

## 📌 Note

This project is intended for educational and demonstration purposes. Internship availability and application information may change over time.

---

### ⭐ Project Highlights

**Project:** AI Internship Tracker  
**Language:** Python  
**Frontend:** Streamlit  
**AI:** Google Gemini  
**Database:** SQLite  
**Data Processing:** Pandas