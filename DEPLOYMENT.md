# Deployment Guide - SS7 Termux Tools 🚀

## Production Deployment

This guide covers deploying SS7 Termux Tools to production.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deployment Steps](#deployment-steps)
3. [Verification](#verification)
4. [Post-Deployment](#post-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Rollback](#rollback)

## Pre-Deployment Checklist

### Code Quality

- [ ] All modules tested locally
- [ ] No debug code in production
- [ ] All error handling in place
- [ ] Logging configured correctly

### Security

- [ ] No hardcoded credentials
- [ ] Input validation complete
- [ ] Error messages don't leak info
- [ ] Logging doesn't contain secrets

### Documentation

- [ ] README up to date
- [ ] Installation guide complete
- [ ] Examples provided
- [ ] Troubleshooting guide included

### Testing

- [ ] Tested on Termux
- [ ] All commands work
- [ ] Error handling tested

## Deployment Steps

### Step 1: Create Release Branch

```bash
git checkout main
git pull origin main
git checkout -b release/v0.1.0
```

### Step 2: Update Version

Edit `src/__init__.py` and `src/main.py`:

```python
__version__ = "0.1.0"
```

### Step 3: Create CHANGELOG Entry

```markdown
# Changelog

## [0.1.0] - 2026-07-01

### Added
- Initial release
- SS7 network scanner
- Protocol parser
- Vulnerability detection
```

### Step 4: Commit Changes

```bash
git add -A
git commit -m "Release v0.1.0: Initial production release"
```

### Step 5: Create Pull Request

```bash
git push origin release/v0.1.0
```

Create PR from `release/v0.1.0` to `main`

### Step 6: Code Review

- [ ] Maintainer review
- [ ] Security review
- [ ] Documentation review

### Step 7: Merge to Main

```bash
git checkout main
git merge release/v0.1.0
git push origin main
```

### Step 8: Create GitHub Release

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## Verification

### Installation Verification

```bash
git clone https://github.com/Mar140-tech/ss7-termux-tools.git
cd ss7-termux-tools
git checkout v0.1.0

chmod +x setup.sh
./setup.sh

bash scripts/check_env.sh
python3 src/main.py version
```

### Functionality Verification

```bash
# Test scan
python3 src/main.py scan --target 127.0.0.1 -o test_scan.json

# Test vulnerability detection
python3 src/main.py detect-vuln --report -o test_report.json

# Test config
python3 src/main.py config --show
python3 src/main.py config --check
```

## Post-Deployment

### Monitoring

```bash
# Monitor logs
tail -f logs/ss7_tools_*.log

# Check for errors
grep ERROR logs/ss7_tools_*.log
```

### User Communication

Announce release:
- GitHub Issues/Discussions
- Email to users
- Social media if applicable

### Support

- [ ] Monitor GitHub issues
- [ ] Respond to questions
- [ ] Track bug reports

## Troubleshooting

### Installation Issues

**Problem:** Package installation fails

```bash
pkg update && pkg upgrade -y
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Problem:** Permission denied

```bash
chmod +x setup.sh scripts/*.sh src/main.py
```

### Runtime Issues

**Problem:** Module not found

```bash
bash scripts/check_env.sh
pip install -r requirements.txt
```

**Problem:** Connection timeout

Increase timeout in `config/config.json`:
```json
{"network": {"timeout": 60}}
```

## Rollback

### If Issues Occur

```bash
git checkout v0.0.1
./setup.sh
```

Notify users about rollback.

## Maintenance

### Regular Updates

- Check dependency updates: `pip list --outdated`
- Review security advisories
- Update documentation
- Release patches for bugs

### Performance Monitoring

```bash
# Check size
du -sh .

# Check logs for errors
grep -c ERROR logs/ss7_tools_*.log
```

---

**For questions, open a GitHub issue.**
