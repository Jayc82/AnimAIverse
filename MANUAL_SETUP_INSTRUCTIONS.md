# 🔐 MANUAL SETUP INSTRUCTIONS

**IMPORTANT**: These steps must be completed manually to fully protect your IP.

---

## Step 1: Make Repository Private

### Why This Matters
Making the repository private ensures only authorized users can view your code, protecting your intellectual property.

### Instructions

1. **Navigate to Repository Settings**
   - Go to: https://github.com/Jayc82/AnimAIverse/settings
   - You must be logged in as the repository owner

2. **Locate Danger Zone**
   - Scroll to the bottom of the settings page
   - Find the red "Danger Zone" section

3. **Change Visibility**
   - Click **"Change repository visibility"**
   - A modal will appear
   - Select **"Make private"**
   - Type the repository name `Jayc82/AnimAIverse` to confirm
   - Click **"I understand, change repository visibility"**

4. **Verify**
   - Repository should now show a 🔒 private badge
   - Only you and invited collaborators can see it

---

## Step 2: Enable Branch Protection

### Why This Matters
Branch protection prevents accidental or unauthorized changes to your main branch.

### Instructions

1. **Navigate to Branch Settings**
   - Go to: https://github.com/Jayc82/AnimAIverse/settings/branches
   - Or: Settings → Branches from the repository

2. **Add Branch Protection Rule**
   - Click **"Add branch protection rule"** (or **"Add rule"**)

3. **Configure Rule**
   - **Branch name pattern**: `main`
   - Enable these checkboxes:
     - ✅ **Require a pull request before merging**
       - ✅ Require approvals: 1
       - ✅ Dismiss stale pull request approvals when new commits are pushed
     - ✅ **Require status checks to pass before merging**
       - ✅ Require branches to be up to date before merging
     - ✅ **Require conversation resolution before merging**
     - ✅ **Include administrators** (prevents even you from bypassing rules)
     - ✅ **Restrict who can push to matching branches**
       - Select only yourself or trusted collaborators
     - ✅ **Allow force pushes** → Keep this UNCHECKED (prevent force push)
     - ✅ **Allow deletions** → Keep this UNCHECKED (prevent branch deletion)

4. **Save**
   - Click **"Create"** or **"Save changes"** at the bottom

5. **Verify**
   - You should see "main" listed under "Branch protection rules"
   - Try to push directly to main - it should be blocked

---

## Step 3: Enable Tag Protection (Recommended)

### Why This Matters
Tag protection prevents deletion or modification of version tags (like v0.1.0-prototype).

### Instructions

1. **Navigate to Tags Settings**
   - Go to: https://github.com/Jayc82/AnimAIverse/settings/tag_protection
   - Or: Settings → Tags from the repository

2. **Add Tag Protection Rule**
   - Click **"New rule"**

3. **Configure Rule**
   - **Pattern**: `v*`
   - This protects all tags starting with "v" (v0.1.0, v1.0.0, etc.)

4. **Save**
   - Click **"Add rule"**

5. **Verify**
   - You should see `v*` listed under "Protected tags"
   - Try to delete tag v0.1.0-prototype - it should be blocked

---

## Step 4: Configure Additional Security Settings (Optional but Recommended)

### Enable Dependabot Security Updates

1. Go to: https://github.com/Jayc82/AnimAIverse/settings/security_analysis
2. Enable:
   - ✅ **Dependency graph**
   - ✅ **Dependabot alerts**
   - ✅ **Dependabot security updates**

### Enable Secret Scanning

1. Same page as above
2. Enable:
   - ✅ **Secret scanning**
   - ✅ **Push protection** (prevents committing secrets)

### Review Collaborators

1. Go to: https://github.com/Jayc82/AnimAIverse/settings/access
2. Review who has access
3. Remove anyone who shouldn't have access

---

## Verification Checklist

After completing all steps, verify:

- [ ] Repository shows 🔒 **Private** badge
- [ ] Main branch shows 🛡️ **Protected** badge
- [ ] Tag v0.1.0-prototype is listed and protected
- [ ] Direct pushes to main are blocked
- [ ] Force pushes are disabled
- [ ] Branch deletion is disabled
- [ ] Security features enabled (optional but recommended)

---

## Testing Branch Protection

To verify branch protection is working:

```bash
# This should be BLOCKED
echo "test" >> README.md
git add README.md
git commit -m "test commit"
git push origin main
```

**Expected Result**: Push should be rejected with a message about branch protection.

**Correct Workflow** (after protection is enabled):
1. Create a new branch: `git checkout -b feature-branch`
2. Make changes and commit
3. Push branch: `git push origin feature-branch`
4. Create Pull Request on GitHub
5. Get approval
6. Merge through GitHub UI

---

## Need Help?

If you encounter issues:

1. **Documentation**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches

2. **Verify Permissions**: Ensure you're logged in as the repository owner

3. **Check Organization Settings**: If this is an organization repo, check org-level permissions

---

## Security Best Practices

After setup:

- ✅ Never commit API keys or secrets
- ✅ Use environment variables for sensitive data
- ✅ Review all pull requests carefully
- ✅ Keep dependencies updated
- ✅ Enable two-factor authentication on your GitHub account
- ✅ Use SSH keys or personal access tokens (not passwords)
- ✅ Regularly audit repository access
- ✅ Back up code regularly

---

## Timeline

**Estimated Time**: 10-15 minutes

1. Make repository private: 2 minutes
2. Enable branch protection: 5 minutes
3. Enable tag protection: 2 minutes
4. Additional security settings: 5 minutes

---

## Questions?

If something doesn't work as expected:
1. Check that you're the repository owner
2. Verify you have admin permissions
3. Clear browser cache and try again
4. Use incognito/private browsing mode
5. Try a different browser

---

**Remember**: These settings protect your intellectual property. Take the time to set them up correctly!

🔒 **Your code. Your IP. Your protection.**
