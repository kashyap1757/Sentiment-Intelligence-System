#!/usr/bin/env bash
set -u  # fail on unset vars (but don't use -e so one missing file won't stop all)

echo "== Sentiment-Intelligence-System cleanup script =="

# Ensure we're in a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ Not inside a git repository. cd into your repo first."
  exit 1
fi

echo "📍 Repo root: $(git rev-parse --show-toplevel)"
cd "$(git rev-parse --show-toplevel)" || exit 1

# Helper: move only if source exists
move_if_exists () {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    git mv "$src" "$dst"
    echo "✅ moved: $src -> $dst"
  else
    echo "⚠️  skip (not found): $src"
  fi
}

# Helper: untrack only if tracked
untrack_if_tracked () {
  local p="$1"
  if git ls-files --error-unmatch "$p" >/dev/null 2>&1; then
    git rm -r --cached "$p"
    echo "✅ untracked from git index: $p"
  else
    echo "⚠️  skip (not tracked): $p"
  fi
}

# Create target folders
mkdir -p docs/lab assets/images scripts tests

# Move files if present
move_if_exists "EXPERIMENT_REPORT.md" "docs/EXPERIMENT_REPORT.md"
move_if_exists "POWERBI_DASHBOARD_GUIDE.md" "docs/POWERBI_DASHBOARD_GUIDE.md"
move_if_exists "Lab Practice II -2026 mtech.docx" "docs/lab/Lab Practice II -2026 mtech.docx"
move_if_exists "Lab Practice II -2026 mtech.pdf" "docs/lab/Lab Practice II -2026 mtech.pdf"
move_if_exists "sentiment_dashboard_full_view_final_1773680925977.png" "assets/images/sentiment_dashboard_full_view_final_1773680925977.png"
move_if_exists "sentiment_project_poster_full_high_res_1773682706603.png" "assets/images/sentiment_project_poster_full_high_res_1773682706603.png"
move_if_exists "generate_data.py" "scripts/generate_data.py"
move_if_exists "test_api.py" "tests/test_api.py"

# Write/overwrite .gitignore safely
cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual environments
venv/
.venv/
env/

# Jupyter
.ipynb_checkpoints/

# MLflow / experiment artifacts
mlruns/
mlflow.db

# Logs and runtime outputs
*.log
api_results.json
api_test_output.txt

# OS / IDE
.DS_Store
.vscode/
.idea/
EOF
echo "✅ updated .gitignore"

# Untrack generated/runtime artifacts if currently tracked
untrack_if_tracked "venv"
untrack_if_tracked "mlruns"
untrack_if_tracked "mlflow.db"
untrack_if_tracked "api_results.json"
untrack_if_tracked "api_test_output.txt"

# Stage all remaining changes
git add -A

echo
echo "===== REVIEW CHANGES ====="
git status --short
echo "=========================="
echo
echo "If everything looks good, run:"
echo "  git commit -m \"Refactor repo structure and remove generated artifacts\""
echo "  git push origin main"