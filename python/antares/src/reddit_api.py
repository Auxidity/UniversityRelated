"""
File     : reddit_api.py
Author   : Daniel Kortesmaa
Desc.    : Reddit Crawler using Reddit API to fetch either topics, posts or source links that are present in the messages. Current functionality is limited to printing if the posts have a reference material or not, and also
returning a link to the reddit post so that user can read it themselves. This will be a gui issue on how to handle the ui operations.
"""

"""
There is potential issue here where the user will ask for a topic, i.e. politics, and then when we search for politics, it will always be US politics due to how r/politics is focused on US politics.
Potential solution is to pass the argument to a chatgpt or another similliar generative llm to figure out what subreddit might contain what user could be interested in. Most likely we run this through AI one way or another
to simplify the process.

Something that needs a further investigation is to look if making the state machine makes sense in the mqtt_sub module, or make a separate file for the state machine, which then listens on mqtt for arguments for api calls such as 
this one (which will each be their own module). Some IPC is neccesary. It is perhaps easier to have a dedicated FSM, dedicated message handler. One potential solution is that FSM gives keywords as argument list based on
FSM state to the subscriber, and subscriber will then pass output as a string back to FSM. Handle keyword count etc. 


Another issue is that if we handle an array of keywords (which is more humanlike), passing arguments to this file can be annoying. Knowing whether or not to use accurate version or inaccurate version isn't difficu
"""


import praw
import prawcore
import json #For later when we pass it out. Reddit already returns in JSON, most likely we will also pass the JSON along. Uncertain if we build the state machine on flask, or skip flask and make the mqtt_sub a state machine aswell. 
import re
import sys

try: 
    with open('src/reddit.json') as f:
        config = json.load(f)
        user_agent_variable = config['user_agent']
        client_secret_variable = config['client_secret']
        client_id_variable = config['client_id']
except FileNotFoundError as e:
    print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
    sys.exit(2)

#Reddit API variables moved to reddit.json.

reddit = praw.Reddit(client_id = client_id_variable,
                     client_secret = client_secret_variable,
                     user_agent = user_agent_variable)


def crawl_subreddit(subreddit_names, num_posts):
    all_posts_data = []

    for subreddit_name in subreddit_names:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            subreddit.title
        except prawcore.exceptions.PrawcoreException as e:
            print(f"An error occurred while accessing subreddit {subreddit_name}: {e}")
            continue

        posts_data = []
        # Iterate through posts
        for post in subreddit.new(limit=num_posts):
            post_data = {
                'title': post.title,
                'author': post.author.name if post.author else '[deleted]',
                'created_utc': post.created_utc,
                'url': post.url,
                'permalink': "https://www.reddit.com" + post.permalink,  # Include permalink
                'score': post.score,  # Add the score of the post. Can be used to fine tune what is used.
                'comments': []
            }
            posts_data.append(post_data)

        all_posts_data.extend(posts_data)

    return all_posts_data

def search_keywords_in_posts(posts_data, keywords):
    if not posts_data:
        print("No posts found with the provided subreddit and search criteria.")
        return None
    

    matching_posts = []
    for post in posts_data:
        for keyword in keywords:
            if keyword.lower() in post['title'].lower():
                if post['url'] != post['permalink']:  # Compare reference URL and permalink
                    has_reference = True
                else:
                    has_reference = False
                matching_posts.append({
                    'title': post['title'],
                    'url': post['url'],
                    'permalink': post['permalink'],
                    'has_reference': has_reference
                })
                break  # If any keyword matches, break out of the loop to avoid duplicate posts

    if not matching_posts:
        print("No posts found matching the provided keyword.")
        return None
    
    return matching_posts

def search_exact_keywords_in_posts(posts_data, keywords):
    if not posts_data:
        print("No posts found with the provided subreddit.")
        return None

    matching_posts = []
    for post in posts_data:
        for keyword in keywords:
            keyword_pattern = r'\b{}\b'.format(re.escape(keyword))  # Construct regex pattern for each keyword
            if re.search(keyword_pattern, post['title'], flags=re.IGNORECASE):
                if post['url'] != post['permalink']:  # Compare reference URL and permalink
                    has_reference = True
                else:
                    has_reference = False
                matching_posts.append({
                    'title': post['title'],
                    'url': post['url'],
                    'permalink': post['permalink'],
                    'has_reference': has_reference
                })
                break  # If any keyword matches, break out of the loop to avoid duplicate posts

    if not matching_posts:
        print("No posts found matching the exact keywords.")
        return None

    return matching_posts


"""
The following is used to filter posts based on keyword match count, so if one title has 1 keyword match but another title has 2, it should print 2nd first. By default return the one with most matches, but if user is not happy
with that, provide rest as options. Potentially as GUI list?
"""
def count_keywords(title, keywords):
    count = 0
    for keyword in keywords:
        if keyword.lower() in title.lower():
            count += 1
    return count

