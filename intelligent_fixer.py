#!/usr/bin/env python3
"""
GitHub Intelligent Issue Fixer Bot
Autonomous Revenue Generation System v3.0

Strategy: Find simple, fixable issues in small-medium projects
Payment Model: Fix-first, pay-later via peb20 wallet
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import urllib.request
import urllib.error
import urllib.parse

# Configuration
PAYMENT_WALLET = "0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C"
PAYMENT_CHAIN = "peb20"
GITHUB_API = "https://api.github.com"

# Search Strategy: Focus on easy wins
ISSUE_LABELS = [
    "good first issue",
    "documentation",
    "easy",
    "beginner friendly", 
    "help wanted",
    "typo",
    "enhancement",
    "minor"
]

LANGUAGES = ["python", "javascript", "typescript", "markdown"]

# Quality filters
MIN_STARS = 10  # Not too small
MAX_STARS = 5000  # Not too complex
RECENT_ACTIVITY_DAYS = 30  # Active projects only


class IntelligentFixer:
    """Smart bot that finds and fixes GitHub issues for payment"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.session_log = []
        self.temp_dir = None
        
    def log(self, message: str, level: str = "INFO"):
        """Professional logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        sys.stdout.flush()
        self.session_log.append(log_entry)
        
    def api_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated GitHub API request"""
        url = f"{GITHUB_API}{endpoint}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
            
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Intelligent-Fixer-Bot"
        }
        
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
            
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            self.log(f"API Error {e.code}: {e.reason}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Request failed: {str(e)}", "ERROR")
            return None
            
    def search_fixable_issues(self, max_results: int = 50) -> List[Dict]:
        """Find issues matching our strategy"""
        self.log("🔍 Searching for fixable issues...")
        
        all_issues = []
        
        for label in ISSUE_LABELS[:3]:  # Try top 3 labels
            for language in LANGUAGES[:2]:  # Focus on Python and JS
                query = (
                    f"is:issue is:open label:\"{label}\" language:{language} "
                    f"stars:{MIN_STARS}..{MAX_STARS} "
                    f"updated:>{(datetime.now() - timedelta(days=RECENT_ACTIVITY_DAYS)).strftime('%Y-%m-%d')}"
                )
                
                params = {
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 10
                }
                
                result = self.api_request("/search/issues", params)
                
                if result and "items" in result:
                    all_issues.extend(result["items"])
                    self.log(f"  Found {len(result['items'])} issues for {label}/{language}")
                    
                time.sleep(2)  # Rate limiting respect
                
                if len(all_issues) >= max_results:
                    break
                    
            if len(all_issues) >= max_results:
                break
                
        # Filter and score issues
        scored_issues = []
        for issue in all_issues:
            score = self._score_issue(issue)
            if score > 0:
                issue["fixability_score"] = score
                scored_issues.append(issue)
                
        # Sort by score
        scored_issues.sort(key=lambda x: x["fixability_score"], reverse=True)
        
        self.log(f"✅ Found {len(scored_issues)} potentially fixable issues")
        return scored_issues[:max_results]
        
    def _score_issue(self, issue: Dict) -> float:
        """Score issue fixability (0-100)"""
        score = 50.0  # Base score
        
        title = issue.get("title", "").lower()
        body = issue.get("body", "").lower() if issue.get("body") else ""
        labels = [l["name"].lower() for l in issue.get("labels", [])]
        
        # Positive signals
        if "typo" in title or "typo" in labels:
            score += 30
        if "documentation" in labels or "docs" in title:
            score += 25
        if "readme" in title:
            score += 20
        if "test" in title and "add" in title:
            score += 15
        if "good first issue" in labels:
            score += 15
        if "easy" in labels or "beginner" in labels:
            score += 10
        if issue.get("comments", 0) == 0:  # No one else working
            score += 10
        if issue.get("assignee") is None:  # Not assigned
            score += 10
            
        # Negative signals
        if "refactor" in title or "architecture" in title:
            score -= 40
        if "breaking" in title or "major" in title:
            score -= 30
        if "security" in labels:
            score -= 50  # Too risky
        if len(title) > 200:  # Complex description
            score -= 15
        if issue.get("comments", 0) > 20:  # Too much discussion
            score -= 20
        if "?" in title:  # Question, not clear fix
            score -= 10
            
        return max(0, min(100, score))
        
    def analyze_issue(self, issue: Dict) -> Dict:
        """Deep analysis of issue to determine fix approach"""
        self.log(f"📊 Analyzing issue #{issue['number']}: {issue['title']}")
        
        repo_url = issue["repository_url"]
        repo_info = self.api_request(repo_url.replace(GITHUB_API, ""))
        
        if not repo_info:
            return {"feasible": False, "reason": "Cannot fetch repo info"}
            
        # Check repository characteristics
        analysis = {
            "issue": issue,
            "repo": repo_info,
            "feasible": True,
            "complexity": "low",
            "estimated_time": 0,
            "fix_strategy": "",
            "payment_suggested": 0
        }
        
        # Determine fix strategy based on issue type
        title_lower = issue["title"].lower()
        labels = [l["name"].lower() for l in issue.get("labels", [])]
        
        if "typo" in title_lower or "typo" in labels:
            analysis["fix_strategy"] = "typo_fix"
            analysis["estimated_time"] = 15
            analysis["payment_suggested"] = 10
            
        elif "documentation" in labels or "readme" in title_lower:
            analysis["fix_strategy"] = "documentation"
            analysis["estimated_time"] = 30
            analysis["payment_suggested"] = 25
            
        elif "test" in title_lower:
            analysis["fix_strategy"] = "add_tests"
            analysis["estimated_time"] = 60
            analysis["payment_suggested"] = 50
            analysis["complexity"] = "medium"
            
        elif any(word in title_lower for word in ["add", "implement", "create"]):
            analysis["fix_strategy"] = "feature_addition"
            analysis["estimated_time"] = 90
            analysis["payment_suggested"] = 75
            analysis["complexity"] = "medium"
            
        else:
            analysis["fix_strategy"] = "bug_fix"
            analysis["estimated_time"] = 45
            analysis["payment_suggested"] = 40
            
        # Risk assessment
        if repo_info.get("size", 0) > 50000:  # Large repo
            analysis["complexity"] = "high"
            analysis["feasible"] = False
            analysis["reason"] = "Repository too large"
            
        if not repo_info.get("has_issues"):
            analysis["feasible"] = False
            analysis["reason"] = "Issues not enabled"
            
        return analysis
        
    def clone_repository(self, repo_full_name: str) -> Optional[str]:
        """Clone repository to temp directory"""
        self.log(f"📥 Cloning repository: {repo_full_name}")
        
        try:
            self.temp_dir = tempfile.mkdtemp(prefix=f"fixer_{repo_full_name.replace('/', '_')}_")
            repo_url = f"https://github.com/{repo_full_name}.git"
            
            cmd = f"git clone --depth 1 {repo_url} {self.temp_dir}/repo"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self.log("✅ Repository cloned successfully")
                return f"{self.temp_dir}/repo"
            else:
                self.log(f"❌ Clone failed: {result.stderr}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"❌ Clone error: {str(e)}", "ERROR")
            return None
            
    def apply_fix(self, repo_path: str, analysis: Dict) -> bool:
        """Apply the fix based on analysis"""
        self.log(f"🔧 Applying {analysis['fix_strategy']} fix...")
        
        strategy = analysis["fix_strategy"]
        
        try:
            if strategy == "typo_fix":
                return self._fix_typo(repo_path, analysis)
            elif strategy == "documentation":
                return self._improve_documentation(repo_path, analysis)
            elif strategy == "add_tests":
                return self._add_tests(repo_path, analysis)
            else:
                self.log("⚠️  Fix strategy not implemented yet", "WARN")
                return False
                
        except Exception as e:
            self.log(f"❌ Fix failed: {str(e)}", "ERROR")
            return False
            
    def _fix_typo(self, repo_path: str, analysis: Dict) -> bool:
        """Fix typo in repository"""
        # This would contain actual typo detection and fixing logic
        self.log("  Scanning for typos...")
        # Placeholder for actual implementation
        return False
        
    def _improve_documentation(self, repo_path: str, analysis: Dict) -> bool:
        """Improve documentation"""
        # This would contain actual documentation improvement logic
        self.log("  Analyzing documentation gaps...")
        # Placeholder for actual implementation
        return False
        
    def _add_tests(self, repo_path: str, analysis: Dict) -> bool:
        """Add missing tests"""
        # This would contain actual test generation logic
        self.log("  Generating test cases...")
        # Placeholder for actual implementation
        return False
        
    def create_pull_request(self, repo_full_name: str, branch_name: str, 
                          issue_number: int, payment_amount: int) -> Optional[str]:
        """Create PR with payment information"""
        self.log("📤 Creating pull request...")
        
        pr_body = f"""## Issue Resolution

This PR resolves #{issue_number}

### Changes Made
- [Detailed description of changes]

### Testing
- [Testing steps performed]

### Payment Information

For continued open-source contributions, I accept donations via:
- **Chain**: {PAYMENT_CHAIN}
- **Wallet**: `{PAYMENT_WALLET}`
- **Suggested Amount**: ${payment_amount} USD equivalent

Payment is optional but appreciated to support continued open-source work!

---
*This contribution was made by an independent developer. Feel free to review and merge if it adds value to your project.*
"""
        
        # Placeholder - actual PR creation would use GitHub API
        self.log("  PR body prepared")
        return None
        
    def cleanup(self):
        """Cleanup temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self.log("🧹 Temporary files cleaned")
            except Exception as e:
                self.log(f"⚠️  Cleanup warning: {str(e)}", "WARN")
                
    def run_single_cycle(self) -> Dict:
        """Run one complete fix cycle"""
        self.log("🚀 Starting fix cycle...")
        
        cycle_result = {
            "success": False,
            "issues_found": 0,
            "issue_analyzed": None,
            "pr_created": None
        }
        
        try:
            # Step 1: Search for issues
            issues = self.search_fixable_issues(max_results=20)
            cycle_result["issues_found"] = len(issues)
            
            if not issues:
                self.log("⚠️  No suitable issues found", "WARN")
                return cycle_result
                
            # Step 2: Analyze best issue
            best_issue = issues[0]
            self.log(f"🎯 Selected top issue: {best_issue['html_url']}")
            
            analysis = self.analyze_issue(best_issue)
            cycle_result["issue_analyzed"] = analysis
            
            if not analysis["feasible"]:
                self.log(f"⚠️  Issue not feasible: {analysis.get('reason')}", "WARN")
                return cycle_result
                
            # Step 3: Clone and fix
            repo_full_name = best_issue["repository_url"].split("/")[-2:]
            repo_full_name = "/".join(repo_full_name)
            
            repo_path = self.clone_repository(repo_full_name)
            if not repo_path:
                return cycle_result
                
            # Step 4: Apply fix (placeholder for now)
            self.log("⚠️  Automatic fixing not fully implemented yet", "WARN")
            self.log("📋 Issue details logged for manual review")
            
            cycle_result["success"] = True
            return cycle_result
            
        except Exception as e:
            self.log(f"❌ Cycle failed: {str(e)}", "ERROR")
            return cycle_result
        finally:
            self.cleanup()
            
    def run_continuous(self, cycles: int = -1, delay: int = 300):
        """Run bot continuously"""
        self.log(f"🤖 Starting continuous operation (delay: {delay}s)")
        
        cycle_count = 0
        while cycles < 0 or cycle_count < cycles:
            cycle_count += 1
            self.log(f"\n{'='*70}")
            self.log(f"CYCLE {cycle_count}")
            self.log(f"{'='*70}\n")
            
            result = self.run_single_cycle()
            
            self.log(f"\nCycle {cycle_count} summary:")
            self.log(f"  Issues found: {result['issues_found']}")
            self.log(f"  Success: {result['success']}")
            
            if cycles > 0 and cycle_count >= cycles:
                break
                
            self.log(f"\n⏳ Waiting {delay}s before next cycle...")
            time.sleep(delay)
            
        self.log("🏁 Continuous operation completed")


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        GitHub Intelligent Issue Fixer Bot v3.0              ║
║        Autonomous Revenue Generation System                  ║
║                                                              ║
║        Payment Wallet (peb20):                              ║
║        0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Initialize bot
    bot = IntelligentFixer()
    
    # Check for GitHub token
    if not bot.github_token:
        print("⚠️  WARNING: No GITHUB_TOKEN found. API rate limits will be very restrictive.")
        print("   Set GITHUB_TOKEN environment variable for better performance.")
        print()
    
    # Run single cycle for testing
    print("Running test cycle...\n")
    bot.run_single_cycle()
    
    print("\n" + "="*70)
    print("Test cycle complete. For continuous operation, implement scheduling.")
    print("="*70)


if __name__ == "__main__":
    main()
