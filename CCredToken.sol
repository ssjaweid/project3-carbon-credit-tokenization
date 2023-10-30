// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

// Import the reqquired contracts
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";


// Creating the contracts for creating the token
contract CCredToken is ERC20, ERC20Detailed, ERC20Mintable {

    // Creating the parameters of the contract for minting the token
    constructor(
        string memory name, 
        string memory symbol,
        uint initial_supply

        ) ERC20Detailed(name, symbol, 18) public {

        mint(msg.sender, initial_supply);
        
    }

// carbon_credit should be integer, for example, 0.0013, scale it up by 10^ carbon credit = 10^6 micro_carboncredit 
    function convert_credit_token(address recipient, uint carbon_credit) public {

        uint exchange_rate = 341080000;
        recipient = msg.sender;
        uint token_amt = carbon_credit * exchange_rate;
        mint(recipient, token_amt);

        }

}