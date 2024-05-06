# Reddit Monitor

## Introduction
Reddit Monitor is a Python script designed to collect data from your Reddit account and store it in a PostgreSQL database. It retrieves information about your comments, submissions, and karma breakdown on Reddit.

## Features
- Collects data on your comments, submissions, and karma from Reddit.
- Stores the collected data in a PostgreSQL database.
- Logs the execution status of the script for monitoring purposes.

## Prerequisites
Before running the script, ensure you have the following:
- Python 3.x installed on your system.
- Required Python packages installed. You can install them using `pip install -r requirements.txt`.
- Access to a PostgreSQL database with necessary permissions to create tables and insert data.
- Reddit API credentials (client ID, client secret, user agent, username, and password).
- Environment variables set up for Reddit API credentials and database connection details.

## Installation
1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Set up environment variables for Reddit API credentials and database connection details.
4. Ensure your PostgreSQL database is running and accessible.

## Configuration
You can configure the script by modifying the following environment variables:
- `REDDIT_CLIENT_ID`: Your Reddit API client ID.
- `REDDIT_CLIENT_SECRET`: Your Reddit API client secret.
- `REDDIT_USER_AGENT`: Your Reddit API user agent.
- `REDDIT_USERNAME`: Your Reddit username.
- `REDDIT_PASSWORD`: Your Reddit password.
- `DB_NAME`: Name of the PostgreSQL database.
- `DB_USER`: PostgreSQL database username.
- `DB_PASS`: PostgreSQL database password.
- `DB_HOST`: PostgreSQL database host.
- `DB_PORT`: PostgreSQL database port.

## Database Schema
The script requires the following tables in your PostgreSQL database:
- `reddit_comment_insights`: Stores data about your Reddit comments.
- `reddit_submission_insights`: Stores data about your Reddit submissions.
- `reddit_karma_insights`: Stores data about your Reddit karma breakdown.

You can create the table using the following code

```sql
CREATE TABLE reddit_comment_insights (
    id VARCHAR(20) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE,
    body TEXT,
    score INT,
    replies INT,
    url TEXT
);

CREATE TABLE reddit_submission_insights (
    id VARCHAR(20) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE,
    title TEXT,
    score INT,
    comments INT,
    subreddit TEXT,
    url TEXT
);

CREATE TABLE reddit_karma_insights (
    id TEXT PRIMARY KEY,
    date DATE,
    subreddit TEXT,
    comment_karma INT,
    link_karma INT
);
```

## Usage
1. Navigate to the directory containing the script.
2. Run the script using the command `python main.py`.

## Logging
The script logs its execution status to a table named `cron_job_log` in your PostgreSQL database. It records the job name, status (success/failure), error message (if any), and error traceback (if any).
You can create the table using the following code

```sql
CREATE TABLE cron_job_log (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(255) NOT NULL,
    status BOOLEAN NOT NULL,
    error_message TEXT,
    error_traceback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting
If you encounter any issues while running the script, please check the following:
- Ensure all required environment variables are correctly set.
- Verify your Reddit API credentials and permissions.
- Check your PostgreSQL database connection details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
