# Version Management

Easy yt-dlp uses automatic semantic versioning based on PR labels.

## How It Works

When a PR is merged to `main`, the version is automatically bumped based on the PR labels:

- **`major`** label → Bump major version (e.g., 1.0.0 → 2.0.0)
  - Breaking changes
  - Major new features
  - API changes

- **`minor`** label → Bump minor version (e.g., 1.0.0 → 1.1.0)
  - New features
  - Enhancements
  - Non-breaking changes

- **`patch`** label → Bump patch version (e.g., 1.0.0 → 1.0.1)
  - Bug fixes
  - Documentation updates
  - Minor improvements

- **No label** → Defaults to patch bump

## What Gets Updated

The automation updates version numbers in:
- `src/easy_ytdlp/__init__.py`
- `README.md`
- `README-zh.md`

## GitHub Release

After version bump, a GitHub release is automatically created with:
- Release notes from PR description
- Git tag (e.g., `v1.2.3`)
- Changelog link

## Manual Version Bump

To manually bump version:

```bash
# Bump patch version (1.0.0 → 1.0.1)
python scripts/bump_version.py patch

# Bump minor version (1.0.0 → 1.1.0)
python scripts/bump_version.py minor

# Bump major version (1.0.0 → 2.0.0)
python scripts/bump_version.py major
```

## PR Labels

Make sure to add one of these labels to your PR before merging:
- `major` - for breaking changes
- `minor` - for new features
- `patch` - for bug fixes

The first matching label in priority order (major > minor > patch) will be used.
