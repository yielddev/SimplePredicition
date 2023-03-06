import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "./scripts/deployPrediction.ts"
import "./scripts/approveUSDC.ts"

const config: HardhatUserConfig = {
  solidity: "0.8.17",
  networks: {
    hardhat: {
      accounts: {
        count: 20
      }
    }
  }
};

export default config;
