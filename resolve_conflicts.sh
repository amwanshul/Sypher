#!/bin/bash

# Remaining PRs
pr_ids=$(gh pr list --json number --jq '.[].number' | sort -n)

echo "Remaining PRs with potential conflicts: $pr_ids"

for id in $pr_ids; do
    echo "------------------------------------------"
    echo "Resolving conflicts for PR #$id"
    
    # Switch to main and ensure it's clean
    git checkout main
    git pull origin main
    
    # Get the branch name for the PR
    branch=$(gh pr view $id --json headRefName --jq '.headRefName')
    
    echo "Attempting to merge branch: $branch"
    
    # Try to merge the branch into main
    # If it fails due to conflicts, we resolve them using 'theirs' strategy (favoring the PR)
    if git merge origin/$branch; then
        echo "Clean merge for PR #$id"
    else
        echo "Conflicts detected in PR #$id, resolving with 'theirs' strategy..."
        # Checkout the PR version of all conflicting files
        git checkout --theirs .
        git add .
        git commit -m "Resolve conflicts for PR #$id by favoring PR changes"
    fi
    
    # Push the merged main back to origin
    if git push origin main; then
        echo "Successfully pushed merged main for PR #$id"
        # Close the PR since we've manually merged it
        gh pr close $id --comment "Manually merged and resolved conflicts by favoring PR changes."
    else
        echo "Failed to push main for PR #$id"
    fi
done
