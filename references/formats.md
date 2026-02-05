# Protext Format Specifications

Complete format specifications for all protext files.

## Table of Contents

1. [PROTEXT.md](#protextmd)
2. [.protext/index.yaml](#protextindexyaml)
3. [.protext/handoff.md](#protexthandoffmd)
4. [.protext/config.yaml](#protextconfigyaml)
5. [Scope Files](#scope-files)

---

## PROTEXT.md

The orientation layer. Target: ~500 tokens.

### Template

```markdown
# Protext: [Project Name]
> Generated: YYYY-MM-DD | Scope: [active-scope] | Tokens: ~XXX

## Identity
[1-2 sentences describing what this project/system is and its purpose.]

## Current State
Active: [current work] | Blocked: [blockers or "None"] | Recent: [last completed]

## Hot Context
- [Critical point 1 - what matters RIGHT NOW]
- [Critical point 2]
- [Critical point 3]
- [Critical point 4 - optional]
- [Critical point 5 - optional]

## Scope Signals
- `@ops` → .protext/scopes/ops.md
- `@dev` → .protext/scopes/dev.md
- `@security` → .protext/scopes/security.md
- `@deep:[name]` → Extract from .protext/index.yaml

## Handoff
Last: [summary of last session] | Next: [suggested next steps] | Caution: [warnings]
```

### Field Guidelines

| Field | Max Length | Purpose |
|-------|-----------|---------|
| Project Name | 50 chars | Project identifier |
| Identity | 200 chars | What is this? |
| Current State | 150 chars | Active/Blocked/Recent status |
| Hot Context | 5 items, 80 chars each | Critical current context |
| Scope Signals | 5 entries | Links to scope files |
| Handoff | 200 chars | Session continuity |

### Example (Homelab)

```markdown
# Protext: Cooperator Node
> Generated: 2026-02-05 | Scope: ops | Tokens: ~380

## Identity
Edge services and ingress node for Raspberry Pi cluster. Runs Caddy reverse proxy, Pi-hole DNS, and Headscale VPN.

## Current State
Active: Caddy TLS config | Blocked: None | Recent: Pi-hole v6 migration

## Hot Context
- Caddy config at /etc/caddy/Caddyfile - validate before reload
- Pi-hole admin: https://dns.ism.la (Port 8080)
- All secrets via Infisical - never hardcode
- Split-horizon DNS: LAN uses 192.168.254.10, mesh uses 100.64.0.1

## Scope Signals
- `@ops` → .protext/scopes/ops.md
- `@security` → .protext/scopes/security.md
- `@deep:network` → docs/NETWORK.md
- `@deep:services` → docs/SERVICES.md

## Handoff
Last: Completed Pi-hole v6 upgrade | Next: Test wildcard certs | Caution: Port 8080 in use
```

---

## .protext/index.yaml

Extraction index for deep context. Max 20 entries.

### Schema

```yaml
# Required header
# Protext Extraction Index

extractions:
  [name]:                    # Unique identifier (lowercase, hyphens ok)
    source: [path]           # Path relative to project root
    triggers: [list]         # Keywords that suggest this extraction
    summary: "[description]" # One-line description
    tokens: ~[estimate]      # Approximate token count
```

### Example

```yaml
# Protext Extraction Index
# Max 20 extractions. Use suggest-mode by default.

extractions:
  network:
    source: docs/NETWORK.md
    triggers: [dns, ip, tailscale, mesh, routing, headscale]
    summary: "IPs, DNS configuration, mesh nodes, domain routing"
    tokens: ~600

  services:
    source: docs/SERVICES.md
    triggers: [docker, container, service, port, compose, caddy]
    summary: "Docker services, ports, domains, health checks"
    tokens: ~800

  secrets:
    source: docs/SECRETS.md
    triggers: [secret, credential, infisical, auth, password, api-key]
    summary: "Secrets management patterns, Infisical usage"
    tokens: ~400

  architecture:
    source: docs/ARCHITECTURE.md
    triggers: [design, diagram, pattern, cluster, nodes]
    summary: "System architecture, node relationships, data flow"
    tokens: ~500

  router:
    source: docs/ROUTER.md
    triggers: [mikrotik, gateway, dhcp, firewall, port-forward, nat]
    summary: "MikroTik router configuration, port forwarding"
    tokens: ~450
```

### Trigger Guidelines

- Use 3-6 triggers per extraction
- Include synonyms and common misspellings
- Prefer lowercase
- Triggers are hints, not exact matches

---

## .protext/handoff.md

Session continuity. Auto-stales after 48h.

### Template

```markdown
# Session Handoff
> Updated: YYYY-MM-DDTHH:MM | TTL: 48h | Status: FRESH|AGING|STALE

## Last Session
**Completed:**
- [Task 1 that was finished]
- [Task 2 that was finished]

**In Progress:**
- [Task] (stopped at: [specific point])

**Deferred:**
- [Task] (blocked by: [reason])

## Cautions
- [Warning 1 for next session]
- [Warning 2]

## Agent Notes
[Observations, insights, or context that might help the next session]
```

### Status Definitions

| Status | Age | Meaning |
|--------|-----|---------|
| FRESH | < 24h | Handoff is current, trust fully |
| AGING | 24-48h | Handoff is getting old, verify critical items |
| STALE | > 48h | Handoff may be outdated, suggest refresh |

### Example

```markdown
# Session Handoff
> Updated: 2026-02-05T14:30 | TTL: 48h | Status: FRESH

## Last Session
**Completed:**
- Migrated Pi-hole to v6
- Updated split-horizon DNS config
- Tested local resolution

**In Progress:**
- Caddy wildcard cert setup (stopped at: DNS challenge config)

**Deferred:**
- Headscale ACL audit (blocked by: need drtr node online)

## Cautions
- Don't restart Caddy without validating config first
- Port 8080 temporarily used by debug server
- Pi-hole gravity update scheduled for 3am

## Agent Notes
The DNS migration went smoother than expected. Consider documenting the
split-horizon pattern for future reference. The wildcard cert requires
Cloudflare API token - check Infisical under /caddy/cloudflare.
```

---

## .protext/config.yaml

Protext configuration.

### Template

```yaml
# Protext Configuration

# Extraction behavior
extraction_mode: suggest  # suggest | auto | confirm
token_budget: 2000        # Max tokens per session

# Handoff settings
handoff_ttl_hours: 48     # TTL before staleness warning

# Active scope
active_scope: ops         # Current focus area

# Feature flags
features:
  auto_handoff_capture: true   # Prompt for handoff at session end
  token_warnings: true         # Warn at 80% budget
  scope_switching: true        # Enable @scope shortcuts
```

### Extraction Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `suggest` | Show available extractions, don't auto-load | Default, token-conscious |
| `auto` | Load on keyword trigger | Fast iteration, higher token use |
| `confirm` | Require user approval for each load | Maximum control |

---

## Scope Files

Domain-specific orientation. Location: `.protext/scopes/[name].md`

### Template

```markdown
# Scope: [Name]

## Focus
[1-2 sentences describing what this scope covers]

## Key Resources
- [Path or resource 1]
- [Path or resource 2]
- [Path or resource 3]

## Current Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Patterns
[Common patterns or conventions for this scope]

## Cautions
- [Scope-specific warning 1]
- [Scope-specific warning 2]
```

### Default Scopes

**ops.md** - Operations
```markdown
# Scope: Operations

## Focus
Infrastructure management, service health, deployment, monitoring.

## Key Resources
- Docker services: /mnt/ops/docker/
- Caddy config: /etc/caddy/Caddyfile
- System logs: journalctl

## Current Priorities
1. Service availability
2. Resource monitoring
3. Backup verification

## Patterns
- Always validate configs before applying
- Check logs after service restarts
- Document infrastructure changes

## Cautions
- Never restart services without checking dependencies
- Verify backup status before major changes
```

**dev.md** - Development
```markdown
# Scope: Development

## Focus
Code development, testing, debugging, workflow optimization.

## Key Resources
- Source code: /mnt/ops/
- Tests: Run with pytest or relevant test runner
- Linting: Pre-commit hooks configured

## Current Priorities
1. Code quality
2. Test coverage
3. Documentation updates

## Patterns
- Write tests for new functionality
- Use conventional commits
- Review before merge

## Cautions
- Don't commit secrets
- Run tests before pushing
```

**security.md** - Security
```markdown
# Scope: Security

## Focus
Authentication, secrets management, vulnerability assessment, access control.

## Key Resources
- Secrets: Infisical (https://env.ism.la)
- Auth patterns: docs/SECRETS.md
- ACLs: Headscale policies

## Current Priorities
1. Secret rotation schedule
2. Access review
3. Vulnerability scanning

## Patterns
- All secrets via Infisical CLI
- Never log sensitive data
- Principle of least privilege

## Cautions
- Never hardcode credentials
- Review before exposing new services
- Audit access logs regularly
```

---

## File Size Guidelines

| File | Target Size | Max Size |
|------|-------------|----------|
| PROTEXT.md | ~500 tokens | 800 tokens |
| index.yaml | ~200 lines | 300 lines |
| handoff.md | ~300 tokens | 500 tokens |
| config.yaml | ~50 lines | 100 lines |
| Scope files | ~200 tokens each | 400 tokens |

Keep total protext overhead under 2000 tokens for efficient context loading.
