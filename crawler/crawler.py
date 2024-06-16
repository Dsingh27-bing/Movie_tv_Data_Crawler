import requests
import pprint
import time
import psycopg2
import random,sys

from datetime import datetime

# sys.stdout = open('/dev/null', 'w')
# sys.stderr = open('/dev/null', 'w')

# Reddit API credentials
client_id = "v-L_Un0PpdtiVZ6Eu30Sxw"
client_secret = "MEJIdGSeeqVdJlZcyBvi60W9CTcCuA"
user_agent = "Reddit_Project_API/0.0.1 by /u/CS515SMDP"
username = "CS515SMDP"
password = "DDJJR@2108"

# data member definitions
all_movies_titles={}
all_tv_titles={}
sorted_movies = {}
sorted_tv = {}
def get_reddit_token(client_id, client_secret, username, password):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": user_agent}

    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    if res.status_code == 200:
        token = res.json().get("access_token")
        return token
    else:
        print("Failed to authenticate. Status code:", res.status_code)
        print("Error response:", res.json())
        return None



def filter_posts(top_posts, i):
    # check if top_posts is a list or dictionary, if dictionary, run below code

    if isinstance(top_posts, dict):
        # print("top_posts is a dictionary")
        filtered_posts = [ 
                    post["data"]
                    for post in top_posts["data"]["children"]
        ]
        for post in filtered_posts:
            post["data"]["source_name"] = i  

    elif isinstance(top_posts, list):
        # print("top_posts is a list")
        filtered_posts = [
           post
           for post in top_posts
        ]
        for post in filtered_posts:
            post['data']['source_name'] = i
    return filtered_posts


def cleanup_posts(posts):
    cleaned_posts = {}
    for i in posts:
        for post in i:
            title = post["data"]["title"]
            source_name = post["data"]["source_name"]  
            cleaned_post = [post["data"]["id"],source_name,post["data"]["score"],post["data"]["subreddit"],datetime.fromtimestamp(post["data"]["created_utc"]),post["data"]["url"]]
            cleaned_posts[title] = cleaned_post
    return cleaned_posts

def get_reddit_posts_paginated_per_media(subreddit, token, max_requests, name):
    token = get_reddit_token(client_id, client_secret, username, password)
    all_posts = []

    if token:
        headers = {"User-Agent": user_agent, "Authorization": f"Bearer {token}"}
        params = {
            "limit": 100,  # The maximum limit as per Reddit API is 100
            "sort": "new",  # Sort by new posts
            "q":f"{name}",
            "restrict_sr":"on",
            "flair":"reviews"
        }

        after =  None # Initialize 'after' parameter for pagination
        requests_made = 0  # Keep track of the number of requests made

        while requests_made < max_requests:
            if after:
                params["after"] = after
           
            response = requests.get(
                f"https://oauth.reddit.com/r/{subreddit}/search",
                headers=headers,
                params=params,
            )

            if response.status_code == 200:
                top_posts = response.json()
                all_posts.extend(top_posts["data"]["children"])

                after = top_posts["data"].get(
                    "after"
                )  # Update 'after' for the next iteration
                if not after:
                    break  # Exit loop if there are no more posts to fetch

            else:
                print("Failed to retrieve posts. Status code:", response.status_code)
                print("Error response:", response.json())
                break  # Exit loop if request fails

            requests_made += 1

    return all_posts
def write_filtered_posts(filtered_posts):
    current_score = 0
    with open("filtered_posts.txt", "w+") as f:
        for post in filtered_posts:

            current_score += float(post["data"]["score"])
            f.write(
                "ID:" + post["data"]["id"] + "\n" +
                "Name:" + post["data"]["source_name"] + "\n" +
                
                "Title: "
                + post["data"]["title"]
                + "\n"
                + "Score (Upvotes): "
                + str(post["data"]["score"])
                + "\n"
                + "subreddit: "
                + str(post["data"]["subreddit"])
                + "\n"
                + "Created: "
                + str(datetime.fromtimestamp(post["data"]["created_utc"]))
                + "\n"
                + "Link: "
                + post["data"]["url"]
                + "\n\n"
            )
    # print(current_score)
    return current_score

def tmdb_result(query):
    url = f"https://api.themoviedb.org/3/discover/{query}?sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMWY1M2M2ZjlhYTFmMGNiM2I4MThhOTgxMDVkNzhmYyIsInN1YiI6IjY1MzlhMmY5MjgxMWExMDE0ZDYwYjU2OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.B6ceBwcKNx9wuLirTEsLLVzUmeddPFKdgQMIUVT7ses"
    }
    parameters= {
        'adult': 'true',
        'video': 'true',
        'language': 'en-US',
        'primary_release_year':'2013',
        'primary_release_date.gte':'2013-01-01',
        'primary_release_date.lte':'2023-12-31',
        'region':'US',
        'with_original_language':'en'
    }
    
    title_type = 'name'
    filename = 'tmdb_tv_output'
    if (query=='movie'):
        title_type='title'
        filename = 'tmdb_movie_output'

    page = 1
    with open(f'{filename}.txt', 'w+') as f:
        while page <= 10: 
            parameters['page']= page
            response = requests.get(url, headers=headers,params=parameters)
        
            if response.status_code ==  200:
                top_posts = response.json()
                for post in top_posts['results']:
                    title = post[f'{title_type}']
                    f.write("Title: " + title + "\n")
                    popularity = post['popularity']
                    if query == 'movie':
                        all_movies_titles[title] = popularity
                    else:
                        all_tv_titles[title] = popularity
                    f.write("Popularity: " + str(popularity) + "\n")
                page +=1
            else:
                print("Failed to retrieve top posts. Status code:", response.status_code)
                print("Error response:", response.json())
                break



