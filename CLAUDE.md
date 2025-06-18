# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Additional Instructions

- memory workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/memory-instructions.md (not supported in Codex)
- context workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/context-instructions.md
- github workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/github-instructions.md
- issue creation workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/issue-creation-instructions.md
- issue resolution workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/issue-resolution-instructions.md
- pr workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/pr-instructions.md
- milestone workflow @/workspaces/ProxmoxMCP/docs/ai-instructions/milestone-instructions.md

## Development Commands

### Environment Setup

```bash
# Set up git configuration (recommended for development)
cp example.gitconfig .git/config
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies with development tools
uv pip install -e ".[dev]"
```

### Testing and Quality Assurance

```bash
# Run tests
pytest

# Format code
black .

# Type checking
mypy .

# Lint code
ruff .

# Run all quality checks sequentially
pytest && black . && mypy . && ruff .

# Full quality checks including dependency validation
pytest && black . && mypy . && ruff . && uv pip check
```

### Dependency Management and Version Verification

Before modifying dependencies in `pyproject.toml`, `requirements.in`, or `requirements-dev.in`, ALWAYS verify actual package versions to prevent uninstallable packages:

#### Version Research Commands

```bash
# Research PyPI package versions
pip index versions <package-name>
pip show <package-name>  # For currently installed packages

# Alternative research methods
uv pip show <package-name>  # If using uv
python -m pip install <package-name>==nonexistent 2>&1 | grep "from versions"

# Check package compatibility with Python versions
python -c "import sys; print(sys.version_info)"
pip install --dry-run <package-name>==<version>
```

#### GitHub Release Verification

```bash
# For packages sourced from GitHub (like MCP SDK)
gh release list --repo modelcontextprotocol/python-sdk
gh release view <tag> --repo modelcontextprotocol/python-sdk

# Check specific commit or branch availability
gh api repos/modelcontextprotocol/python-sdk/commits/<commit-hash>
gh api repos/modelcontextprotocol/python-sdk/branches/<branch-name>
```

#### Version Constraint Best Practices

Use these patterns when setting dependency versions:

```bash
# Recommended constraint patterns for ProxmoxMCP:

# Core runtime dependencies - conservative ranges
"pydantic>=2.0.0,<3.0.0"      # Major version boundary
"requests>=2.32.0,<3.0.0"      # Security-conscious minimum

# Development tools - broader ranges for flexibility
"pytest>=7.0.0,<9.0.0"        # Allow multiple major versions
"black>=23.0.0,<26.0.0"       # Formatting tool compatibility

# Security-critical packages - narrower ranges  
"cryptography>=45.0.0,<46.0.0" # Strict for security updates

# Git dependencies - use specific tags/commits
"mcp @ git+https://github.com/modelcontextprotocol/python-sdk.git@v1.0.0"
```

#### Dependency Validation Workflow

Before committing dependency changes:

```bash
# 1. Research actual versions available
pip index versions pydantic
pip index versions cryptography
pip index versions pytest

# 2. Test installation in clean environment
uv venv test-deps
source test-deps/bin/activate
uv pip install -e ".[dev]"  # Test all dependencies resolve

# 3. Validate constraint logic
python -c "
import pkg_resources
try:
    pkg_resources.require(['pydantic>=2.0.0,<3.0.0'])
    print('✓ Pydantic constraint valid')
except:
    print('✗ Pydantic constraint invalid')
"

# 4. Check for known vulnerabilities
pip audit  # If available
safety check  # Alternative security scanner

# 5. Clean up test environment
deactivate
rm -rf test-deps
```

#### Dependency Update Process

When updating dependencies:

```bash
# 1. Check current versions
uv pip list --outdated

# 2. Research latest versions and compatibility
pip index versions <package-name>

# 3. Update constraints based on research
# Edit pyproject.toml, requirements.in, or requirements-dev.in

# 4. Regenerate lock files if using uv
uv pip compile requirements.in -o requirements.txt
uv pip compile requirements-dev.in -o requirements-dev.txt

# 5. Test installation and functionality
uv venv fresh-test
source fresh-test/bin/activate
uv pip install -e ".[dev]"
pytest  # Verify functionality
deactivate && rm -rf fresh-test

# 6. Document breaking changes in commit message
git add .
git commit -m "deps: update pydantic to 2.x.x

- Verify compatibility with Python 3.10+
- Test all MCP tool functionality
- Update type annotations as needed

Closes #issue-number"
```

#### Common Version Constraint Mistakes to Avoid

