// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

// Import the required contracts along with the CCredToken.sol contract
import "./CCredToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

contract CCredTokenCrowdsale is Crowdsale, MintedCrowdsale {

    // creating the parameters for exchange rate, wallet for the collected ether to mint and the token
    constructor(uint rate, address payable wallet, CCredToken token) Crowdsale(rate, wallet, token) public {}

}

contract CCredTokenCrowdsaleDeployer {

    // variable to assign the address of the contract CCredToken
    address payable public ccred_token_address;

    // variable to assign the address of the contract CCredTokenCrowdsale
    address payable public ccred_crowdsale_address;

    constructor (
        string memory name,
        string memory symbol,
        address payable wallet
    )
        public
    {   
        // Creating instance of the 'CCredToken' Contract
        CCredToken token = new CCredToken(name, symbol, 0);
        ccred_token_address = address(uint160(address(token)));

        // Creating instance of the 'CCredTokenCrowdsale' contract
        CCredTokenCrowdsale ccred_crowdsale = new CCredTokenCrowdsale(2931863492, wallet, token);
        ccred_crowdsale_address = address(ccred_crowdsale);

        // Set 'CCredTokenCrowdsale' contract as a minter
        token.addMinter(ccred_crowdsale_address);

        // Set 

        // Renounce the minter role of 'CCredTokenCrowdsaleDeployer'
        token.renounceMinter();

    }

}