time_start = time.time()
time_end = time.time()
print(f"Finished crawling TMDB for movies and TV within {time_end-time_start}\n\n")

def reddit_crawler(media):
    token = get_reddit_token(client_id, client_secret, username, password)
    count =0
    final_filtered = []
    time_start = time.time()
    print(f"starting {media} now ...... {len(all_movies_titles.keys())}\n")

    dict_variable = globals()[f"all_{media}_titles"]
    if media == 'tv':
        media = 'television'
    
    
    for i in dict_variable.keys():
        new_posts = get_reddit_posts_paginated_per_media(f"{media}", token, max_requests=10, name=f"{i}")
        filtered_posts = filter_posts(new_posts, i)
        final_filtered.append(filtered_posts)
        dict_variable[i] += write_filtered_posts(filtered_posts)
        progress = (count + 1) / len(dict_variable.keys())
        bar_length = int(40 * progress)
        progress_bar = "[" + "=" * bar_length + " " * (40 - bar_length) + "]"
        print(f"{progress_bar} {int(progress * 100)}% complete", end="\r")
        count += 1

    print()
    time_end = time.time()
    print(f"\t {time_end-time_start}\n")
    return final_filtered,dict_variable


# Define the connect_to_postgresql function
def connect_to_postgresql():
    try:
     
        connection = psycopg2.connect("dbname=crawler user=postgres")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

# Define the insert_data_into_postgresql function
def insert_data_into_postgresql(connection, table_name,data_to_insert):
    if connection is not None:
        try:
            cursor = connection.cursor()
            if table_name == 'REDDIT_MOVIES' or table_name == 'REDDIT_TV':
                query_create = f"CREATE TABLE IF NOT EXISTS {table_name} (\
                    POST_ID VARCHAR PRIMARY KEY,     \
                    NAME VARCHAR, \
                    TITLE VARCHAR, \
                    SCORE FLOAT, \
                    SUBREDDIT VARCHAR, \
                    CREATED DATE, \
                    LINK VARCHAR \
                );"
                cursor.execute(query_create)
                for key, value in data_to_insert.items():
                    cursor.execute(
                        'INSERT INTO {} (POST_ID, NAME,TITLE, SCORE, SUBREDDIT, CREATED, LINK) VALUES (%s, %s,%s, %s, %s, %s, %s) ON CONFLICT (POST_ID) DO NOTHING'.format(table_name),
                        (value[0], value[1], key,float(value[2]), value[3], value[4],value[5])
                    )

            else:
                query_create = f"CREATE TABLE IF NOT EXISTS {table_name} (\
                    TITLE VARCHAR, \
                    POPULARITY FLOAT \
                );"
                cursor.execute(query_create)
                for key,value in data_to_insert.items():
                    cursor.execute('INSERT INTO {}(TITLE, POPULARITY) VALUES (%s, %s)'.format(table_name), (key, float(value)))
            
            connection.commit()
            print("Data inserted into PostgreSQL successfully")
            
        except (Exception, psycopg2.Error) as error:
            connection.rollback()
            print("Error while inserting data into PostgreSQL:", error)
        finally:
            cursor.close()
    else:
        print("Connection to PostgreSQL failed. Data not inserted.")


connection = connect_to_postgresql()

# Call the insert_data_into_postgresql function for movies and TV data
if connection is not None:
    output= tmdb_result('movie')
    output_tv = tmdb_result('tv')
    

    insert_data_into_postgresql(connection, "TMDB_MOVIES", all_movies_titles)
    insert_data_into_postgresql(connection, "TMDB_TV", all_tv_titles)

    unclean_reddit_posts,sorted_dict = reddit_crawler("movies")
    reddit_posts = cleanup_posts(unclean_reddit_posts)
    insert_data_into_postgresql(connection, "REDDIT_MOVIES", reddit_posts)

    sorted_movies = dict(sorted(sorted_dict.items(), key=lambda item: item[1], reverse=True))
    time.sleep(60)
    unclean_reddit_posts,sorted_dict = reddit_crawler("tv")
    reddit_posts = cleanup_posts(unclean_reddit_posts)
    insert_data_into_postgresql(connection, "REDDIT_TV", reddit_posts)
    sorted_tv = dict(sorted(sorted_dict.items(), key=lambda item:item[1], reverse= True))

    insert_data_into_postgresql(connection, "MOVIES_POPULARITY", sorted_movies)
    insert_data_into_postgresql(connection, "TV_POPULARITY", sorted_tv)

    all_movies_titles = {}
    all_tv_titles = {}

    
# Close the PostgreSQL connection
if connection is not None:
    connection.close()
    print("PostgreSQL connection is closed")
