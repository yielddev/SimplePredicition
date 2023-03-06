import { ethers } from "hardhat";

async function main() {
  const MockUSDC = await ethers.getContractFactory("MockUSDC");
  const mock_usdc = await MockUSDC.deploy();
  const Prediction = await ethers.getContractFactory("Prediction");
  const prediction = await Prediction.deploy(mock_usdc.address, "Lebron", "LBJ", "Giannis", "GAK")
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
