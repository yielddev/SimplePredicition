import { task } from "hardhat/config";
const {
    BN,
    constants,
    ether
} = require("@openzeppelin/test-helpers");


task("approveUSDC", "Approve usdc spending")
  .addPositionalParam("usd")
  .addPositionalParam("amount")
  .addPositionalParam("predictionAddress")
  .addPositionalParam("account")
  .setAction(async(taskArgs, hre) => {
    const ethers = hre.ethers;

    const user = (await ethers.getSigners())[taskArgs.account]
    console.log(taskArgs)
    const USD = await ethers.getContractFactory("MockUSDC")
    const usd = await USD.attach(taskArgs.usd)
    console.log((await usd.address))
    await usd.mint(user.address, ether(taskArgs.amount).toString())
    const tx = await usd.connect(user).approve(taskArgs.predictionAddress, ether(taskArgs.amount).toString());
    // const allowance = await usd.allowance(user.address, taskArgs.predictionAddress)
    // console.log(allowance.toString())

    console.log("Receipt: ", tx)
  });
  
