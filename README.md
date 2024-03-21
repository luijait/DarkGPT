![Descripción de la imagen](https://i.imgur.com/bYW6pai.jpg)
# Installation Guide for DarkGPT Project

DarkGPT is an artificial intelligence assistant based on GPT-4-200K designed to perform queries on leaked databases. This guide will help you set up and run the project on your local environment.

## Prerequisites

Before starting, make sure you have Python installed on your system. This project has been tested with Python 3.8 and higher versions.

## Environment Setup

1. **Clone the Repository**

   First, you need to clone the GitHub repository to your local machine. You can do this by executing the following command in your terminal:

```shell
git clone https://github.com/luijait/DarkGPT.git
```
```shell
cd DarkGPT
```

2. **Configure Environment Variables**

   You will need to set up some environment variables for the script to work correctly. Copy the `.example.env` file to a new file named `.env`:

```env
DEHASHED_API_KEY="your_dehashed_api_key_here"
DEHASHED_USERNAME="your_dehashed_username"
OPENAI_API_KEY="API_KEY from openai.com"
```
4. **Install Dependencies**

   This project requires certain Python packages to run. Install them by running the following command:

```shell
pip install -r requirements.txt
```
5. Then Run the project:
```shell
python3 main.py
```
DeHashed API Key
1. Sign Up or Log In: Visit the DeHashed website (https://www.dehashed.com/). If you don't already have an account, you'll need to sign up. If you do, just log in.
2. Subscription: DeHashed is a paid service, so you'll need to subscribe to one of their plans to get access to the API. Choose a plan that fits your needs and complete the subscription process.
3. Accessing the API Key: Once you've subscribed, you can usually find your API key in your account settings or dashboard. Look for a section labeled "API" or something similar. If you're having trouble finding it, DeHashed's support or documentation might be able to help.
4. Security: Keep your API key secure. Don't share it with others or expose it in public code repositories.

   
OpenAI API Key
1. Sign Up or Log In: Go to the OpenAI website (https://openai.com/). You'll need to create an account if you don't have one, or log in if you do.
3. Getting the API Key: Once you have been granted access, you can find your API key in your OpenAI account dashboard. There should be a section for API keys or developer settings.
4. Usage and Billing: Be aware of OpenAI's usage and billing policies. Depending on the volume of your requests and the specific models you use, you might incur charges. Plan accordingly and monitor your usage.
5. Security: As with any API key, it's crucial to keep your OpenAI key secure. Do not share it publicly or with anyone who should not have access to it.
General Tips for Managing API Keys:
Environment Variables: Store your API keys in environment variables rather than hard-coding them into your project. This makes your application more secure and flexible.
.gitignore: If you're using Git, ensure your .env file or any file containing API keys is listed in your .gitignore file to prevent it from being uploaded to a public repository.
Documentation: Always refer to the official documentation of the API provider for the most accurate and up-to-date information on obtaining and using API keys.
By following these steps and guidelines, you'll be able to obtain the necessary API keys to integrate DeHashed and OpenAI services into your projects.
