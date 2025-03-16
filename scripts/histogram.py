import matplotlib.pyplot as plt
import os
from github import Github

# Authenticate with GitHub API using the token automatically provided by GitHub Actions
token = os.getenv('GITHUB_TOKEN')

# List of repositories to analyze
repositories = ["username/repository"]  # Replace with actual repositories

# Authenticate with GitHub API
g = Github(token)

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

    # Define the path to save the histogram image
    artifacts_dir = "artifacts"  # Ensure this matches the directory name
    os.makedirs(artifacts_dir, exist_ok=True)  # Create the directory if it doesn't exist
    filename = os.path.join(artifacts_dir, "histogram.png")
    print(f"Saving histogram to {filename}")  # Debugging output
    
    # Save the histogram as a PNG file inside the artifacts folder
    plt.savefig(filename)
    plt.close()  # Close the plot to free up memory
    print(f"Histogram saved as {filename}")
    
    # Return the filename so the GitHub Actions can commit it later
    return filename  

def main():
    for repo_name in repositories:
        try:
            repo = g.get_repo(repo_name)
            print(f"Processing repository: {repo_name}")
            labels_count = count_labels(repo)
            filename = generate_histogram(repo_name, labels_count)
            if filename:
                print(f"Histogram file created: {filename}")
        except Exception as e:
            print(f"Error processing {repo_name}: {e}")

if __name__ == '__main__':
    main()










