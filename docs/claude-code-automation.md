# Claude Code Automation

This repository is configured to work with Claude Code automation for issue resolution. When you assign an issue to Claude Code, it will automatically create a branch, implement the solution, and create a pull request.

## How It Works

### 1. Creating an Issue for Claude Code

Use the "Claude Code Task" issue template or manually:

1. Create a new issue
2. Add the `claude-code` label
3. Assign to `claude-code-bot` (or ensure the label is present)
4. Provide clear requirements and acceptance criteria

### 2. Automatic Process

When an issue is assigned to Claude Code, the automation will:

1. **Create Branch**: Generate a new branch named `claude/issue-{number}-{title}`
2. **Comment**: Add a comment to the issue indicating work has started
3. **Implement**: Analyze requirements and implement the solution
4. **Quality Checks**: Run tests, formatting, and type checking
5. **Commit**: Create meaningful commits with the changes
6. **Pull Request**: Create a PR linking back to the issue

### 3. Review Process

After Claude Code completes the work:

1. Review the generated pull request
2. Check that all requirements are met
3. Run additional tests if needed
4. Merge when satisfied or request changes

## Configuration Requirements

### Repository Secrets

The following secrets must be configured in your repository:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude Code
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### Permissions

The workflow requires the following permissions:
- `contents: write` - To create branches and commits
- `issues: write` - To comment on issues
- `pull-requests: write` - To create pull requests
- `id-token: write` - For authentication

## Issue Template Guidelines

When creating issues for Claude Code, include:

### Clear Task Description
```markdown
## Task Description
Add support for VM snapshot management in the Proxmox MCP server.
```

### Specific Requirements
```markdown
## Requirements
- [ ] Add `create_vm_snapshot` tool
- [ ] Add `delete_vm_snapshot` tool
- [ ] Add `restore_vm_snapshot` tool
- [ ] Include proper error handling
```

### Acceptance Criteria
```markdown
## Acceptance Criteria
- [ ] All tools follow existing patterns in tools/ directory
- [ ] Proper Pydantic models for validation
- [ ] Rich formatted output
- [ ] Tests included
```

### Technical Details
```markdown
## Technical Details
- Use the existing ProxmoxManager pattern
- Follow the formatting standards in formatting/ module
- Add to tools/vm.py or create tools/snapshot.py
```

## Best Practices

### For Issue Creation
- Be specific about requirements
- Provide examples of expected behavior
- Include error cases to handle
- Reference existing code patterns when applicable

### For Review
- Check that the solution follows project conventions
- Verify tests are comprehensive
- Ensure documentation is updated if needed
- Test the implementation manually if possible

## Troubleshooting

### Common Issues

**Workflow doesn't trigger:**
- Ensure the issue has the `claude-code` label
- Check that the assignee is `claude-code-bot` or the label is present
- Verify repository secrets are configured

**Implementation fails:**
- Check the workflow logs for detailed error messages
- Ensure the task description is clear and actionable
- Verify the requirements don't conflict with existing code

**Quality checks fail:**
- The workflow will show which checks failed
- Claude Code will attempt to fix issues automatically
- Manual intervention may be needed for complex conflicts

### Getting Help

If you encounter issues with the automation:

1. Check the GitHub Actions logs for detailed error information
2. Review the issue description for clarity and completeness
3. Ensure all required repository secrets are configured
4. Create a support issue if problems persist

## Example Workflow

1. **Create Issue**: Use the Claude Code Task template
   ```
   Title: [CLAUDE] Add VM backup scheduling feature
   Description: Clear requirements and acceptance criteria
   Labels: claude-code
   Assignee: claude-code-bot
   ```

2. **Automatic Processing**: Claude Code creates branch `claude/issue-123-add-vm-backup-scheduling-feature`

3. **Implementation**: Code is written, tested, and committed

4. **Pull Request**: PR #124 created with link to issue #123

5. **Review**: You review and merge the PR

6. **Completion**: Issue #123 is automatically closed

This automation streamlines the development process while maintaining code quality and project standards.