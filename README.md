# Local Setup Guide for Feedback Popup Form

## Setting up the Backend Locally

This Section provides a comprehensive guide to setting up and running the Feedback API locally. The API is built with FastAPI, SQLAlchemy, and utilizes an asynchronous database connection for improved performance using PostgreSQL as its database.

### 1. PostgreSQL Database Setup

1. **Install PostgreSQL:** 
    - Download the appropriate installer for your operating system from the official PostgreSQL website ([https://www.postgresql.org/download/](https://www.postgresql.org/download/)).
    - Follow the installation instructions provided.

2. **Access PostgreSQL Shell (psql):**
    - Open your terminal or command prompt.
    - Type `psql -U postgres` and enter the password you set during installation (default is usually blank).

3. **Create a Database:**
    - Once in the `psql` shell, execute the following command to create a new database for your API:
    
     ```sql
     CREATE DATABASE feedback_db;
     ```

4. **Create a Database User (Optional but Recommended):**
    - It's good practice to create a dedicated user for your API to interact with the database:

     ```sql
     CREATE USER feedback_user WITH PASSWORD 'your_password';
     ```
     **Replace `'your_password'` with a strong password.**

5. **Grant Privileges:**
    - Grant the necessary privileges to the newly created user for the `feedback_db` database:

     ```sql
     GRANT ALL PRIVILEGES ON DATABASE feedback_db TO feedback_user;
     ```

6. **Connect to the Database:**
    - You can now connect to the database using the new user:

     ```sql
     \c feedback_db feedback_user
     ```
     You will be prompted for the password you set for `feedback_user`.

### 2. Project Setup

#### 2.1. `.env`

- This file stores your environment variables, specifically the database connection URL. 
- Create a `.env` file in the root directory of your project and add the following:

```
DATABASE_URL="postgresql+asyncpg://feedback_user:your_password@localhost:5432/feedback_db"
```

**Replace `'your_password'` with the actual password set for `feedback_user`.**

#### 2.2. `db.py`

- Responsible for configuring the database connection.
- Utilizes `create_async_engine` from SQLAlchemy to establish an asynchronous connection to the database specified in the `DATABASE_URL` environment variable.
- Defines a base class `Base` that other SQLAlchemy models will inherit from.

#### 2.3. `models.py`

- Defines the database table structure using SQLAlchemy's ORM.
- In this case, it defines a single table named "feedback" with the following columns:
    - `id`: Primary key, auto-incrementing integer.
    - `rating`: Integer representing the feedback rating.
    - `satisfaction`: String representing the satisfaction level, derived from the rating.
    - `description`: Text field for optional feedback description.
    - `created_at`: Timestamp indicating when the feedback was created.

#### 2.4. `schemas.py`

- Defines Pydantic models for data validation.
- Two schemas are defined:
    - `FeedbackModel`: Represents the structure of feedback data returned by the API.
    - `FeedbackCreateModel`: Used for validating data sent in requests to create new feedback entries.

#### 2.5. `crud.py`

- Contains functions for performing CRUD (Create, Read, Update, Delete) operations on the `Feedback` model in the database.
- Each function utilizes asynchronous SQLAlchemy sessions for efficient database interactions.

#### 2.6. `create_db.py`

- A script to create the database tables defined in `models.py`.
- Connects to the database and executes `Base.metadata.create_all()`, which generates tables based on the defined models.

#### 2.7. `main.py`

- The heart of your FastAPI application.
- Initializes a FastAPI app instance.
- Sets up CORS (Cross-Origin Resource Sharing) to allow requests from your frontend (replace `http://localhost:8080` with your frontend URL).
- Defines API endpoints for:
    - Retrieving all feedback entries (`GET /feedback`)
    - Creating a new feedback entry (`POST /feedback`)
    - Retrieving feedback by ID (`GET /feedback/{feedback_id}`)
    - Deleting feedback by ID (`DELETE /feedback/{feedback_id}`)
    - Updating feedback by ID (`PUT /feedback/{feedback_id}`)


### 3. Install Dependencies & Run

1. **Install Dependencies:**
   - Ensure you have Python and pip installed.
   - Install the required Python packages:

     ```bash
     pip install fastapi uvicorn sqlalchemy pydantic python-dotenv asyncpg
     ```

2. **Create Tables:**
   - Run the `create_db.py` script to create the necessary tables:

     ```bash
     python create_db.py
     ```

3. **Run the Application:**
   - Start the FastAPI development server:

     ```bash
     uvicorn main:app --reload
     ```

   - This will start the server, usually at `http://127.0.0.1:8000`. The `--reload` flag enables automatic server restart on file changes.

4. **Access API Documentation:**
   - Once the server is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs` (or your specified port).
 
## Setting Up the Vue 2 Feedback Popup Frontend Locally

This guide outlines the steps to set up the Vue 2 Feedback Popup frontend locally, based on the repository you provided: [https://github.com/nrzngr/feedback-popup/tree/master/frontend](https://github.com/nrzngr/feedback-popup/tree/master/frontend). This guide assumes you already have a backend API set up and running.

### 1. Prerequisites

Make sure you have the following software installed on your system:

- **Node.js and npm:** Download and install from [https://nodejs.org/](https://nodejs.org/). Choose the LTS version for best compatibility.
- **Git (Optional):** If you prefer to clone the repository instead of downloading it manually, install Git from [https://git-scm.com/](https://git-scm.com/).

### 2. Download the Project

You can either clone the repository or download it as a ZIP file:

**Using Git (Recommended):**

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to save the project.
3. Run the following command:

    ```bash
    git clone https://github.com/nrzngr/feedback-popup.git
    cd feedback-popup/frontend
    ```

**Download ZIP:**

1. Go to the repository link: [https://github.com/nrzngr/feedback-popup/tree/master/frontend](https://github.com/nrzngr/feedback-popup/tree/master/frontend)
2. Click the green "Code" button.
3. Select "Download ZIP."
4. Extract the downloaded ZIP file to your desired location.
5. Navigate to the extracted `frontend` directory using your terminal or command prompt.

### 3. Install Dependencies

1. In your terminal, navigate to the `frontend` directory of the project.
2. Run the following command to install the project dependencies:

    ```bash
    npm install
    ```
    This will download and install all necessary packages listed in the `package.json` file.

### 4. Running the Application

Once you've installed dependencies, you can run the application using the following command in your terminal:

```bash
npm run serve
```

This will start the development server, usually at `http://localhost:8080`. Open this URL in your web browser to see the application running. Make sure your backend API is running and the frontend can communicate with it.

### 5. Building for Production

When you're ready to deploy the application, run the following command:

```bash
npm run build
```

This will create a `dist` directory in your project folder. This directory contains a production-ready build of your application, optimized for deployment to a web server.

