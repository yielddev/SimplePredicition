import { time, loadFixture } from "@nomicfoundation/hardhat-network-helpers";
import { anyValue } from "@nomicfoundation/hardhat-chai-matchers/withArgs";
import { expect } from "chai";
import { ethers } from "hardhat";
const {
    BN,
    constants,
    ether
} = require("@openzeppelin/test-helpers");

describe("Prediction", function() {
    var PredictionToken: ethers.ContractFactory;
    var usdc: ethers.Contract;
    beforeEach(async function() {
        PredictionToken = await ethers.getContractFactory("PredictionToken")
        const USDC = await ethers.getContractFactory("MockUSDC")
        usdc = await USDC.deploy()
    })
    it("Should Deploy", async function() {
        const Prediction = await ethers.getContractFactory("Prediction")
        const prediction = await Prediction.deploy(usdc.address, "Lebron", "LBJ", "Giannis", "GAK")
        const side1 = await prediction.side1()
        const side1_instance = await PredictionToken.attach(side1)
        expect(await side1_instance.name()).to.equal("Lebron")
        console.log(side1)
    })
    describe("Prediction Exists", function() {
        var prediction: ethers.Contract;
        var side1: ethers.Contract;
        var side2: ethers.Contract;
        var owner: ethers.Signer;
        var user1: ethers.Signer;
        beforeEach(async function() {
            [owner, user1] = await ethers.getSigners();
            await usdc.mint(user1.address, ether('100').toString())
            const Prediction = await ethers.getContractFactory("Prediction")
            prediction = await Prediction.deploy(usdc.address, "Lebron", "LBJ", "Giannis", "GAK")
            let side1_address = await prediction.side1()
            let side2_address = await prediction.side2()
            side1 = await PredictionToken.attach(side1_address)
            side2 = await PredictionToken.attach(side2_address)
        })
        it("Should Mint", async function() {
            usdc.connect(user1).approve(prediction.address, ether('2').toString())
            await prediction.connect(user1).mint(user1.address, ether('2').toString());

            expect(await side1.balanceOf(user1.address)).to.equal(ether('2'))
            expect(await side2.balanceOf(user1.address)).to.equal(ether('2'))
            expect(await usdc.balanceOf(user1.address)).to.equal(ether('98'))
            expect(await usdc.balanceOf(prediction.address)).to.equal(ether('2'))
        })
        it("Should Allow Admin to set side1 as winner", async function() {
            await prediction.setWinner(true);
            expect(await prediction.winner()).to.equal(side1.address)
        })
        it("Should Allow Admin to set side2 as winner", async function() {
            await prediction.setWinner(false);
            expect(await prediction.winner()).to.equal(side2.address)
        })

        describe("Prediction Finalized", function() {
            beforeEach(async function() {
                usdc.connect(user1).approve(prediction.address, ether('2').toString())
                await prediction.connect(user1).mint(user1.address, ether('2').toString());
                await prediction.setWinner(true);
            })
            it("Should Redeem Winning Token", async function() {
                //await side1.connect(user1).approve(prediction.address, ether('2').toString());
                await prediction.connect(user1).redeem(user1.address, ether('2').toString());

                expect(await side1.balanceOf(user1.address)).to.equal(ether('0'))
                expect(await side2.balanceOf(user1.address)).to.equal(ether('2'))
                expect(await side1.balanceOf(prediction.address)).to.equal(ether('2'))
                expect(await usdc.balanceOf(prediction.address)).to.equal(ether('0'))
                expect(await usdc.balanceOf(user1.address)).to.equal(ether('100'))
            })
        })
    })
})
