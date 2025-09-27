# 🎯 Ghost Hunter - Operation Nightfall

**Automated DeFi Vulnerability Scanner & Bug Bounty Hunter**

Prize Wallet: `0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C`

## 🚀 Quick Start

### Local Execution
```bash
# Install dependencies
pip install slither-analyzer

# Run scan on target repository
python hunter.py https://github.com/target/defi-project
```

### GitHub Actions (Recommended)
1. Fork this repository
2. Go to **Actions** tab
3. Select **"Ghost Hunter Workflow"**
4. Click **"Run workflow"**
5. Enter target GitHub URL
6. Download the **"Slither-Report"** artifact

## 🎭 Operation Phases

### Phase 2: Weaponization ✅
- [x] `hunter.py` - Core vulnerability scanner
- [x] `hunt.yml` - GitHub Actions automation
- [x] Slither integration with comprehensive analysis
- [x] Automated report generation

## 🔬 Technical Specifications

### Scanner Features
- **Target Validation**: GitHub URL verification
- **Repository Cloning**: Automated git operations
- **Static Analysis**: Slither-powered vulnerability detection
- **Report Generation**: Structured vulnerability reports
- **Cleanup**: Automatic temporary file management

### Vulnerability Detection
- Reentrancy attacks
- Oracle manipulation
- Integer overflows/underflows
- Access control issues
- Logic errors

### Automation Features
- Manual workflow dispatch
- Artifact upload for reports
- Comprehensive logging
- Error handling and recovery

## 🎯 Usage Examples

### Command Line
```bash
# Scan a Uniswap V2 fork
python hunter.py https://github.com/newproject/uniswap-v2-fork

# Scan a Compound fork
python hunter.py https://github.com/defiproject/compound-fork

# Scan an OlympusDAO fork
python hunter.py https://github.com/rebasecoin/olympus-fork
```

### GitHub Actions Workflow
1. Navigate to repository Actions
2. Select "Ghost Hunter Workflow"
3. Input target URL: `https://github.com/target/project`
4. Execute workflow
5. Download report from artifacts

## 📋 Report Structure

Generated reports include:
- Target repository information
- Slither analysis output
- Vulnerability summaries
- Exploitation confidence ratings
- Prize wallet information

## ⚠️ Operational Security

- Zero-API dependency design
- Open-source toolchain only
- Temporary file cleanup
- No sensitive data persistence
- Automated artifact management

## 🏆 Prize Wallet

All successful vulnerability discoveries should direct bounties to:
```
0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C
```

---

**Operation Nightfall - Phase 2 Complete**  
*Ghost Hunter Ready for Deployment*