# Quick branch hygiene check

Quick branch hygiene check and immediate improvements: $ARGUMENTS

Execute rapid branch analysis focusing on immediate wins and obvious improvements. Use this for daily/weekly branch maintenance.

## Rapid Analysis Mode

**Step 1: Quick Branch Overview**

```bash
# Get branches modified in last 14 days with change stats
git for-each-ref --format='%(refname:short) %(committerdate:relative) %(authorname)' refs/heads/ --sort=-committerdate | head -10
```

**Step 2: Identify Low-Hanging Fruit**
Focus on branches with these patterns for immediate merge candidates:

**A. Universal Improvements (Merge Immediately)**

- `.eslintrc`, `prettier.config.js`, `.github/workflows/` changes
- `package.json` dependency updates
- `CONTRIBUTING.md`, `README.md` improvements  
- `pyproject.toml`, `requirements.txt` updates
- General bug fixes in shared utilities

**B. ProxmoxMCP-Specific Quick Wins**

- Updates to `CLAUDE.md` that improve development guidance
- Improvements to `formatting/` module that benefit all tools
- Enhancements to `core/proxmox.py` error handling
- Quality improvements to existing tools in `tools/` directory
- Test infrastructure improvements

**Step 3: Execute Quick Merge Strategy**
For each identified improvement:

```bash
# Create quality improvement branch
git checkout main && git pull origin main
git checkout -b chore/quality-improvements-$(date +%Y%m%d)

# Cherry-pick specific improvements
git cherry-pick -x [commit-hash] # Add meaningful commit messages
```

**Step 4: Generate Quick PR**
Create immediate PR for quality improvements:

- Title: "Quality improvements from feature branches [DATE]"
- Description: List source branches and specific improvements
- Label: `enhancement`, `code-quality`
- Assign to `claude-code-bot` for automated review

## Focus Areas for ProxmoxMCP

**High-Value Immediate Merges:**

- Improvements to ProxmoxManager error handling
- Rich formatting enhancements in `formatting/` module
- Test utilities that benefit multiple tools
- Documentation improvements that clarify current functionality
- CI/CD improvements from `.github/workflows/`

**Keep in Feature Branches:**

- Incomplete MCP server implementations
- New Proxmox API endpoints under development
- Experimental authentication methods
- WIP tool implementations in `tools/` directory

**Red Flags (Need Attention):**

- Feature branches modifying core authentication without clear purpose
- Changes to existing tool interfaces without feature justification
- Configuration changes that might break existing setups

## Quick Decision Matrix

**Immediate Merge If:**

- ✅ Improves code quality for existing functionality
- ✅ Fixes bugs in current stable features
- ✅ Enhances development experience (linting, testing, docs)
- ✅ Security improvements with no breaking changes
- ✅ Performance optimizations with no API changes

**Keep in Branch If:**

- 🔄 Implements new Proxmox functionality
- 🔄 Changes existing tool APIs
- 🔄 Adds new MCP server capabilities
- 🔄 Experimental or incomplete implementations
- 🔄 Breaking changes requiring coordination

**Needs Investigation If:**

- ⚠️ Mixes feature work with quality improvements
- ⚠️ Large changes without clear branch purpose
- ⚠️ Modifications to stable core components
- ⚠️ Configuration changes affecting authentication
- ⚠️ Cross-cutting changes affecting multiple tool categories

## Output Quick Summary

Generate immediate actionable summary:

```markdown
## Quick Branch Hygiene - [Date]

### Immediate Merge Candidates (< 30 min effort)
- Branch: feature/vm-snapshot-tools
  - File: `formatting/table_formatter.py` (performance improvement)
  - Action: Cherry-pick commit abc123

### This Week's Focus Branches
- feature/mcp-claude-sdk-integration: 75% complete, ETA 1 week
- bugfix/authentication-retry-logic: Ready for review

### Cleanup Needed
- feature/old-experiment: No activity 30+ days, consider closing
- hotfix/temp-fix: Changes should be in main, needs immediate merge

### Next Actions
1. Create quality improvement PR with 3 identified commits
2. Review feature/mcp-claude-sdk-integration for completion
3. Close stale experimental branches
```

**Integration Note:** Use this command weekly before your automated GitHub issue processing to maintain clean branch state for your automation workflows.
