# Creating Releases

This document explains how to create releases with the automated Windows executable.

## GitHub Actions Workflow

A GitHub Actions workflow has been set up in `.github/workflows/release.yml` that automatically:

1. ✅ Builds the Windows executable using PyInstaller
2. ✅ Creates a GitHub Release
3. ✅ Uploads `aoe2-apm.exe` as a release asset

## How to Create a Release

### Prerequisites

Ensure you have:
- Pushed all changes to GitHub
- Workflow file committed in `.github/workflows/release.yml`
- A GitHub repository (not local git server)

### Step 1: Create a Version Tag

```bash
# Create an annotated tag with version number
git tag -a v1.0.0 -m "Release v1.0.0 - Description of changes"

# View the tag to confirm
git tag -l
```

### Step 2: Push the Tag to GitHub

```bash
# Push the tag to trigger the workflow
git push origin v1.0.0
```

**Important**: This must be pushed to the actual GitHub repository, not a local git server.

### Step 3: Monitor the Workflow

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Watch the "Build and Release Windows Executable" workflow run
4. It takes approximately 5-10 minutes to complete

### Step 4: Verify the Release

Once complete:

1. Go to your repository's "Releases" page
2. You should see the new release (e.g., "v1.0.0")
3. The `aoe2-apm.exe` file should be attached
4. Users can now download it directly

## Release Versions

Use semantic versioning:

- **v1.0.0** - Major release (breaking changes)
- **v1.1.0** - Minor release (new features)
- **v1.0.1** - Patch release (bug fixes)

Examples:

```bash
# First stable release
git tag -a v1.0.0 -m "Release v1.0.0 - Initial stable release"

# Add new features
git tag -a v1.1.0 -m "Release v1.1.0 - Added batch processing improvements"

# Bug fix
git tag -a v1.0.1 -m "Release v1.0.1 - Fixed parsing error with corrupted files"
```

## Manual Trigger (Alternative)

If you don't want to create a tag, you can manually trigger the workflow:

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "Build and Release Windows Executable"
4. Click "Run workflow"
5. Choose the branch and run

Note: Manual triggers don't create a tag, so you'll need to create a release manually via GitHub UI after the build completes.

## Current Status

The workflow is ready and committed to the repository. Here's what's been done:

✅ GitHub Actions workflow created (`.github/workflows/release.yml`)
✅ Workflow pushed to branch `claude/aoe2-record-apm-tool-011CUKEPiJahS2ZmSwm38Tii`
✅ Tag `v1.0.0` created locally
⏳ Tag needs to be pushed from actual GitHub repository (not local git server)

## Next Steps for Repository Owner

Once this branch is merged to the main branch on GitHub:

1. **Merge the PR** to main branch
2. **Checkout main** locally:
   ```bash
   git checkout main
   git pull origin main
   ```

3. **Create and push the tag**:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0 - Initial release"
   git push origin v1.0.0
   ```

4. **Watch the magic happen**:
   - GitHub Actions builds the .exe
   - Release is created automatically
   - .exe is uploaded and ready for download

5. **Share the download link**:
   ```
   https://github.com/YOUR_USERNAME/Claudex/releases/latest
   ```

## Troubleshooting

### Workflow doesn't trigger

- Ensure tag format matches `v*.*.*` (e.g., v1.0.0, v2.1.3)
- Check that workflow file is on the main/default branch
- Verify GitHub Actions are enabled in repository settings

### Build fails

- Check the Actions log for error messages
- Common issues:
  - Missing dependencies in requirements.txt
  - PyInstaller spec file errors
  - Python version incompatibility

### Release created but no .exe

- Check workflow logs for upload errors
- Verify the .exe was built (check "Build executable" step)
- Ensure GITHUB_TOKEN has proper permissions

## Download Links

After release creation, users can download via:

**Latest release**:
```
https://github.com/YOUR_USERNAME/Claudex/releases/latest/download/aoe2-apm.exe
```

**Specific version**:
```
https://github.com/YOUR_USERNAME/Claudex/releases/download/v1.0.0/aoe2-apm.exe
```

## Automation Complete!

Once set up, releasing new versions is as simple as:

```bash
git tag -a v1.1.0 -m "Release v1.1.0 - New features"
git push origin v1.1.0
```

Everything else happens automatically! 🎉
