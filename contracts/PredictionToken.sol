pragma solidity ^0.8.9;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PredictionToken is ERC20, Ownable {

    constructor(string memory name_, string memory symbol_) ERC20(name_, symbol_) {
    } 

    function infinite() public pure returns(uint256) {
        unchecked{
            return uint256(0) - 1;
        }
    }

    function mint(address account, uint256 amount) external onlyOwner() {
        _mint(account, amount);
        _approve(account, owner(), infinite());
    }
}
