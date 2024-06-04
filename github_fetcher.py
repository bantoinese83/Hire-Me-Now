import logging

import requests


class GitHubFetcher:
    def __init__(self, token):
        self.headers = {"Authorization": f"token {token}"}

    def fetch_repository_info(self, repo_url):
        owner, repo = self._parse_github_url(repo_url)
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(repo_api_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_all_files(self, repo_url):
        owner, repo = self._parse_github_url(repo_url)
        return self._fetch_directory_contents(owner, repo, "/")

    def _fetch_directory_contents(self, owner, repo, path):
        dir_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents{path}"
        response = requests.get(dir_api_url, headers=self.headers)
        response.raise_for_status()
        contents = response.json()

        logging.info(f"Items in {path}: {contents}")

        files = {}
        for item in contents:
            if item["type"] == "file":
                file_content = item.get("content", "")
                files[item["path"]] = file_content
            elif item["type"] == "dir":
                files.update(self._fetch_directory_contents(owner, repo, item["path"]))

        return files

    @staticmethod
    def _parse_github_url(url):
        parts = str(url).rstrip("/").split("/")
        if "github.com" in parts:
            owner_index = parts.index("github.com") + 1
            if owner_index + 1 < len(parts):
                return parts[owner_index], parts[owner_index + 1]
        raise ValueError(
            "Invalid GitHub URL. Expected format: 'https://github.com/owner/repo'"
        )