```bash
# ❌ WRONG: Unverified constraints that may not exist
"pydantic>=99.0.0,<100.0.0"  # Version 99.x.x doesn't exist

# ❌ WRONG: Overly restrictive constraints
"requests==2.32.0"  # Pins to exact version, prevents security updates

# ❌ WRONG: Conflicting constraints
"black>=24.0.0,<25.0.0"  # When 24.x.x was never released

# ❌ WRONG: Missing upper bounds for major versions
"pydantic>=2.0.0"  # Could install v3.x.x with breaking changes

# ✅ CORRECT: Research-verified constraints
"pydantic>=2.0.0,<3.0.0"    # Verified that 2.x.x exists
"requests>=2.32.0,<3.0.0"   # Allows security updates within v2.x
"black>=23.0.0,<26.0.0"     # Verified version range exists
```

#### ProxmoxMCP-Specific Dependency Considerations

```bash
# MCP SDK - use specific tagged releases
# Research: gh release list --repo modelcontextprotocol/python-sdk
"mcp @ git+https://github.com/modelcontextprotocol/python-sdk.git@v1.0.0"

# Proxmoxer - check compatibility with Proxmox VE API versions
# Research API changes between versions
"proxmoxer>=2.0.1,<3.0.0"

# Cryptography - security-critical, use narrow ranges
# Research: pip index versions cryptography
"cryptography>=45.0.0,<46.0.0"

# FastMCP or MCP dependencies - verify protocol compatibility
# Check MCP protocol version requirements
```

### Running the Server

```bash
# Set config path and run server
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
python -m proxmox_mcp.server

# Or with Docker
docker compose up --build
```

### Configuration Setup

```bash
# Create config directory and copy template
mkdir -p proxmox-config
cp proxmox-config/config.example.json proxmox-config/config.json
# Edit config.json with your Proxmox credentials
```

## Architecture Overview

### Core Components

