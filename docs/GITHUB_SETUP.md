# GitHub Repository Setup Guide

This guide documents the recommended GitHub repository settings to maximize community engagement and star conversion.

## 🔧 Repository Settings

### General Settings

1. Go to **Settings** → **General**
2. Enable these features:
   - ✅ Issues
   - ✅ Preserve this repository (for archival)
   - ✅ Sponsorships (if applicable)
   - ✅ Projects
   - ✅ Discussions

### Social Preview

1. Go to **Settings** → **General** → **Social preview**
2. Upload the generated banner image: `demos/banner.png`
3. This image appears when sharing the repo on social media

## 💬 GitHub Discussions

### Enable Discussions

1. Go to **Settings** → **General** → **Features**
2. Check **Discussions**
3. Click **Set up discussions**

### Create Discussion Categories

Create the following categories:

| Category | Description | Format |
|----------|-------------|--------|
| 📢 Announcements | Project updates and releases | Announcement |
| 💡 Ideas | Feature suggestions and brainstorming | Open discussion |
| 🙏 Q&A | Questions about using GoldenSeed | Q&A |
| 🎮 Show and tell | Share your projects using GoldenSeed | Open discussion |
| 🐛 Troubleshooting | Get help with issues | Q&A |
| 🌟 General | General discussion about GoldenSeed | Open discussion |

### Discussion Templates

Create templates for common discussion types:

**Feature Idea Template:**
```markdown
## Problem
What problem does this solve?

## Proposed Solution
How should it work?

## Use Case
How would you use this?

## Additional Context
Any other information?
```

## 🏷️ Issue Labels

### Create Custom Labels

Go to **Issues** → **Labels** and create these labels:

#### Type Labels
- `bug` (red) - Something isn't working
- `enhancement` (blue) - New feature or request
- `documentation` (light blue) - Improvements to docs
- `question` (purple) - Questions about usage
- `good first issue` (green) - Good for newcomers
- `help wanted` (orange) - Extra attention needed

#### Priority Labels
- `priority: critical` (dark red) - Needs immediate attention
- `priority: high` (orange) - Important issue
- `priority: medium` (yellow) - Normal priority
- `priority: low` (light gray) - Nice to have

#### Area Labels
- `area: core` (navy) - Core algorithm
- `area: examples` (teal) - Example code
- `area: performance` (purple) - Performance related
- `area: testing` (pink) - Testing infrastructure
- `area: cross-platform` (brown) - Platform compatibility

#### Status Labels
- `status: triage` (gray) - Needs triage
- `status: in-progress` (yellow) - Being worked on
- `status: blocked` (red) - Blocked by something
- `status: duplicate` (light gray) - Duplicate issue
- `status: wontfix` (white) - Won't be fixed

### Label Good First Issues

1. Go through existing issues
2. Tag beginner-friendly issues with `good first issue`
3. Examples of good first issues:
   - Documentation improvements
   - Adding code examples
   - Fixing typos
   - Adding tests
   - Small bug fixes with clear reproduction steps

## 📋 Projects

### Create Project Board

1. Go to **Projects** → **New project**
2. Choose **Board** template
3. Name it "GoldenSeed Development"
4. Create columns:
   - 📥 Backlog
   - 🎯 To Do
   - 🚧 In Progress
   - 👀 Review
   - ✅ Done

### Link Issues to Project

- Add relevant issues to the project board
- This helps contributors see what's being worked on

## 🌟 GitHub Actions

### Status Badges

Already configured in README.md:
- Build status
- Test coverage (if configured)
- PyPI version

### Additional Workflows to Consider

1. **Stale Issue Management**
   - Auto-close inactive issues after 60 days
   - Add "stale" label after 30 days

2. **Welcome Bot**
   - Greet first-time contributors
   - Link to CONTRIBUTING.md

3. **Release Automation**
   - Auto-generate release notes
   - Publish to PyPI on tag push

