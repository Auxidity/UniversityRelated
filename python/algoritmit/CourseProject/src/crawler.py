"""
File : crawler.py
Author : Daniel Kortesmaa
Description : Reddit webcrawler using their API surface creating raw data json dumps
"""

#Currently using only one subreddit to fetch data from. Ideally we for loop through a list of subreddits and create raw data for each. Keeping it simple for simplicity to inspect functionality.

import praw
import json
import os, datetime

# user_agent_variable = REDACTED
# client_secret_variable = REDACTED
# client_id_variable = REDACTED


reddit = praw.Reddit(client_id = client_id_variable,
                     client_secret = client_secret_variable,
                     user_agent = user_agent_variable)

def crawl_subreddit(subreddit_name, num_posts):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    # Iterate through posts
    for post in subreddit.new(limit=num_posts):
        post_data = {
            'title': post.title,
            'author': post.author.name if post.author else '[deleted]',
            'created_utc': post.created_utc,
            'url': post.url,
            'score': post.score,  # Add the score of the post. Can be used to fine tune what is used.
            'comments': []
        }

        # Fetch comments for the post
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comment_data = {
                'comment_id': comment.id, #Used to form conversation pairs.
                'parent_id': comment.parent_id.split('_')[1] if comment.parent_id.startswith('t1_') else None, #Used to form parent-child conversation pairs. If no parent_id, use post as parent.
                'author': comment.author.name if comment.author else '[deleted]', 
                'body': comment.body, #The meat
                'created_utc': comment.created_utc, #Creation date of the message.
                'upvotes': comment.ups, #Doesn't work as intended, but has an actual use. This shows 'karma', not the actual count of upvotes. Will be used for comment filtering.
                'downvotes': comment.downs #Doesn't work. At all. Entirely useless. Only there in case it does ever get fixed.
            }

            post_data['comments'].append(comment_data)

        posts_data.append(post_data)

    return posts_data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
def generate_filename(subreddit_name):
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    filename = f"{current_date}_{subreddit_name}_data.json"
    return filename


if __name__ == '__main__':
    # Get the parent directory of the script's directory
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # Define the path to the data directory relative to the parent directory
    data_dir = os.path.join(parent_dir, 'data/raw')

    # Ensure the data directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


    subreddit_name = 'Science'
    num_posts = 10
    output_file = os.path.join(data_dir, generate_filename(subreddit_name))

    subreddit_data = crawl_subreddit(subreddit_name, num_posts)
    save_to_json(subreddit_data, output_file)
