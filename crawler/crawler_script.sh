#!/bin/bash
while true
do
    echo "starting"
    rm *_output.txt
    rm filtered_posts.txt
    rm *.csv
    source myenv/bin/activate
    # python3 crawler.py &
    python3 crawler.py
    deactivate
    echo "done crawling and inserting into db"
    echo -e "\n"  
    echo -e "\n"
    # Start psql and send SQL commands
    psql -U postgres <<EOF
    \c crawler
    select count(*) from tmdb_movies;
    select count(*) from tmdb_tv;
    SELECT 'Reddit Posts for movies:' AS category, COUNT(*) AS post_count FROM reddit_movies;
    SELECT 'Reddit Posts for tv:' AS category, COUNT(*) AS post_count FROM reddit_tv;
    select count(*) from movies_popularity;
    select count(*) from tv_popularity;
    \q
EOF
    psql -U postgres -d crawler -c "\copy movies_popularity TO '/home/rkale2/movies_popularity.csv' WITH CSV HEADER"
    psql -U postgres -d crawler -c "\copy tv_popularity TO '/home/rkale2/tv_popularity.csv' WITH CSV HEADER"
    break
done
