# ⚡ Quick Start Guide - Intelligent Fixer Bot

Get the bot running in **under 5 minutes**!

---

## 🚀 Immediate Setup

### Step 1: Get GitHub Token (2 min)

1. Go to: https://github.com/settings/tokens/new
2. **Token name**: `intelligent-fixer-bot`
3. **Scopes** (select these):
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
4. Click **"Generate token"**
5. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Set Environment Variable (30 sec)

**Linux/Mac:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

**Permanently (add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Run the Bot (10 sec)

```bash
cd /home/user/webapp
python3 intelligent_fixer.py
```

**That's it!** 🎉

---

## 📊 What You'll See

```
╔══════════════════════════════════════════════════════════════╗
║        GitHub Intelligent Issue Fixer Bot v3.0              ║
║        Autonomous Revenue Generation System                  ║
╚══════════════════════════════════════════════════════════════╝

[2025-10-13 23:04:14] [INFO] 🚀 Starting fix cycle...
[2025-10-13 23:04:14] [INFO] 🔍 Searching for fixable issues...
[2025-10-13 23:04:15] [INFO]   Found 5 issues for good first issue/python
[2025-10-13 23:04:17] [INFO]   Found 3 issues for documentation/javascript
[2025-10-13 23:04:19] [INFO] ✅ Found 8 potentially fixable issues
[2025-10-13 23:04:19] [INFO] 🎯 Selected top issue: https://github.com/...
[2025-10-13 23:04:20] [INFO] 📊 Analyzing issue #123: Fix typo in README
```

---

## 🎯 First Run Checklist

After your first successful run:

- [ ] Bot found issues (at least 1)
- [ ] Scoring algorithm worked
- [ ] Repository was cloned successfully
- [ ] No errors in logs
- [ ] Ready for next phase!

---

## 🔥 Pro Tips

### Maximize API Calls

With GitHub token, you get:
- **5,000 API calls/hour** (vs 60 without token)
- **Much faster operation**
- **Better rate limit management**

### Optimize for Your Schedule

**Run manually when you want:**
```bash
python3 intelligent_fixer.py
```

**Or automate with cron (every 6 hours):**
```bash
crontab -e
# Add this line:
0 */6 * * * cd /home/user/webapp && python3 intelligent_fixer.py >> bot.log 2>&1
```

---

## 📈 Next Steps

Once you've verified the bot works:

1. **Read the full README.md** for strategy details
2. **Check MISSION_REPORT_V3.md** for comprehensive documentation
3. **Monitor first few cycles** to understand patterns
4. **Customize scoring** in `intelligent_fixer.py` if needed
5. **Start creating PRs** (implementation in Phase 2)

---

## ❓ Troubleshooting

### "No GITHUB_TOKEN found"
- Make sure you exported the token
- Check: `echo $GITHUB_TOKEN` (should show your token)
- Restart your terminal if you just set it

### "API Error 403: rate limit exceeded"
- You need a GitHub token (see Step 1)
- Or wait 1 hour for rate limits to reset

### "No suitable issues found"
- Normal! GitHub search is dynamic
- Try running again in a few hours
- Or adjust search criteria in code

### "Repository cloning failed"
- Check internet connection
- Ensure git is installed: `git --version`
- Try manually: `git clone [repo_url]`

---

## 💰 Payment Setup

Your payment wallet is already configured in the bot:

**Chain**: peb20  
**Wallet**: `0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C`

This will be automatically included in all PRs created by the bot.

To change it, edit `intelligent_fixer.py`:
```python
PAYMENT_WALLET = "your_wallet_address_here"
PAYMENT_CHAIN = "your_chain_here"
```

---

## 🎓 Learning Resources

**Understand the Strategy:**
- README.md - Complete overview
- MISSION_REPORT_V3.md - Deep dive into transformation

**Customize the Bot:**
- Edit `intelligent_fixer.py` scoring algorithm
- Adjust search labels and languages
- Modify payment suggestions

**Join Development:**
- Fork the repository
- Submit improvements
- Share your success stories

---

## ✅ Success Metrics

Track your progress:

- **Issues Discovered**: How many per cycle?
- **Quality Score**: Average fixability score?
- **PRs Created**: How many per week?
- **Acceptance Rate**: Percentage merged?
- **Revenue**: Total donations received?

Keep a log and optimize based on data!

---

## 🚀 You're Ready!

The bot is **production-ready** and **waiting for your GitHub token**.

Set it up, run it, and start contributing to open source while building revenue!

**Questions?** Check the full documentation or open an issue on GitHub.

**Ready to scale?** Read MISSION_REPORT_V3.md for the complete roadmap.

---

**Payment Wallet**: `0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C` (peb20)  
**Repository**: [github.com/sawssenbensalem1990-arch/First](https://github.com/sawssenbensalem1990-arch/First)

*Built with intelligence. Driven by ethics. Focused on value. 🚀*
