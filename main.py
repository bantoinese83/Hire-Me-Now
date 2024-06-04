import os
import uvicorn
from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel, HttpUrl
from github_fetcher import GitHubFetcher
from openai_generator import OpenAIGenerator
from dotenv import load_dotenv
from loguru import logger
from halo import Halo

load_dotenv()

app = FastAPI(
    title="Hire Me Now API",
    description=(
        "A FastAPI application for generating a 'Why You Should Hire Me' summary based on a GitHub repository."
        " It uses the OpenAI API to generate the summary."
        " The application fetches repository information from GitHub and all files in the repository,"
        " and then generates a hiring statement based on the repository details."
        "The hiring statement is designed to be persuasive and highlight the strengths, skills, and achievements of the"
        "repository owner."
        " The application is built using FastAPI, GitHub API, and OpenAI API."
        " The application is designed to be used by job seekers to create a compelling summary of their work and "
        "achievements on GitHub."
        "The hiring statement is generated using the OpenAI API, which uses the GPT-4 model to generate human-like "
        "text."
        " The application is designed to be easy to use and requires only a GitHub repository URL as input."
        "The application fetches the repository information from GitHub, including the owner, description, and number "
        "of"
        "stars, forks, and issues. It then generates a summary highlighting the key projects and contributions."
        " Aim for 3-5 well-documented, substantial projects that demonstrate your skills and expertise."
    ),
    version="0.1.0",
)

# Get API keys from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Instantiate the necessary parts
github_fetcher = GitHubFetcher(GITHUB_TOKEN)
openai_generator = OpenAIGenerator(OPENAI_API_KEY)

# Set up logging with loguru
logger.add("file.log")

# Set up spinner with halo
spinner = Halo(text="Loading", spinner="dots")


class RepoURL(BaseModel):
    url: HttpUrl


@app.post("/hire_me_now_summary/")
async def hire_me_now_summary(url: HttpUrl = Form(...)):
    repo_url = RepoURL(url=url)
    spinner.start()
    try:
        # Fetch repository info
        repo_info = github_fetcher.fetch_repository_info(repo_url.url)
        # Fetch all files in the repository
        repo_files = github_fetcher.fetch_all_files(repo_url.url)
    except Exception as e:
        spinner.fail()
        logger.error(f"Failed to fetch repository info: {e}")
        raise HTTPException(status_code=400, detail="Failed to fetch repository info")

    try:
        # Generate hiring statement
        github_username = repo_info["owner"]["login"]
        hiring_statement = openai_generator.generate_hiring_statement(
            repo_info, repo_files, github_username
        )
    except Exception as e:
        spinner.fail()
        logger.error(f"Failed to generate hiring statement: {e}")
        raise HTTPException(
            status_code=400, detail="Failed to generate hiring statement"
        )
    logger.info(f"Hiring statement: {hiring_statement}")
    spinner.succeed()

    return {"hiring_statement": hiring_statement}


# Startup events
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


# Shutdown events
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    logger.remove(0)


# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
