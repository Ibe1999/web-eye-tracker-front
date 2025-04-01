name: Generate and Upload Histogram

on:
  schedule:
    - cron: '0 0 * * 0'  # Runs every Sunday at midnight UTC
  workflow_dispatch:  # Allows manual trigger

jobs:
  generate-histogram:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_PAT }}  # Ensure this token has repo write permissions

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt  # Add dependencies if needed

      - name: Run histogram script
        run: python scripts/histogram.py  # Ensure correct path

      - name: Configure Git
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "github-actions@github.com"

      - name: Commit and Push Updated Histogram
        run: |
          git add artifacts/histogram.png
          git commit -m "Update histogram (automated)"
          git push origin main