- **server.py**: Main MCP server implementation using FastMCP, handles tool registration and request routing
- **core/proxmox.py**: ProxmoxManager class that manages API connections and authentication
- **config/**: Configuration loading and validation using Pydantic models
- **tools/**: Individual tool implementations (node, VM, storage, cluster operations)
- **formatting/**: Rich output formatting with themes, colors, and structured display

### Key Design Patterns

- **Tool-based Architecture**: Each Proxmox operation is implemented as a separate MCP tool
- **Pydantic Validation**: All configuration and API parameters use Pydantic models for type safety
- **Centralized Formatting**: All output uses consistent formatting through the formatting module
- **Async Support**: VM command execution supports async operations via QEMU guest agent

### Tool Categories

1. **Node Tools**: `get_nodes`, `get_node_status` - Cluster node management
2. **VM Tools**: `get_vms`, `execute_vm_command` - Virtual machine operations
3. **Storage Tools**: `get_storage` - Storage pool information
4. **Cluster Tools**: `get_cluster_status` - Overall cluster health

### Configuration Requirements

- Requires `PROXMOX_MCP_CONFIG` environment variable pointing to config JSON file
- Config must include Proxmox connection details (host, port, SSL settings) and authentication (user, token_name, token_value)
- Supports both file-based and environment variable configuration

### Authentication

- Uses Proxmox API tokens (not passwords) for secure authentication
- Tokens must have appropriate permissions for the operations being performed
- Connection is tested during server startup

### Output Formatting

- Rich formatted output with emojis, colors, and structured layout
- Consistent formatting across all tools using theme system
- Human-readable resource usage (bytes, percentages, uptime)

## Important Implementation Notes

### VM Command Execution

- Requires QEMU Guest Agent to be installed and running in target VMs
- Commands execute asynchronously and return both stdout and stderr
- Returns proper exit codes and handles command failures gracefully

### Error Handling

- Connection failures during startup cause server to exit with detailed error messages
- API operation failures are caught and returned as formatted error responses
- SSL verification can be disabled for self-signed certificates via config

### Testing

- Uses pytest with async support for testing MCP operations
- Test configuration should use mock Proxmox API to avoid requiring live server
- Tests are located in `tests/` directory

### Dependencies

- Built on Model Context Protocol (MCP) SDK for tool interface
- Uses `proxmoxer` library for Proxmox API communication
- Requires Python 3.10+ with modern async/await support

#### Dependency Version Management

All dependency versions MUST be verified before setting constraints:

1. **Research actual versions** using `pip index versions <package>` or GitHub releases
2. **Test constraints** in clean environments before committing
3. **Use appropriate constraint patterns** based on package type and stability
4. **Validate installation** using `uv pip check` and functionality tests
5. **Document breaking changes** when updating major versions

See the "Dependency Management and Version Verification" section above for detailed procedures.

## Repository Hygiene and Maintenance

### Overview

Repository hygiene involves proactive maintenance procedures to prevent accumulation of stale references, outdated analysis, and technical debt. These procedures should be integrated into regular development workflows to ensure repository health and accuracy.

### Pre-Work Hygiene Procedures

Before starting any development task, perform these validation steps:

```bash
# Validate current branch state and clean workspace
git status && git fetch origin && git log --oneline -5

# Check for stale analysis files and outdated references
find .claude/reports -name "*.md" -type f -mtime +30 -ls
find docs/ -name "*.md" -type f -exec grep -l "TODO\|FIXME\|outdated" {} \;

# Verify configuration and dependency consistency
python -c "from proxmox_mcp.config.loader import load_config; load_config()" 2>/dev/null || echo "Config validation failed"
```

### Regular Maintenance Schedule

#### Daily (During Active Development)
- **Memory Updates**: Capture new learnings and patterns immediately after completing tasks
- **Branch Cleanup**: Remove merged feature branches and stale references
- **Issue Synchronization**: Update issue status and remove stale labels

```bash
# Daily branch cleanup
git branch --merged main | grep -v main | xargs -n 1 git branch -d
git remote prune origin

# Validate current memory state alignment
get_all_coding_preferences # Review for outdated patterns
```

#### Weekly Maintenance
- **Analysis Validation**: Review and update repository analysis against current state
- **Documentation Accuracy**: Verify instruction files reflect current codebase structure
- **Dependency Updates**: Check for security updates and compatibility issues

```bash
# Weekly maintenance routine
pytest && black . && mypy . && ruff .
uv pip list --outdated
docker system prune -f
```

#### Monthly Deep Cleaning
- **Comprehensive Memory Audit**: Review all stored coding preferences for accuracy
- **Architecture Documentation**: Update component descriptions and design patterns
- **Security Review**: Validate security practices and credential management

### Memory Management Hygiene

#### When to Capture New Learnings
Immediately capture patterns in these scenarios:
- **After resolving complex technical issues** - Document solution approach and decision rationale
- **When implementing new architectural patterns** - Store complete implementation context
- **Following security implementations** - Capture security best practices and validation methods
- **After performance optimizations** - Document performance patterns and measurement approaches
- **When discovering integration patterns** - Store MCP protocol and Proxmox API integration insights

#### Memory Update Timing
```python
# Capture immediately after significant implementations
add_coding_preference(
    content="""
    ProxmoxMCP Tool Implementation Pattern:
    - Inherit from ProxmoxTool base class
    - Use Pydantic models for validation
    - Implement rich formatting via ProxmoxTheme
    - Add comprehensive error handling
    - Include tool registration in definitions.py
    """,
    context="Complete implementation with dependencies and examples"
)
```

### Analysis Accuracy Validation

#### Pre-Task Validation
Before starting any analysis or implementation:
1. **Current State Verification**: Use LS, Glob, and Grep tools to verify actual codebase structure
2. **Reference Validation**: Check that all file references and paths are current and accurate
3. **Component Status**: Verify component descriptions match actual implementation state
4. **Integration Points**: Validate that described integration patterns still exist and function

#### Post-Task Validation
After completing implementation work:
1. **Architecture Alignment**: Verify changes align with documented architectural patterns
2. **Reference Updates**: Update any documentation that references modified components
3. **Integration Consistency**: Ensure new implementations follow established integration patterns

### Repository Health Metrics

#### Key Health Indicators
- **Test Coverage**: Maintain >90% coverage for core components
- **Code Quality**: Zero mypy errors, consistent black formatting
- **Documentation Currency**: No references to non-existent files or outdated patterns
- **Memory Accuracy**: Stored coding preferences reflect current implementation patterns
- **Security Posture**: No exposed secrets, current security practices documented

## Memories

- "When tasked are completed you must commit changes to github"
- When submitting PR reviews with complex text containing special shell characters, it's better to:
  1. Use simpler review text, or
  2. Escape special characters properly, or
  3. Submit reviews through the GitHub web interface for complex formatting
- ALWAYS verify package versions exist before setting dependency constraints using `pip index versions <package>` or GitHub releases to prevent uninstallable packages
- ALWAYS treat GitHub API as authoritative source for repository state; verify branch existence before analysis
- Perform stale branch cleanup before any repository analysis to ensure accuracy
