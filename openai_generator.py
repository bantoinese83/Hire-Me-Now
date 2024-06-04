import logging

from loguru import logger
from openai import OpenAI


class OpenAIGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def generate_hiring_statement(self, repo_info, repo_files, github_username):
        logging.info(f"Repo files: {repo_files}")

        prompt = self._create_prompt(repo_info, repo_files, github_username)
        response = self._get_response_from_openai(prompt)
        return self._extract_message_from_response(response)

    @staticmethod
    def _create_prompt(repo_info, repo_files, github_username):
        file_contents = "\n".join(repo_files.values())
        return (
            f"IDENTITY and PURPOSE\n"
            f"You will generate a 'Why You Should Hire Me' summary based on the following repository details. "
            f"The summary should be persuasive and highlight the strengths, skills, and achievements of {github_username},"
            f"showcasing why they would be a valuable hire.\n\n"
            f"INPUT\n"
            f"INPUT:\n\n"
            f"Repository Name: {repo_info['name']}\n"
            f"Description: {repo_info['description']}\n"
            f"Stars: {repo_info['stargazers_count']}\n"
            f"Forks: {repo_info['forks_count']}\n"
            f"Primary Language: {repo_info['language']}\n"
            f"Open Issues: {repo_info['open_issues_count']}\n"
            f"File Contents:\n{file_contents}\n"
            f"OUTPUT INSTRUCTIONS\n"
            f"OUTPUT:\n\n"
            f"Only output Markdown.\n\n"
            f"Use Emojis to make the output more engaging.\n\n"
            f"Generate a 'Why You Should Hire Me' summary based on the provided repository details. "
            f"Highlight the strengths, skills, and achievements of the repository owner, showcasing why they would be "
            f"a valuable hire."
        )

    def _get_response_from_openai(self, prompt):
        try:
            return self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                temperature=1,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        except Exception as e:
            logger.error(f"Failed to generate hiring statement: {e}")
            return None

    @staticmethod
    def _extract_message_from_response(response):
        if response and response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            logger.error("No message found in the response.")
            return None
