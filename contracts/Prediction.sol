pragma solidity ^0.8.9;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./PredictionToken.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Prediction is Ownable{

    PredictionToken public side1;
    PredictionToken public side2;
    ERC20 public USD;
    PredictionToken public winner;


    constructor(address usd_, string memory name1_, string memory name2_, string memory symbol1_, string memory symbol2_) {
        side1 = new PredictionToken(name1_, symbol1_);
        side2 = new PredictionToken(name2_, symbol2_);
        USD = ERC20(usd_);
    }

    function setWinner(bool winningSide) public onlyOwner {
        if (winningSide) {
            winner = side1;
        } else {
            winner = side2;
        }

    }

    function mint(address account, uint256 amount) public {
        require(
            USD.transferFrom(account, address(this), amount),
            "Payment Reverted"
        );  
        side1.mint(account, amount);
        side2.mint(account, amount);
    }

    function redeem(address account, uint256 amount) public {
        require(
            winner.transferFrom(account, address(this), amount),
            "Redemtion Reverted"
        );
        USD.transfer(account, amount);
    }
}
