import { useContractFunction, useEthers } from "@usedapp/core";
import { constants, Contract, utils } from "ethers";
import TokenFarm from "../chain-config/chain-build/contracts/TokenFarm.json";
import ERC20 from "../chain-config/chain-build/contracts/MockToken.json";
import networkMapping from "../chain-config/chain-build/deployments/map.json";
import { useEffect, useState } from "react";

export const useStakeTokens = (tokenAddress: string) => {
    /**
     * - Need to approve the token spending
     * - Need to stake tokens
     */

    /* --------------------------------- Approve -------------------------------- */
    const { chainId } = useEthers();
    const { abi: tokenFarmABI } = TokenFarm;

    const tokenFarmAddress = chainId
        ? networkMapping[String(chainId)]["TokenFarm"][0]
        : constants.AddressZero;

    const tokenFarmInterface = new utils.Interface(tokenFarmABI);

    const tokenFarmContract = new Contract(
        tokenFarmAddress,
        tokenFarmInterface
    );

    const erc20ABI = ERC20.abi;
    const erc20Interface = new utils.Interface(erc20ABI);

    const erc20Contract = new Contract(tokenAddress, erc20Interface);

    // Approve
    const { send: approveErc20Send, state: approveAndStakeErc20State } =
        useContractFunction(erc20Contract, "approve", {
            transactionName: "Approve ERC20 transfer",
        });

    const approveAndStake = (amount: string) => {
        setAmountToStake(amount);
        return approveErc20Send(tokenFarmAddress, amount);
    };

    const { send: stakeSend, state: stakeState } = useContractFunction(
        tokenFarmContract,
        "stakeTokens",
        { transactionName: "Stake Tokens" }
    );

    const [amountToStake, setAmountToStake] = useState("0");

    useEffect(() => {
        if (approveAndStakeErc20State.status == "Success") {
            stakeSend(amountToStake, tokenAddress);
        }
    }, [approveAndStakeErc20State, amountToStake, tokenAddress]);

    const [state, setState] = useState(approveAndStakeErc20State);

    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            setState(stakeState);
        } else {
            setState(approveAndStakeErc20State);
        }
    }, [approveAndStakeErc20State, stakeState]);

    return { approveAndStake, state };
};
