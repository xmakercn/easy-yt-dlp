# GitHub Actions Workflows

This directory contains automated workflows for the Easy yt-dlp project.

## Available Workflows

### Version Bump (`version-bump.yml`)

Automatically bumps version and creates releases when PRs are merged.

**Trigger**: When a PR is merged to `main`

**What it does**:
1. Reads PR labels to determine version bump type
2. Updates version in:
   - `src/easy_ytdlp/__init__.py`
   - `README.md`
   - `README-zh.md`
3. Commits version changes
4. Creates Git tag (e.g., `v2.0.1`)
5. Creates GitHub Release with PR description

**Required PR Labels**:
- `major` - Breaking changes (1.0.0 → 2.0.0)
- `minor` - New features (1.0.0 → 1.1.0)
- `patch` - Bug fixes (1.0.0 → 1.0.1)

If no label is present, defaults to `patch`.

## Setup

No additional setup required. Workflows run automatically on PR merge.

## Testing Locally

Test version bump script:

```bash
# Test patch bump
python scripts/bump_version.py patch

# Test minor bump
python scripts/bump_version.py minor

# Test major bump
python scripts/bump_version.py major

# Run all tests
python test_version_management.py
```

## Troubleshooting

If version bump fails:
1. Check PR has appropriate label
2. Verify `scripts/bump_version.py` is executable
3. Check GitHub Actions logs for errors
4. Ensure version format in `__init__.py` is correct: `__version__ = "X.Y.Z"`
