# 🔁 SkillSwap API

SkillSwap is a fast, flexible skill exchange API server where users can offer and request skills, get matched with others, and log exchanges.

---

## 1. 📦 Features

- User CRUD operations
- Skill-based matching logic
- Record & retrieve skill exchanges
- Interactive UI for skill match
- High test coverage with pytest
- SQLite-backed database with SQLAlchemy ORM

---

## 2. 🛠️ Installation and Setup

### Clone the repository:

```bash
git clone https://github.com/your-username/SkillSwapAPI.git
cd SkillSwapAPI
Create and activate a virtual environment:
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   
Install required packages:
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is missing, you can generate it:

bash
Copy
Edit
pip freeze > requirements.txt
3. 🗃️ Initialize the Database
This project uses SQLite. To create the database tables:

bash
Copy
Edit
python main.py
This runs the following code:

python
Copy
Edit
Base.metadata.create_all(bind=engine)
🧪 To confirm the database was created:

bash
Copy
Edit
dir skill_swap.db 
4. 🧪 Run Tests with Coverage
To run all tests and generate coverage:

bash
Copy
Edit
pytest --cov=crud --cov=main --cov-report=term-missing --cov-report=html
term-missing: shows uncovered lines in terminal

html: generates a detailed visual report

To open the report:

bash
Copy
Edit
start htmlcov\index.html 
5. 📬 API Endpoints
Method	Endpoint	Description
GET	/	Root message
POST	/users/	Create a new user
GET	/users/{id}	Retrieve user details
PUT	/users/{id}	Update user info
DELETE	/users/{id}	Delete user
POST	/match/	Get list of matched users
POST	/exchange/	Record a skill exchange
GET	/exchanges/	View all skill exchanges
GET	/match_ui	UI to display matched users

6. 📁 Project Structure
pgsql
Copy
Edit
SkillSwapAPI/
├── crud.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── templates/
│   └── match.html
├── tests/
│   ├── test_api.py
│   ├── test_integration.py
│   └── test_unit.py
├── skill_swap.db
├── requirements.txt
└── README.md
7. ✅ Testing Summary
🧪 Unit + integration + API tests using pytest

✔️ Achieves 90%+ code coverage

📊 Report available in htmlcov/index.html

8. 🙋‍♀️ Author
Shriti Sadhu
🌐 GitHub
