#!/bin/bash

# 1) Go to project folder
cd /Users/ashish/LinkedIn_Post || exit 1

# 2) Activate virtual environment
source .venv/bin/activate

# 3) Run the Python script that posts to LinkedIn
#    Output (print + errors) will be saved to cron_log.txt
python post_with_groq.py >> daily_post.log 2>&1