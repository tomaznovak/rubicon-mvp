# Rubicon

### Description

This is the source code for Rubicon - AI agent. The agent itself is capable of searching for scientific papers on [[https://arxiv.org/]], downloading them and extracting the main points and explanation of the research. The whole agent is developed in agency-swarm framework developed by Arsenii Shatokhin [[https://github.com/VRSEN/agency-swarm]].

Agent is in my daily included in my daily workflow as i use it for writing scripts for my short form podcast ( generated by NotebookLM), which I download daily on my YT chanel. This is the first part of my automation that process.


This version is runnable on the google cloud with database integrated.


### Quick Start

After you clone the reposotory create .env files with next environment variables in it:

- OPENAI_API_KEY, DATABASE_HOSTNAME, DATABASE_PORT, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_USERNAME, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

Next, configure the gcloud on which you are going to run it.
