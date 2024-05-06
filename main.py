import os
import praw
import psycopg2
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

def load_env_variables():
    global client_id, client_secret, user_agent, username, password
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")

    global db_name, db_user, db_pass, db_host, db_port
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

def get_comment_data(reddit_client):
    comment_data = []
    for comment in reddit_client.user.me().comments.new(limit=100):
        comment.refresh()
        comment_data.append({
            "id": comment.id,
            "created_at": datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "body": comment.body,
            "score": comment.score,
            "replies": len(comment.replies),
            "url": comment.permalink
        })
    return comment_data

def get_submission_data(reddit_client):
    submission_data = []
    for submission in reddit_client.user.me().submissions.new(limit=100):
        submission_data.append({
            "id": submission.id,
            "created_at": datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "title": submission.title,
            "score": submission.score,
            "comments": submission.num_comments,
            "subreddit": submission.subreddit.display_name,
            "url": submission.url
        })
    return submission_data

def get_karma_data(reddit_client):
    karma_data = []
    karma = reddit_client.user.karma()
    for subreddit, karma_details in karma.items():
        karma_data.append({
            "id": today + "_" + subreddit.id,
            "date": today,
            "subreddit": subreddit.display_name,
            "comment_karma": karma_details['comment_karma'],
            "link_karma": karma_details['link_karma']
        })
    return karma_data

def save_to_database(items, table_name, on_conflict):
    cursor = conn.cursor()

    for item in items:
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['%s'] * len(item))
        values = tuple(item.values())
        conflict_clause = ', '.join([f"{key} = EXCLUDED.{key}" for key in item.keys()])

        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON CONFLICT ({on_conflict})
            DO UPDATE SET
            {', '.join([f"{key} = EXCLUDED.{key}" for key in item.keys()])};
        """
        cursor.execute(query, values)

    conn.commit()
    cursor.close()

def log_cron_execution(conn, job_name, status, error_message=None):
    query = """
        INSERT INTO cron_job_log (
            job_name, 
            status, 
            error_message
        )
        VALUES (%s, %s, %s)
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (job_name, status, error_message))
        conn.commit()

def main():

    reddit_client = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password
    )
    comment_data = get_comment_data(reddit_client)
    submission_data = get_submission_data(reddit_client)
    karma_data = get_karma_data(reddit_client)

    save_to_database(comment_data, "reddit_comment_insights", "id")
    save_to_database(submission_data, "reddit_submission_insights", "id")
    save_to_database(karma_data, "reddit_karma_insights", "id")

if __name__ == "__main__":
    load_env_variables()
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port
    )
    try:
        main()
        log_cron_execution(conn, "RedditMonitor", True)
    except Exception as e:
        conn.rollback()
        log_cron_execution(conn, "RedditMonitor", False, str(e))
    finally:
        conn.close()
