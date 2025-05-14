import matplotlib.pyplot as plt
import os
from github import Github

token = os.getenv('GH_PAT')
repo_name = "ruxailab/web-eye-tracker-front"

g = Github(token)
repo = g.get_repo(repo_name)

def count_labels(repo):
    labels_count = {}
    for issue in repo.get_issues(state="all"):
        for label in issue.labels:
            labels_count[label.name] = labels_count.get(label.name, 0) + 1
    return labels_count

def generate_histogram(repo_name, labels_count):
    if not labels_count:
        print(f"No labeled issues found in {repo_name}.")
        return None

    plt.figure(figsize=(10, 6))
    plt.bar(labels_count.keys(), labels_count.values(), color='b')
    plt.ylabel('Number of Issues')
    plt.xlabel('Labels')
    plt.title(f'Histogram of Issues by Label - {repo_name}')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    artifacts_dir = os.path.join(os.getcwd(), 'artifacts')
    os.makedirs(artifacts_dir, exist_ok=True)
    filename = os.path.join(artifacts_dir, "histogram.png")
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
        print(f"Error: {e}")

if __name__ == '__main__':
    main()


