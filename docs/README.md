# 📚 ProxmoxMCP Documentation

Welcome to the comprehensive documentation for **ProxmoxMCP** - a Python-based Model Context Protocol (MCP) server for managing Proxmox hypervisors.

## 🚀 Quick Start

For installation and basic usage, see the [main README](../README.md).

## 📖 Documentation Structure

### **Getting Started**
- **[Project Roadmap](ROADMAP.md)** - Development roadmap and feature planning
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to the project

### **Architecture & Development**
- **[Repository Review](repository-review.md)** - Comprehensive code analysis and structure
- **[Claude Code Automation](claude-code-automation.md)** - Automated development workflow setup
- **[Memory Instructions](memory-instructions.md)** - AI assistant memory management
- **[Mem0 MCP Integration](mem0mcp.md)** - Memory context protocol integration

### **Security**
- **[Security & Encryption](security-encryption.md)** - Token encryption and security practices

## 🛠️ Development

This project uses modern Python development practices:
- **Python 3.10+** for MCP compatibility
- **FastMCP** for the server framework
- **Pydantic** for data validation
- **Docker** for containerized deployment

## 📋 Configuration

The server requires proper configuration for Proxmox API access. See the configuration examples in the `proxmox-config/` directory.

## 🤖 Automation

This project includes Claude Code automation for issue resolution. When you assign an issue with the `claude-code` label, it automatically:
1. Creates a branch
2. Implements the solution
3. Runs tests and quality checks
4. Creates a pull request

## 🔗 Links

- **[Main Repository](../README.md)** - Project overview and setup
- **[GitHub Issues](https://github.com/basher83/ProxmoxMCP/issues)** - Bug reports and feature requests
- **[Pull Requests](https://github.com/basher83/ProxmoxMCP/pulls)** - Code contributions

---

*This documentation is built with GitBook and automatically synced with the repository.*