
Team Members: 
- Dimple Singh
- Jay Balaram Sankhe 
- Debangana Ghosh
- Jeremy Anton 
- Ritika Sanjay Kale

**Introduction**: The core objective of our study is to gain insights into the ever-changing landscape of movie trends. We want to identify and understand what makes a movie popular at any given time. To achieve this, we focus on several key aspects such as what topics are currently trending, how audiences rate these movies, and the discussions and interactions happening on platforms like TMDb and Reddit. 

Our ultimate goal is to uncover the key factors that contribute to a movie's popularity. Our research findings are expected to reveal emerging patterns within the movie industry. They will also provide valuable insights into what audiences like and dislike, and how social media plays a crucial role in determining a movie's success in today's world. 

This exploration offers valuable insights for professionals in the film industry, filmmakers, and movie enthusiasts who want to better understand and navigate the ever-changing landscape of movie popularity trends. 

The Reddit and TMDB Data Crawler is a Python script developed for the purpose of collecting data from two prominent online platforms: Reddit and The Movie Database (TMDB). 

This script serves as a tool to extract vital information related to movies and television shows, including their levels of popularity, and relevant posts and discussions on Reddit. All the collected data is then stored neatly in a PostgreSQL database for later analysis.


--- 
### How to Run the code: 

Run the python file directly by creating python virtual environment(myenv) or run the bash script.

1. Create Virtual Environment using virtualenv package
```
virtualenv -p python3 env
```
2. Create postgres database and keep it open for connection
```
systemctl restart postgresql@16-main.service
```

3. Activate the virtual environment

```
 source env/bin/activate
```

4. Run the python script 
```
python3 crawler.py
```

_OPTIONAL_:   
5. You can automate the crawler using the shell scripts we have provided in `crawler_script.sh` and `test.sh`

```
bash test.sh
```

6. We have sent it to the background process to continuously collect data using the following command

```
nohup {HOME_FOLDER}/test.sh > results.out 2>&1 &
```
