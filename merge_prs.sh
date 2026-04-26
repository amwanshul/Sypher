#!/bin/bash

# Get list of open PR IDs
pr_ids=$(gh pr list --limit 100 --json number --jq '.[].number' | sort -n)

echo "Found PRs: $pr_ids"

for id in $pr_ids; do
    echo "------------------------------------------"
    echo "Processing PR #$id"
    
    # Try to merge the PR
    # Using --merge flag for a standard merge commit.
    # The 'gh pr merge' command is non-interactive by default if flags are provided, 
    # but we'll use --admin just in case and to ensure it proceeds.
    if gh pr merge $id --merge --delete-branch; then
        echo "Successfully merged PR #$id"
    else
        echo "Failed to merge PR #$id. It might have conflicts or other issues."
    fi
done

echo "------------------------------------------"
echo "All PR processing completed."
