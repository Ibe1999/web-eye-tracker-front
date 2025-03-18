import matplotlib.pyplot as plt
import os
from github import Github
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
    filename = os.path.join(artifacts_dir, "histogram.png")  # Save as histogram.png
    plt.savefig(filename)
    plt.close()

    print(f"Histogram saved as {filename}")
    return filename  

def main():
    try:
        print(f"Processing repository: {repo_name}")
        labels_count = count_labels(repo)
        generate_histogram(repo_name, labels_count)
    except Exception as e:
        print(f"Error processing {repo_name}: {e}")

if __name__ == '__main__':
    main()
