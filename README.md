![Descripción de la imagen](https://i.imgur.com/bYW6pai.jpg)
# Installation Guide for DarkGPT Project

DarkGPT is an artificial intelligence assistant based on GPT-4-200K designed to perform queries on leaked databases. This guide will help you set up and run the project on your local environment.

## Prerequisites

Before starting, make sure you have Python installed on your system. This project has been tested with Python 3.8 and higher versions.

## Environment Setup

1. **Clone the Repository**

   First, you need to clone the GitHub repository to your local machine. You can do this by executing the following command in your terminal:

  git clone https://github.com/luijait/DarkGPT.git 
  cd DarkGPT

2. **Configure Environment Variables**

   You will need to set up some environment variables for the script to work correctly. Copy the `.env.example` file to a new file named `.env`:

   DEHASHED_API_KEY="your_dehashed_api_key_here"
   DEHASHED_USERNAME="your_dehashed_username"
   OPENAI_API_KEY="API_KEY from openai.com"
4. **Install Dependencies**

   This project requires certain Python packages to run. Install them by running the following command:

   pip install -r requirements.txt
5. Then Run the project:
   python3 main.py
