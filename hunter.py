#!/usr/bin/env python3
"""
Ghost Hunter - Automated DeFi Vulnerability Scanner
Operation Nightfall - Phase 2 Weaponization Module
"""

import os
import sys
import subprocess
import tempfile
import shutil
import argparse
from pathlib import Path
import urllib.parse

# Configuration
PRIZE_WALLET_ADDRESS = "0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C"

class GhostHunter:
    def __init__(self, target_url):
        self.target_url = target_url
        self.repo_name = self._extract_repo_name()
        self.temp_dir = None
        
    def _extract_repo_name(self):
        """Extract repository name from GitHub URL"""
        try:
            parsed = urllib.parse.urlparse(self.target_url)
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 2:
                return f"{path_parts[0]}_{path_parts[1]}"
            return "unknown_repo"
        except Exception:
            return "unknown_repo"
    
    def _log(self, message):
        """Enhanced logging with operation context"""
        print(f"[GHOST HUNTER] {message}")
        sys.stdout.flush()
    
    def _run_command(self, command, cwd=None, capture_output=False):
        """Execute shell command with error handling"""
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=cwd, 
                    capture_output=True, 
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                return result
            else:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=cwd, 
                    check=True,
                    timeout=300
                )
                return result
        except subprocess.TimeoutExpired:
            self._log(f"⚠️  Command timeout: {command}")
            return None
        except subprocess.CalledProcessError as e:
            self._log(f"❌ Command failed: {command}")
            self._log(f"   Error code: {e.returncode}")
            return None
        except Exception as e:
            self._log(f"❌ Unexpected error: {str(e)}")
            return None
    
    def validate_target(self):
        """Validate GitHub URL format"""
        self._log("🔍 Validating target URL...")
        
        if not self.target_url.startswith(('https://github.com/', 'http://github.com/')):
            self._log("❌ Invalid GitHub URL format")
            return False
            
        # Basic URL validation
        try:
            parsed = urllib.parse.urlparse(self.target_url)
            if not parsed.netloc or not parsed.path:
                self._log("❌ Malformed URL")
                return False
        except Exception as e:
            self._log(f"❌ URL validation error: {str(e)}")
            return False
            
        self._log("✅ Target URL validated")
        return True
    
    def clone_repository(self):
        """Clone target repository to temporary directory"""
        self._log("📥 Cloning target repository...")
        
        try:
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix=f"ghost_hunt_{self.repo_name}_")
            self._log(f"   Created temp directory: {self.temp_dir}")
            
            # Clone repository with depth limit for efficiency
            clone_cmd = f"git clone --depth 1 --quiet {self.target_url} {self.temp_dir}/repo"
            result = self._run_command(clone_cmd)
            
            if result is None:
                self._log("❌ Repository cloning failed")
                return False
                
            # Verify clone success
            repo_path = os.path.join(self.temp_dir, "repo")
            if not os.path.exists(repo_path):
                self._log("❌ Repository directory not found after clone")
                return False
                
            self._log("✅ Repository cloned successfully")
            return True
            
        except Exception as e:
            self._log(f"❌ Clone operation failed: {str(e)}")
            return False
    
    def run_slither_analysis(self):
        """Execute Slither static analysis on cloned repository"""
        self._log("🔬 Executing Slither analysis...")
        
        repo_path = os.path.join(self.temp_dir, "repo")
        
        try:
            # Check if Slither is installed
            slither_check = self._run_command("which slither", capture_output=True)
            if slither_check is None or slither_check.returncode != 0:
                self._log("❌ Slither not found. Installing...")
                install_result = self._run_command("pip install slither-analyzer")
                if install_result is None:
                    self._log("❌ Failed to install Slither")
                    return False
            
            # Look for Solidity files
            solidity_check = self._run_command(
                "find . -name '*.sol' | head -5", 
                cwd=repo_path, 
                capture_output=True
            )
            
            if solidity_check and solidity_check.stdout.strip():
                self._log(f"   Found Solidity files:\n{solidity_check.stdout.strip()}")
            else:
                self._log("⚠️  No Solidity files detected - proceeding anyway")
            
            # Run Slither with comprehensive options
            slither_cmd = (
                "slither . "
                "--print human-summary "
                "--print contract-summary "
                "--print function-summary "
                "--print variable-order "
                "--print call-graph "
                "--exclude-dependencies "
                "--exclude-optimization "
                "--exclude-informational"
            )
            
            self._log("   Running comprehensive Slither scan...")
            result = self._run_command(slither_cmd, cwd=repo_path, capture_output=True)
            
            if result is None:
                self._log("❌ Slither execution failed")
                return False, ""
                
            # Combine stdout and stderr for complete output
            full_output = ""
            if result.stdout:
                full_output += "=== SLITHER STDOUT ===\n"
                full_output += result.stdout
                full_output += "\n\n"
                
            if result.stderr:
                full_output += "=== SLITHER STDERR ===\n" 
                full_output += result.stderr
                full_output += "\n\n"
                
            if not full_output.strip():
                full_output = "Slither completed but produced no output. This could indicate:\n"
                full_output += "- No Solidity files found\n"
                full_output += "- No vulnerabilities detected\n"
                full_output += "- Compilation errors prevented analysis\n"
            
            self._log("✅ Slither analysis completed")
            return True, full_output
            
        except Exception as e:
            self._log(f"❌ Slither analysis error: {str(e)}")
            return False, ""
    
    def generate_report(self, slither_output):
        """Generate comprehensive vulnerability report"""
        self._log("📝 Generating vulnerability report...")
        
        try:
            report_content = f"""
=============================================================================
                        GHOST HUNTER VULNERABILITY REPORT
                            Operation Nightfall - Phase 2
=============================================================================

TARGET INFORMATION:
Repository URL: {self.target_url}
Repository Name: {self.repo_name}
Scan Timestamp: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
Prize Wallet: {PRIZE_WALLET_ADDRESS}

=============================================================================
                              SLITHER ANALYSIS
=============================================================================

{slither_output}

=============================================================================
                             ANALYSIS SUMMARY
=============================================================================

Repository: {self.target_url}
Total Issues Found: [Parse from Slither output]
Critical Vulnerabilities: [Review required]
Exploitation Confidence: [Manual assessment needed]

OPERATIONAL NOTES:
- This is an automated reconnaissance scan
- Manual verification required for all findings
- Cross-reference with known vulnerability patterns
- Prioritize reentrancy, oracle manipulation, and integer overflow issues

PRIZE WALLET ADDRESS: {PRIZE_WALLET_ADDRESS}

=============================================================================
                         END OF AUTOMATED REPORT
=============================================================================
"""
            
            # Write report to file
            with open("report.txt", "w", encoding="utf-8") as f:
                f.write(report_content)
                
            self._log("✅ Report generated successfully: report.txt")
            return True
            
        except Exception as e:
            self._log(f"❌ Report generation failed: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up temporary files and directories"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self._log("🧹 Temporary files cleaned up")
            except Exception as e:
                self._log(f"⚠️  Cleanup warning: {str(e)}")
    
    def hunt(self):
        """Main hunting operation"""
        self._log("🚀 GHOST HUNTER INITIATED")
        self._log(f"   Target: {self.target_url}")
        self._log(f"   Prize Wallet: {PRIZE_WALLET_ADDRESS}")
        
        try:
            # Validation phase
            if not self.validate_target():
                return False
                
            # Reconnaissance phase
            if not self.clone_repository():
                return False
                
            # Analysis phase
            success, slither_output = self.run_slither_analysis()
            if not success:
                return False
                
            # Reporting phase
            if not self.generate_report(slither_output):
                return False
                
            self._log("🎯 OPERATION COMPLETED SUCCESSFULLY")
            self._log("📋 Report available: report.txt")
            return True
            
        except Exception as e:
            self._log(f"💥 CRITICAL ERROR: {str(e)}")
            return False
        finally:
            self.cleanup()

def main():
    """Main entry point for Ghost Hunter"""
    parser = argparse.ArgumentParser(
        description="Ghost Hunter - Automated DeFi Vulnerability Scanner",
        epilog="Operation Nightfall - Phase 2 Weaponization Module"
    )
    parser.add_argument(
        "target_url", 
        help="GitHub repository URL to scan for vulnerabilities"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="Ghost Hunter v1.0 - Operation Nightfall"
    )
    
    args = parser.parse_args()
    
    # Initialize and execute hunter
    hunter = GhostHunter(args.target_url)
    success = hunter.hunt()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()