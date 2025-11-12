# **Now Listening – A Flask Music Blog**

Now Listening is a **full-stack music blogging platform** that lets users share their favorite albums, post reviews, and rate them on a 1–5 star scale. Inspired by Letterboxd (an app for reviewing movies), Now Listening lets you explore and discuss music with the world!
It’s built with **Flask**, **Bootstrap**, and **PostgreSQL**, and deployed using **Docker** and **Render**.  

👉 **Live site:** [*[Check it Out!](https://now-listening.onrender.com/about)*]

---

## **Overview**

Now Listening provides a simple but elegant way for music lovers to:

- ✏️ **Create posts** to share albums they’re currently listening to  
- ⭐ **Rate albums** and view average ratings from other users  
- 👤 **Register, log in, and manage profiles** with Flask-Login  
- 🧾 **Browse all posts** on the homepage, even without an account  

Users can search, read, and explore community posts to discover new music — all in a clean, responsive interface powered by Flask and Bootstrap.

---

## **Tech Stack**

| Layer | Technology |
|-------|-------------|
| **Backend** | Flask (Python), SQLAlchemy ORM |
| **Frontend** | HTML, CSS, Bootstrap 5 |
| **Database** | PostgreSQL (via SQLAlchemy) |
| **Deployment** | Docker + Render |
| **Authentication** | Flask-Login & Flask-Bcrypt |
| **Email / Reset** | Flask-Mail (optional for password reset) |

---

## **Features**

- **Account Management** – Users can register, log in, and manage their account info  
- **Create & View Posts** – Share albums, artists, and thoughts with a star rating  
- **Average Album Ratings** – Displays average community ratings per album  
- **Responsive UI** – Built with Bootstrap 5 and fully mobile-friendly  
- **Database Persistence** – Uses PostgreSQL on Render for reliable cloud storage  

---

## **Deployment**

Now Listening is containerized using **Docker** and deployed via **Render**.  


<!-- 
> 💡 Since this project relies on environment variables (e.g. `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, etc.), the full Docker setup is **not necessary for recruiters to replicate** — it’s already live and running.  
> If you’re an engineer interested in setup details, see the `Dockerfile` for reference.

--- -->








<!-- 


## 🐳 Run Locally with Docker

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/now-listening.git
cd now-listening
```


### 2. Create a .env file

```bash
Copy the example environment file and fill in your own values:
cp .env.example .env
```

Then open .env and set your configuration:
```bash
# Flask secret key
SECRET_KEY=change-me

# Local database (SQLite)
SQLALCHEMY_DATABASE_URI=sqlite:///instance/site.db

# Or, if using PostgreSQL
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:password@host:5432/musicblog

# Flask-Mail
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_password
```

### 3. Build the Docker image
```bash
docker build -t musicblog .
```

This will install all dependencies and packages your Flask app into a Docker image.


### 4. Run the container
```bash
docker run -p 8000:8000 --env-file .env musicblog
```
 -->
