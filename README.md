# Deployment Guide for Dockerized BOT on Heroku

## Introduction
This guide provides detailed steps for building Docker image for your applications and deploying Dockerized applications to Heroku. It covers everything from setting up Heroku CLI to monitoring the deployed application.

## Prerequisites
Before you start, ensure you have:
- A **Heroku account**. Sign up [here](https://signup.heroku.com/).
- **Heroku CLI** installed. [Installation instructions](https://devcenter.heroku.com/articles/heroku-cli).
- **Docker** installed on your machine. [Download Docker](https://docs.docker.com/get-docker/).

## Deployment Process

Before building the docker image make sure your project is donne and runs properly on you locale machine.

If you have an working openai_API key, you can Fork this project and run a quick test. You can proceed to build the docker image directly after forking the code source

```bash
git clone https://github.com/Tijame98/Bot_niceGUI.git
```

The next step would be to reorginazed your project (create requirements.txt, the Procfile, .env file for example) 

### Step 1: Building Docker Image For the Project

Go to your project directory and create a Dockerfile (for example file.dockerfile) in wish you need to specifie what command should be run within your code source for your application.
For example in this example my dockerfile was as following :

```bash
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Run app.py when the container launches
CMD ["python", "main.py"]

```

Then you can run the command below to build the docker image
```bash
sudo docker build -t image_name -f file.dockerfile .

```
Test your dockerized application by running the command below

```bash
sudo docker run image_name
```

### Step 2: Heroku CLI and Container Registry Login

You need to run the commands below in your terminal to log in to Heroku and the Heroku Container Registry

```bash
sudo heroku login
sudo heroku container:login
```

These commands log you into the Heroku CLI and Heroku Container Registry, necessary for pushing and releasing Docker containers.

### Step 3: Create a New Heroku Application


```bash
sudo heroku create app_name
```

This command will output the URL and repository for your new Heroku app, like so:

- **Expected Output**

```bash
Creating app... done, ⬢ your-app-name
https://your-app-name.herokuapp.com/ | https://git.heroku.com/your-app-name.git
```

### step 4: Tag Your Docker Image

Replace "your-local-image-name" with your actual local Docker image name

image_name = "your-local-image-name"
app_name = "your-app-name"  

Replace with the name provided by the `heroku create` command

```bash
sudo docker tag image_name registry.heroku.com/app_name/web
```

### step 5: Push the Docker Image to Heroku

```bash
sudo docker push registry.heroku.com/app_name/web
```

### step 6: Release the Image on Heroku

```bash
sudo heroku container:release web -a app_name
```
### step 7: Open Your Deployed Application

```bash
sudo heroku open -a app_name
```

### Check Logs

```bash
sudo heroku logs --tail -a app_name
```
You can check my results. There is the link for my [Sales Bot](https://moosach-b33cdda8a16a.herokuapp.com/)