def sort_by_keyword_count(posts, keywords):
    if posts is None:
        return #Nothing to be done
    posts.sort(key=lambda post: count_keywords(post['title'], keywords), reverse=True)



"""
The logic how to handle these calls needs further investigation.  All basic functionality should be above, and something that could be done is that if exact_keyword returns None, we do a looser search and return that instead.
Prompt the user so that they know about increased inaccuracy. We are currently printing all the important knowledge that would be returned and then handled based on FSM control. View the content? Or just read title out loud.
Another thing that can be considered is to also return comments, and read them out based on rating. Or perhaps ability to creating comments aswell? Also filtering the posts by score threshold. Though this might not be so great
in smaller subreddits.

Also potentially let the user define with physical input what they wish to search for (as an additional option instead of relying on speech recognition being able to. SR will struggle with abbreviations and names afterall).
Explore the possibility of running a parallel speech recognition thread with something slower but more accurate with names and such on functionality that requires it.
"""


"""
Extremely important : if the keyword is passed as a string, it "works" with "unwanted features". Change the code to expect a string (remove 'for keyword in keywords' & break), or stick to arrays. Arrays for multi keyword search. 
Same functionality on subreddits, so that we can multi search multiple subreddits at once (if deemed neccesary. )

Potentially use AI to create a concise list of keywords out of a spoken string. Reason to avoid this is potential AI hallucination and the delay that comes with AI requests.
Also use AI in cases where keyword search should be expanded upon multiple subreddits. Or if the user knows which subreddit to search from, then allow user to do that. Handle the argument creation in the FSM, pass it here and then
we return serialized json back, which then gets used however.
"""

def output(keywords, subreddit_names, num_posts):
    posts_data = crawl_subreddit(subreddit_names, num_posts)
    if posts_data is not None:
        matching_posts = search_keywords_in_posts(posts_data, keywords)
        sort_by_keyword_count(matching_posts, keywords)
        result = []
        if matching_posts is not None:
            for post in matching_posts:
                post_info = {
                    "Title              ": post['title'],
                    "Reference URL      ": post['url'],
                    "Reddit Permalink   ": post['permalink'],
                    "Has reference      ": post['has_reference']
                } 
                formatted_post = ""
                for key, value in post_info.items():
                    formatted_post += f"{key}:{value}\n"
                result.append(formatted_post)
        return result
    else:
        pass

if __name__ == "__main__":
    keyword = ["can", "confirmed", "is"]
    subreddit_name = ["science"]
    num_posts = 15
    print(output(keyword, subreddit_name, num_posts))

"""
#Example usage 1 has references, inaccurate: 
keyword = ["can", "confirmed", "is"]
subreddit_name = ["science", "politics"]
num_posts = 15
posts_data = crawl_subreddit(subreddit_name, num_posts)
matching_posts = search_keywords_in_posts(posts_data, keyword)
sort_by_keyword_count(matching_posts, keyword)


if matching_posts is not None:
    for post in matching_posts:
        print("Title            :",post['title'])
        print("Reference URL    :", post['url'])
        print("Reddit Permalink :", post['permalink'])
        print("Has reference    :",post['has_reference'])
        print()

print()
print()
print()
"""

"""
#Example usage 2 has references, accurate: 
keyword = ["kindness"]
subreddit_name = "science"
num_posts = 5
posts_data = crawl_subreddit(subreddit_name, num_posts)
matching_posts = search_exact_keywords_in_posts(posts_data, keyword)
if matching_posts is not None:
    for post in matching_posts:
        print("Title            :",post['title'])
        print("Reference URL    :", post['url'])
        print("Reddit Permalink :", post['permalink'])
        print("Has reference    :",post['has_reference'])
        print()
"""

"""
The following is commented out for now. But use something like this as skeleton for the logic.
Pass keywords as an array stringified, something like this. :

#def call_script(var1, var2, keyword_array):
#    keyword_array_string = ",".join(map(str, array))  # Convert array to string with comma delimiter
#    subprocess.run(["python", "script2.py", str(var1), str(var2), keyword_array_string])

Above is extremely simplified. Do not use that directly, its just for basic idea. Better idea is to serialize
to JSON and pass that as argument and then load it here.


if __name__ == "__main__":
    var1 = int(sys.argv[1])  # Convert the first argument to integer. Boolean to hold if we use exact or non-exact keyword searcher function
    var2 = sys.argv[2]  # Second argument as string. The subreddit to search
    keyword_array_as_str = sys.argv[3]  # keyword array

    keyword_array = list(map(int, array_str.split(',')))  # Parse the string back into array


    #Print them out or do something. Figure this out later. Probably something like if var1 == 0, search_keywords_in_posts(var2, keyword_array) else search_exact_keywords_in_posts(var2, keyword_array).
    #Then do something in the FSM with the shit. Most likely we need to serialize the data to JSON to be accessed in FSM. Easy solution is to do file I/O with it and access it in FSM. Look into other solutions.
    print("var1:", var1)
    print("var2:", var2)
    print("keyword_array:", keyword_array)
"""
