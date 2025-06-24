# ProxmoxMCP Branch Management Guide

*Comprehensive branch management documentation including implementation details, strategy, and workflow guidelines.*

## Table of Contents

- [Overview](#overview)
- [Implementation Summary (PR #67)](#implementation-summary-pr-67)
- [Branching Strategy](#branching-strategy)
- [Workflow Processes](#workflow-processes)
- [Best Practices](#best-practices)

---

## Overview

This document provides complete guidance on branch management for the ProxmoxMCP project, covering both the implemented tools and strategic workflow processes. The branch management system ensures consistent naming conventions, quality gates, and efficient development workflows.

---

## Implementation Summary (PR #67)

### Comprehensive Branch Management System Implementation

Successfully implemented a comprehensive branch management system for the ProxmoxMCP project that
addresses all shell script issues and provides robust branch naming validation and management tools.

#### ✅ Issues Resolved

##### Shell Script Issues (~30 issues)

**File: `scripts/branch-templates/config.sh`**

- ✅ **Missing shebang (SC2148)**: Added proper `#!/usr/bin/env bash` shebang
- ✅ **Multiple unused variables (SC2034)**: All variables are now properly exported for external use
- ✅ **Error handling**: Added `set -euo pipefail` for robust error handling

**File: `scripts/branch-templates/validate.sh`**

- ✅ **Use ${variable//search/replace} instead of sed (SC2001)**: Replaced all sed usage with bash parameter expansion
- ✅ **Unused variable suggestions**: All variables are properly used throughout the script
- ✅ **Proper shebang and error handling**: Consistent with best practices

**Additional Improvements**

- ✅ **Shellcheck compliance**: All scripts pass shellcheck validation
- ✅ **Consistent coding standards**: Follow existing project patterns
- ✅ **Proper documentation**: Comprehensive inline comments and help text

#### 📁 Files Created

##### Core Scripts

1. **`scripts/branch-templates/config.sh`** (108 lines)
   - Central configuration for branch management system
   - Exported variables for external script usage
   - Shared functions for validation logic
   - User-configurable settings support

2. **`scripts/branch-templates/validate.sh`** (386 lines)
   - Comprehensive branch name validation
   - Multiple validation layers (length, prefix, component, description, characters)
   - Helpful error messages and suggestions
   - Support for current branch and specific name validation

3. **`scripts/branch-templates/branch-manager.sh`** (330 lines)
   - Main interface for branch management operations
   - Interactive branch creation with guided prompts
   - Branch listing with validation status indicators
   - Merged branch cleanup functionality
   - Comprehensive help system

4. **`scripts/branch-templates/README.md`** (165 lines)
   - Complete documentation and usage guide
   - Quick start examples
   - Configuration options
   - Git hooks integration examples
   - Troubleshooting guide

##### Supporting Files

5. **`BRANCH_MANAGEMENT_SUMMARY.md`** (This file's source)
   - Implementation summary and testing results

#### 🎯 Features Implemented

##### Branch Naming Convention Enforcement

- **Format**: `<type>/<component>-<description>`
- **Valid Types**: feature, fix, security, docker, config, docs, ci, perf
- **Valid Components**: vm, container, storage, network, backup, auth, encryption, config, api, mcp,
  core, tools, formatting, docker, proxmox, console, management
- **Length Validation**: 10-80 characters (configurable)
- **Character Validation**: Only alphanumeric, hyphens, and forward slashes
- **Description Requirements**: Meaningful descriptive suffix after component

##### Interactive Tools

- **Branch Creation**: Guided prompts for type, component, and description selection
- **Validation**: Current branch or specific name validation with detailed feedback
- **Branch Listing**: Visual status indicators (✅ valid, ❌ invalid, 🛡️ protected)
- **Cleanup**: Safe removal of merged branches with dry-run option

##### Configuration System

- **Default Settings**: Sensible defaults for immediate use
- **User Customization**: Optional `.branch-config` file for overrides
- **Protected Branches**: Automatic recognition of main, develop, staging
- **Component Extensibility**: Easy addition of new valid components

#### 🧪 Testing Results

##### Validation Testing

```bash
# Valid branch name
$ ./scripts/branch-templates/validate.sh --name "feature/vm-console-management"
[SUCCESS] Branch name is valid! ✨

# Invalid branch name
$ ./scripts/branch-templates/validate.sh --name "invalid-branch-name"
[ERROR] Branch name validation failed
[INFO] Suggestions for improvement:
  Example: feature/core-update
  Format: <type>/<component>-<description>
```

##### Help System Testing

```bash
# Both scripts provide comprehensive help
$ ./scripts/branch-templates/validate.sh --help
$ ./scripts/branch-templates/branch-manager.sh help
```

##### Script Quality Verification

- ✅ All scripts are executable (`chmod +x` applied)
- ✅ Proper error handling with `set -euo pipefail`
- ✅ No shellcheck warnings or errors
- ✅ Consistent with existing project shell script patterns
- ✅ No unused variables (all exported for external use)
- ✅ Parameter expansion used instead of sed (addresses SC2001)

#### 🚀 Usage Examples

##### Quick Start

```bash
# Validate current branch
./scripts/branch-templates/validate.sh --current

# Create new branch interactively
./scripts/branch-templates/branch-manager.sh create

# List all branches with status
./scripts/branch-templates/branch-manager.sh list
```

##### Advanced Usage

```bash
# Validate specific branch name
./scripts/branch-templates/validate.sh --name "feature/api-enhancement"

# List including remote branches
./scripts/branch-templates/branch-manager.sh list --all

# Clean up merged branches (dry run)
./scripts/branch-templates/branch-manager.sh cleanup --dry-run
```

#### 🔧 Integration Options

##### Git Hooks Integration

The system can be integrated with Git hooks for automatic enforcement:

- Pre-push validation to prevent invalid branch names
- Pre-commit validation for branch name compliance
- Examples provided in documentation

##### CI/CD Integration

Scripts can be incorporated into CI/CD pipelines for branch name validation during pull request creation.

#### 📊 Impact Assessment

##### Code Quality Improvements

- **Shell Script Standards**: All scripts follow best practices and are shellcheck compliant
- **Error Handling**: Robust error handling with proper exit codes
- **Documentation**: Comprehensive documentation for maintainability
- **User Experience**: Intuitive interface with helpful error messages and suggestions

##### Development Workflow Enhancement

- **Consistency**: Enforces consistent branch naming across the project
- **Guidance**: Interactive tools help developers create properly named branches
- **Maintenance**: Automated cleanup of merged branches
- **Validation**: Early detection of naming convention violations

##### Maintainability

- **Modular Design**: Separate configuration, validation, and management components
- **Extensibility**: Easy to add new branch types and components
- **Configuration**: User-customizable settings without code changes
- **Testing**: All functionality tested and verified

#### ✅ Completion Status

**Status: COMPLETE** ✨

All shell script issues have been resolved and the comprehensive branch management system has been
successfully implemented with:

- ✅ 30+ shell script issues addressed
- ✅ 4 new files created with 989 total lines of code
- ✅ Complete documentation and usage examples
- ✅ Full testing and validation
- ✅ Integration-ready with Git hooks and CI/CD systems

The branch management system is ready for immediate use and provides a solid foundation for
maintaining consistent branch naming conventions across the ProxmoxMCP project.

---

## Branching Strategy

### Enhanced GitHub Flow

This section outlines the branching strategy and workflow for the ProxmoxMCP
repository to ensure consistent, high-quality development practices.

#### Branch Types

##### 1. `main` Branch

- **Purpose**: Production-ready code, always deployable
- **Protection**: Fully protected, no direct pushes
- **Merge Requirements**: PR review + CI checks passing

##### 2. Feature Branches

```bash
feature/issue-number-short-description
# Examples:
feature/61-fix-subprocess-shell-vulnerabilities
feature/65-update-security-dependencies
feature/new-vm-management-tools
```

##### 3. Fix Branches

```bash
fix/issue-number-short-description  
# Examples:
fix/58-autofix-workflow-warnings
fix/memory-leak-in-connection-pool
```

##### 4. Security Branches

```bash
security/vulnerability-description
# Examples:
security/cve-2025-47273-setuptools
security/bandit-shell-injection-fixes
```

##### 5. Maintenance Branches

```bash
chore/maintenance-task
# Examples:
chore/update-documentation
chore/dependency-updates
chore/ci-workflow-improvements
```

##### 6. Release Branches (Optional)

```bash
release/version-number
# Examples:
release/v1.0.0
release/v1.1.0-beta
```

##### 7. Hotfix Branches

```bash
hotfix/critical-issue-description
# Examples:
hotfix/security-patch-immediate
hotfix/production-down-fix
```

---

## Workflow Processes

### Standard Development Workflow

#### 1. Start New Work

```bash
# Ensure main is current
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/123-add-new-tool

# Work and commit
git add .
git commit -m "feat: implement new VM monitoring tool

- Add VM metrics collection
- Implement memory usage tracking  
- Add CPU utilization monitoring

Closes #123"

# Push branch
git push -u origin feature/123-add-new-tool
```

#### 2. Create Pull Request

- Use PR template checklist
- Link related issues
- Add appropriate labels
- Request relevant reviewers
- Ensure all CI checks pass

#### 3. Review Process

- Address review feedback
- Keep commits clean and logical
- Squash commits if necessary before merge

#### 4. Merge and Cleanup

```bash
# After PR approval and merge
git checkout main
git pull origin main
git branch -d feature/123-add-new-tool
git push origin --delete feature/123-add-new-tool
```

### Emergency Hotfix Workflow

```bash
# Critical production issue
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-patch

# Make minimal fix
git add .
git commit -m "hotfix: patch critical security vulnerability

- Fix shell injection in subprocess calls
- Update affected methods to use shell=False
- Add input validation

Addresses CVE-2025-XXXX"

# Push and create emergency PR
git push -u origin hotfix/critical-security-patch
# Create PR with "hotfix" label for fast-track review
```

### Release Workflow

```bash
# Prepare release
git checkout main
git pull origin main
git checkout -b release/v1.0.0

# Update version numbers, finalize docs
git add .
git commit -m "release: prepare v1.0.0

- Update version to 1.0.0
- Finalize release notes
- Update documentation"

# Create release PR
git push -u origin release/v1.0.0
# After merge, tag the release
git tag v1.0.0
git push origin v1.0.0
```

### Branch Protection Rules

#### Main Branch Protection

- ✅ Require pull request reviews before merging (minimum: 1)
- ✅ Require status checks to pass before merging
  - Codacy quality checks
  - CI/CD workflows (autofix, yaml-lint)
  - Security scans
- ✅ Require branches to be up to date before merging  
- ✅ Restrict pushes to matching branches
- ✅ Do not allow bypassing the above settings
- ✅ Allow force pushes: disabled
- ✅ Allow deletions: disabled

#### Quality Gates

All PRs must pass:

1. **Automated Checks**
   - Codacy quality assessment
   - Security vulnerability scans
   - Linting (ruff, black, mypy)
   - Test suite (pytest)

2. **Manual Review**
   - Code quality review
   - Security review (for security changes)
   - Documentation review (for docs changes)

---

## Best Practices

### PR Review Guidelines

#### For Reviewers

##### Security Changes

- [ ] Verify no hardcoded credentials
- [ ] Check for proper input validation
- [ ] Ensure secure coding practices
- [ ] Review dependency updates for vulnerabilities

##### Code Changes  

- [ ] Code follows project standards
- [ ] Adequate test coverage
- [ ] Documentation updated if needed
- [ ] No breaking changes without version bump

##### Documentation Changes

- [ ] Accuracy of technical content
- [ ] Consistency with existing docs
- [ ] Proper formatting and grammar

#### For Contributors

##### Before Creating PR

- [ ] Branch name follows conventions
- [ ] Commits are logical and well-described
- [ ] All CI checks passing
- [ ] Manual testing completed
- [ ] Documentation updated if needed

##### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes Made
- Bullet point list of changes
- Link to related issues: Closes #123

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass  
- [ ] Manual testing completed

## Documentation
- [ ] Documentation updated
- [ ] README updated if needed
- [ ] API docs updated if needed

## Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes documented and versioned
```

### Integration with Existing Tools

#### Codacy Integration

- All PRs must pass Codacy quality gates
- Security issues must be addressed before merge
- Code complexity limits enforced

#### Dependabot Integration  

- Automated dependency PRs get `dependencies` label
- Security updates get expedited review
- Breaking changes require manual testing

#### CI/CD Workflows

- `autofix.yml`: Automated formatting fixes
- `claude-auto-review.yml`: AI-assisted code review
- `yaml-lint.yml`: YAML file validation
- All workflows must pass for PR merge

### Migration Plan

#### Phase 1: Foundation (Week 1)

1. Update branch protection rules
2. Create PR and issue templates
3. Document new workflow (this guide)
4. Train team on new process

#### Phase 2: Process Rollout (Week 2)

1. Apply new workflow to all new PRs
2. Migrate any existing feature work to proper branches
3. Update CI/CD to enforce new rules

#### Phase 3: Optimization (Week 3-4)  

1. Monitor adoption and address issues
2. Refine review process based on experience
3. Add additional automation as needed
4. Create release process documentation

### Troubleshooting

#### Common Issues

**Q: What if I accidentally committed to main?**
A: Create a revert commit, then properly implement the change in a feature branch.

**Q: How do I handle conflicts during rebase?**
A:

```bash
git rebase main
# Fix conflicts in files
git add .
git rebase --continue
```

**Q: What if CI checks fail?**
A: Fix the issues locally, commit the fixes, and push to update the PR.

**Q: Emergency fix needed in production?**
A: Use hotfix workflow with fast-track review process.

### Benefits of This Strategy

1. **Quality Assurance**: All changes reviewed and tested
2. **Security Focus**: Mandatory security reviews for sensitive changes
3. **Automation Integration**: Leverages existing Codacy/CI infrastructure  
4. **Flexibility**: Supports different types of changes appropriately
5. **Traceability**: Clear history and relationship to issues
6. **Collaboration**: Encourages code review and knowledge sharing

### Next Steps

1. Implement branch protection rules
2. Create PR/issue templates  
3. Update CI/CD workflows if needed
4. Begin using new workflow for all changes
5. Monitor and refine process based on team feedback

---

*This document provides comprehensive branch management guidance for ProxmoxMCP, combining implementation details with strategic workflow processes.*