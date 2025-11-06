# 📘 ASQAG – Automatic Short Answer Question Generator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20NLTK-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![GitHub stars](https://img.shields.io/github/stars/isonukumarp368/ASQAG?style=social)

ASQAG (Automatic Short Answer Question Generator) is a Flask-based NLP application that automatically generates short-answer questions and answers from text input. It is designed around Bloom’s Taxonomy, making it useful for educational assessments, e-learning platforms, and smart quizzes.

The project comes with a modern web interface (HTML + CSS + JS + assets) for user interaction.

---

## 🚀 Features

- 🌐 Flask Web App with clean UI
- 📄 Multiple Templates (index, result, layout, mainPage, greet)
- 🎨 Custom Styling with CSS + JS + image assets
- 🤖 Automatic Q&A Generation using NLP (NLTK + spaCy)
- 🧠 Bloom’s Taxonomy Alignment – Generates questions across six cognitive levels
- 📊 Evaluation Metrics (Precision, Recall, F1-score, Semantic Similarity)
- 🖼 Custom Icons & Assets (backgrounds, favicons, exam icons)

---

## 📂 Project Structure

```bash
ASQAG/
│── app.py                  # Main Flask app
│── requirements.txt         # Dependencies
│
├── static/                  # Frontend static assets
│   ├── assets/
│   │   ├── img/             # Backgrounds & images
│   │   │   ├── bg.png
│   │   │   ├── bgg.png
│   │   │   ├── icon.png
│   │   ├── exam.ico
│   │   ├── favicon.ico
│   ├── css/
│   │   └── styles.css       # Styling
│   ├── js/
│       └── scripts.js       # Client-side interactivity
│
├── templates/               # HTML Templates
│   ├── index.html           # Input page
│   ├── resultPage.html      # Display results
│   ├── mainPage.html        # Main landing page
│   ├── greet.html           # Welcome screen
│   └── layout.html          # Shared layout template
│
└── .vscode/                 # VSCode settings
    └── launch.json
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/isonukumarp368/ASQAG.git
cd ASQAG
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Download spaCy Model
```bash
python -m spacy download en_core_web_lg
```

---

## ▶️ Usage

Run Flask App:
```bash
python app.py
```

App will be available at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

**Workflow**
1. Open the app in your browser.
2. Enter a text passage into the input field.
3. Select Bloom’s Level + number of questions.
4. Generate automatic Q&A pairs.
5. View results in resultPage.html.

---

## 📊 Example

**Input:**
```text
Ravi is a boy. He loves reading books and playing cricket.
```

**Generated Output:**
- **Level 1 (Remember):** Who is Ravi? → Ravi is a boy.
- **Level 2 (Understand):** Can you explain why Ravi loves reading books?
- **Level 3 (Apply):** How would you apply Ravi’s habit of reading to your daily routine?
- **Level 4 (Analyze):** What are the components of Ravi’s hobbies?
- **Level 5 (Evaluate):** Do you agree reading makes Ravi a better student? Why/why not?
- **Level 6 (Create):** Can you design a story where Ravi’s love for cricket changes his life?


## 📌 Future Enhancements

- 📊 Integration with Tableau/Streamlit dashboards for visualization
- 🖼 Support for Image → Text → Q&A (OCR + BLIP model)
- 🤖 Transformer-based models (T5, BART, Flan-T5) for more natural questions

---

## 👨‍💻 Author

Developed by Krishna Shree Tripathy 
Based on Bloom’s Taxonomy framework for educational Q&A