## 📱 Repository Topics

1. Go to **About** (top right on repo page)
2. Click the gear icon ⚙️
3. Add these topics:
   ```
   procedural-generation
   prng
   deterministic
   golden-ratio
   procedural-content
   game-development
   python
   cross-platform
   zero-dependencies
   reproducible-testing
   seeded-random
   infinite-streams
   ```

## 📖 Repository Description

Update the short description (under About):

```
🌟 Infinite reproducible high-entropy streams from tiny fixed seeds. Perfect for procedural generation, reproducible testing, and deterministic simulations.
```

Add website: `https://github.com/beanapologist/seed`

## 📄 Community Health Files

Ensure these files exist (✅ already created):
- ✅ README.md
- ✅ LICENSE
- ✅ CONTRIBUTING.md
- ✅ CODE_OF_CONDUCT.md (optional but recommended)
- ✅ SECURITY.md
- ✅ Issue templates
- ✅ Pull request template

### Create CODE_OF_CONDUCT.md (Optional)

Use GitHub's template:
1. Go to **Insights** → **Community**
2. Click **Add** next to Code of Conduct
3. Choose **Contributor Covenant 2.1**

## 🎯 Optimize for Discovery

### README Checklist
- ✅ Eye-catching badges at top
- ✅ Clear tagline
- ✅ Visual demo (GIF/image)
- ✅ Quick install instructions
- ✅ Code examples
- ✅ Comparison table
- ✅ Clear use cases
- ✅ Contributing section
- ✅ Links to docs and examples

### SEO Keywords

Already included in:
- Repository topics
- README.md content
- setup.py keywords
- Issue templates

## 📊 Insights & Analytics

### Enable Insights

1. Go to **Insights**
2. Review:
   - Traffic (views, clones)
   - Popular content
   - Referring sites
   - Visitor demographics

### Track Success Metrics

Monitor:
- ⭐ Stars growth
- 🔱 Forks
- 👁️ Watchers
- 📊 Traffic
- 🐛 Issue closure rate
- 🤝 PR acceptance rate
- 💬 Discussion participation

## 🚀 Growth Strategies

### Cross-Promotion

1. **Share on social media**:
   - Twitter/X with #GameDev #ProceduralGeneration
   - Reddit: r/proceduralgeneration, r/Python, r/gamedev
   - Hacker News
   - Dev.to articles

2. **Create content**:
   - Tutorial videos
   - Blog posts about use cases
   - Live coding streams
   - Conference talks

3. **Engage with community**:
   - Answer questions in Discussions
   - Help with issues
   - Review pull requests
   - Acknowledge contributors

### Monthly Tasks

- 📝 Write release notes for new versions
- 🏷️ Label new issues
- 💬 Respond to discussions
- 🔍 Review analytics
- 📢 Share project updates

## 📝 Checklist

Use this checklist to verify everything is set up:

- [ ] Discussions enabled with categories
- [ ] Custom labels created
- [ ] Project board set up
- [ ] Repository topics added
- [ ] Social preview image uploaded
- [ ] Community health files complete
- [ ] Issue templates configured
- [ ] Good first issues labeled
- [ ] README.md optimized
- [ ] GitHub Actions working
- [ ] Analytics enabled

## 🎉 Launch Checklist

Before announcing the polished repo:

- [ ] Generate demo visualizations (`python3 examples/generate_demo_visualizations.py`)
- [ ] Update README with actual demo images
- [ ] Test all example code
- [ ] Verify all links work
- [ ] Run full test suite
- [ ] Review documentation for typos
- [ ] Create initial discussion post welcoming contributors
- [ ] Tag a new release
- [ ] Announce on social media

---

**Note**: These settings are recommendations based on successful open-source projects. Adjust based on your project's specific needs.

For questions about these settings, open a [Discussion](https://github.com/beanapologist/seed/discussions)!
