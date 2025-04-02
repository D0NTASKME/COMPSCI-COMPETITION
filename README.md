# Computer Science Competition Challenges Platform

Welcome to the repository for our cool cyber compsci competition platform! This project is all about learning and having fun with different kinds of security puzzles.

## What's Inside?

This repository contains all the code needed to run the platform, including:

* **`frontend`**: This folder holds the code for what you see in your web browser. It's built using Next.js and React.
* **`backend`**: This folder contains the code that runs on the server. It's built with FastAPI (a super speedy Python framework) and handles things like user accounts, challenges, and checking if your flags are correct!
* **`backend/database.py`**: This file sets up how our backend talks to the database.
* **`backend/models.py`**: This file defines the structure of the information we store (like users and challenges).
* **`backend/schemas.py`**: These files help us make sure the data we send around is in the right format.
* **`backend/crud.py`**: This file contains the code for creating, reading, updating, and deleting information in the database.
* **`backend/routes/`**: This folder has files that handle different parts of the website's functionality (like authentication and levels).
* **`main.py`**: This is the main file that starts up our backend server.
* **`README.md`**: That's this file you're reading right now! It tells you all about the project.
* **(Other configuration files)**: You might see some other files that help with setting up and running the project.

## How to Get Started (for Developers)

If you want to run this project on your own computer and maybe even help make it better, here's what you need to do:

1.  **Make sure you have these things installed:**
    * **Python** (version 3.8 or higher)
    * **pip** (Python package installer - usually comes with Python)
    * **Node.js** (version 16 or higher)
    * **npm** (Node.js package manager - usually comes with Node.js)
    * **A database** (like PostgreSQL). You'll need to set this up and have it running.

2.  **Get the code:**
    * Go to the main page of your repository on GitHub.
    * Click the green "Code" button.
    * You can either download the code as a ZIP file or use Git to "clone" the repository to your computer. If you know Git, cloning is usually better!

3.  **Set up the backend:**
    * Open your computer's terminal or command prompt.
    * Go into the `backend` folder: `cd backend`
    * Install all the necessary Python libraries: `pip install -r requirements.txt`
    * **Important!** You'll need to configure your backend to connect to your database. Look for a configuration file (like `.env` or inside `backend/config.py`) and put in your database details.
    * Run the database migrations (this sets up the tables in your database): You might have a command for this in your project, like `alembic upgrade head` (if you're using Alembic for migrations).
    * Start the backend server: `uvicorn main:app --reload`

4.  **Set up the frontend:**
    * Open a new terminal or command prompt.
    * Go into the `frontend` folder: `cd frontend`
    * Install all the necessary JavaScript packages: `npm install`
    * Start the frontend development server: `npm run dev`

5.  **Open the platform in your browser!** Usually, the frontend will be running at `http://localhost:3000`.

## Contributing

If you're interested in helping to make this platform even better, that's awesome! Here are a few ways you can contribute:

* **Report Bugs:** If you find something that's not working right, please let us know by creating an "issue" on GitHub.
* **Suggest New Features:** Have a cool idea for a new challenge type or a way to improve the platform? Open an "issue" and tell us about it!
* **Contribute Code:** If you're a coder and want to help fix bugs or add new features, you can "fork" this repository, make your changes, and then create a "pull request" to share your work.

## Have Fun!

This platform is all about learning and challenging yourself in a fun way. So, dive in, try out the challenges, and see what you can discover!

---
