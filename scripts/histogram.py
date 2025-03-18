import matplotlib.pyplot as plt
import os
from github import Github, InputGitTreeElement
from datetime import datetime

# Authenticate with GitHub API using the token
token = os.getenv('GIT_PAT')  # Use GIT_PAT instead of GITHUB_TOKEN

# Define repository name
repo_name = "Ibe1999/web-eye-tracker-front"

# Authenticate with GitHub API
g = Github(token)
repo = g.get_repo(repo_name)

def count_labels(repo):
    """Count the number of issues for each label in a repository."""
    labels_count = {}
    for issue in repo.get_issues(state="all"):
        for label in issue.labels:
            labels_count[label.name] = labels_count.get(label.name, 0) + 1
    return labels_count

def generate_histogram(repo_name, labels_count):
    """Generate and save a histogram of issue labels."""
    if not labels_count:
        print(f"No labeled issues found in {repo_name}.")
        return None  

    # Create a bar plot for the issue labels
    plt.figure(figsize=(10, 6))
    plt.bar(labels_count.keys(), labels_count.values(), color='b')
    plt.ylabel('Number of Issues')
    plt.xlabel('Labels')
    plt.title(f'Histogram of Issues by Label - {repo_name}')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    # Save the histogram as a PNG file inside the artifacts folder
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)  # Ensure directory exists
    filename = os.path.join(artifacts_dir, "histogram.png")
    plt.savefig(filename)
    plt.close()

    print(f"Histogram saved as {filename}")
    return filename  

def commit_and_push(filename):
    """Commit and push the histogram image to the GitHub repository."""
    try:
        with open(filename, "rb") as f:
            content = f.read()
        
        # Define file path in the repo
        repo_file_path = f"artifacts/histogram.png"

        # Get the current timestamp
        commit_message = f"Updated histogram - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"

        # Check if file exists in repo
        contents = None
        try:
            contents = repo.get_contents(repo_file_path)
        except:
            pass  # File doesn't exist yet

        if contents:
            repo.update_file(repo_file_path, commit_message, content, contents.sha)
            print("Histogram updated in the repository.")
        else:
            repo.create_file(repo_file_path, commit_message, content)
            print("Histogram uploaded to the repository.")

    except Exception as e:
        print(f"Error committing file: {e}")

def main():
    try:
        print(f"Processing repository: {repo_name}")
        labels_count = count_labels(repo)
        filename = generate_histogram(repo_name, labels_count)
        if filename:
            commit_and_push(filename)
    except Exception as e:
        print(f"Error processing {repo_name}: {e}")

if __name__ == '__main__':
    main()
