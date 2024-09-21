![Descripción de la imagen](https://i.imgur.com/bYW6pai.jpg)
# Installation Guide for the DarkGPT Project

Welcome to DarkGPT! DarkGPT is your friendly artificial intelligence assistant powered by GPT-4-200K, specially designed to help you perform insightful queries on leaked databases. Whether you're setting it up for personal use or within a team, this guide will walk you through the steps to get DarkGPT up and running on your local machine.

## Prerequisites

Before we dive in, ensure you have the following:

- **Python Installed**: Make sure Python 3.8 or a newer version is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

## Environment Setup

Let's set up your development environment step by step.

### 1. Clone the Repository

First, you'll need to copy the DarkGPT repository to your local machine. Open your terminal and run:

```shell
git clone https://github.com/luijait/DarkGPT.git
cd DarkGPT
```

### 2. Set Up a Virtual Environment

Creating a virtual environment helps manage dependencies and keeps your project isolated. Here's how to set it up:

- **Create the Virtual Environment**

  ```shell
  python3 -m venv venv
  ```

- **Activate the Virtual Environment**

  - On **Windows**:

    ```shell
    venv\Scripts\activate
    ```

  - On **macOS and Linux**:

    ```shell
    source venv/bin/activate
    ```

  Once activated, your terminal prompt will change to indicate that you're working inside the virtual environment.

### 3. Configure Environment Variables

DarkGPT requires certain environment variables to function correctly. Follow these steps:

1. **Copy the Example Configuration**

   ```shell
   cp .example.env .env
   ```

2. **Edit the `.env` File**

   Open the `.env` file in your favorite text editor and fill in your credentials:

   ```env
   DEHASHED_API_KEY="your_dehashed_api_key_here"
   DEHASHED_USERNAME="your_dehashed_username"
   OPENAI_API_KEY="your_openai_api_key_here"
   GPT_MODEL_NAME="gpt-4o-mini"
   ```

   - **DeHashed API Key**: Instructions to obtain your DeHashed API key are provided below.
   - **OpenAI API Key**: Instructions to obtain your OpenAI API key are provided below.

### 4. Install Dependencies

With your virtual environment activated and environment variables configured, install the necessary Python packages:

```shell
pip install -r requirements.txt
```

### 5. Run the Project

Everything is set! Start DarkGPT by running:

```shell
python3 main.py
```

## Obtaining API Keys

### DeHashed API Key

1. **Sign Up or Log In**: Visit the [DeHashed website](https://www.dehashed.com/). If you don't have an account, sign up. Otherwise, log in.

2. **Subscribe to a Plan**: DeHashed offers various subscription plans. Choose one that suits your needs and complete the subscription process.

3. **Retrieve Your API Key**: After subscribing, navigate to your account settings or dashboard to find your API key under the "API" section. If you encounter any issues, refer to DeHashed's support or documentation.

4. **Keep It Secure**: Your API key grants access to your DeHashed account. **Never share it publicly** or expose it in any public code repositories.

### OpenAI API Key

1. **Sign Up or Log In**: Go to the [OpenAI website](https://openai.com/) and create an account or log in if you already have one.

2. **Access the API Key**: Once logged in, navigate to your account dashboard and find the section for API keys or developer settings to obtain your key.

3. **Understand Usage and Billing**: Familiarize yourself with OpenAI's usage limits and billing policies to manage costs effectively. Monitor your API usage regularly to avoid unexpected charges.

4. **Maintain Security**: Just like your DeHashed API key, **keep your OpenAI API key confidential**. Do not expose it in public repositories or share it with unauthorized individuals.

## General Tips for Managing API Keys

- **Use Environment Variables**: Storing API keys in environment variables enhances security and flexibility. Avoid hard-coding them into your scripts.

- **Update `.gitignore`**: Ensure that your `.env` file is listed in your `.gitignore` to prevent accidental uploads to public repositories.

- **Consult Official Documentation**: Always refer to the official documentation of the API providers for the most accurate and up-to-date instructions on managing your keys.

By following this guide, you'll have DarkGPT set up securely and efficiently, ready to assist you in your OSINT and information gathering endeavors!
