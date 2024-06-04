# Hire Me Now API 🚀

Hire Me Now API is a FastAPI application that generates a persuasive 'Why You Should Hire Me' summary for GitHub users. It fetches repository information and files from GitHub, and uses the OpenAI API to create a summary highlighting the user's strengths, skills, and achievements. Aimed at job-seekers, this application can be used to create a compelling hiring statement for potential employers.

## Features 📋

- Fetches repository information and files from GitHub 📚
- Uses OpenAI API to generate a hiring statement 🤖
- Highlights the user's strengths, skills, and achievements 🏆

## Setup and Installation 🛠️

1. Clone the repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Set up your environment variables in a `.env` file. You will need a GitHub token and an OpenAI API key.
4. Run the application with `python main.py`.

## Usage 💻

Send a POST request to the `/hire_me_now_summary/` endpoint with the URL of the GitHub repository you want to generate a hiring statement for.

## Built With 🛠️

- [FastAPI](https://fastapi.tiangolo.com/)
- [GitHub API](https://docs.github.com/en/rest)
- [OpenAI API](https://beta.openai.com/docs/)

## Version 📌

0.1.0

## Author 👤

Bryan Antoine
