# Project Credentials & Environment Configuration (Template)

> [!CAUTION]
> **CRITICAL SECURITY RULE:** Never commit actual passwords, private keys, API secrets, or production credentials to this file or any file tracked by Git. This file is an example structure template only.

---

## 1. Test & Development Environments

| Environment | Purpose | URL / Endpoint | Access Method |
| :--- | :--- | :--- | :--- |
| **Local Dev** | Component testing & Storybook | `http://localhost:6006` | Public / Localhost |
| **Staging Portal** | Preview documentation & UI test builds | `https://staging-design.example.com` | Protected via Basic Auth or VPN |
| **Flutter Testbed** | Mobile/Tablet sandbox | Local Emulator / Simulator | Dart Tooling Daemon |

---

## 2. Environment Variables Specification (`.env.example`)

To configure tooling and deployment pipelines, copy this template to `.env.local` (which must be ignored in `.gitignore`):

```bash
# ==========================================
# MDS Tooling & Build Pipeline Configuration
# ==========================================

# Node & Package Registry
NODE_ENV=development
NPM_REGISTRY_TOKEN=your_npm_token_here

# GitHub MCP & CI/CD Access
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_example_token_here
GITHUB_REPO_OWNER=your_github_username
GITHUB_MAIN_REPO=master-design-system

# Testing & Cloud Inspection
CHROME_DEVTOOLS_PORT=9222
STORYBOOK_PORT=6006
```

---

## 3. Test Accounts (Dummy & Sandbox Only)

For testing role-based component behaviors (Admin, Editor, Viewer):

| Role | Test Username / Email | Mock Permissions |
| :--- | :--- | :--- |
| **Admin** | `admin@mds-sandbox.local` | Full system governance, token creation |
| **Editor** | `editor@mds-sandbox.local` | Component editing, preset selection |
| **Viewer** | `viewer@mds-sandbox.local` | Read-only documentation inspection |
