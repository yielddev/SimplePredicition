import { task } from "hardhat/config";

task("deployPrediction", "Deploy a Two-Way Prediction Market")
  .addPositionalParam("usd")
  .addPositionalParam("side1Name")
  .addPositionalParam("side1Symbol")
  .addPositionalParam("side2Name")
  .addPositionalParam("side2Symbol")
  .setAction(async (taskArgs, hre) => {
    const ethers = hre.ethers;
    console.log(taskArgs)
    const Prediction = await ethers.getContractFactory("Prediction")
    const prediction = await Prediction.deploy(
      taskArgs.usd,
      taskArgs.side1Name,
      taskArgs.side1Symbol,
      taskArgs.side2Name,
      taskArgs.side2Symbol
    )
    console.log("Prediction Address: ", prediction.address)
  });
