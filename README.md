# 📚 Flask Library App

A simple Flask web application to manage authors and books with SQLite and SQLAlchemy.

## 🚀 Features
- Add authors with birth and death dates  
- Add books with title, ISBN, publication year, and author link  
- Display books with cover images (via OpenLibrary API)  
- Search books by title or author  
- Sort books by title or author  
- Delete books (and remove authors if no books remain)  
- Flash messages for user actions  
- Responsive design with centered layout  

## 🛠️ Tech Stack
- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite**
- **HTML/CSS (Jinja2 templates)**

## ⚙️ Setup
1. Clone the repository:
   ```bash
   git clone git@github.com:Edwizio/BookAlchemy.git
   cd library-app

2. Create a virtual environment and activate it:
   ```bash  
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   
3. Install dependencies:
   ```bash 
   pip install -r requirements.txt

4. Run the app:
   ```bash
   flask run

