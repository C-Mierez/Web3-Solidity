import { useEthers } from "@usedapp/core";
import chain_id_mapping from "../chain-config/chain_id_mapping.json";
import networkMapping from "../chain-config/chain-build/deployments/map.json";
import { constants } from "ethers";
import brownieConfig from "../chain-config/brownie-config.json";
import stonk_img from "../img/stonk.jpg";
import dai_img from "../img/dai.png";
import link_img from "../img/link.png";
import eth_img from "../img/eth.png";
import { UserWallet } from "./UserWallet";
import { makeStyles } from "@material-ui/core";

export type Token = {
    image: string;
    address: string;
    name: string;
};

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4),
    },
}));

export const Main = () => {
    /**
     * Show token values from the wallet
     * Get the address of different tokens
     * Get the balance of the user wallets
     */

    const { chainId } = useEthers();

    const classes = useStyles();

    const strChainId = chainId?.toString();
    console.log(`strChainId ${strChainId}`);

    // const networkName = chainId ? String(chain_id_mapping[chainId]) : "unnamed";
    const networkName = strChainId
        ? chain_id_mapping.hasOwnProperty(strChainId)
            ? chain_id_mapping[strChainId]
            : "unnamed"
        : "unnamed";
    console.log(strChainId);
    console.log(networkName);

    const rewardTokenAddr = chainId
        ? networkMapping[String(chainId)]["RewardToken"][0]
        : constants.AddressZero;
    const wethTokenAddr = chainId
        ? brownieConfig["networks"][networkName]["contracts"]["tokens"]["weth"]
        : constants.AddressZero;
    const fauTokenAddr = chainId
        ? brownieConfig["networks"][networkName]["contracts"]["tokens"]["fau"]
        : constants.AddressZero;
    const linkTokenAddr = chainId
        ? brownieConfig["networks"][networkName]["contracts"]["tokens"]["link"]
        : constants.AddressZero;

    const supportedTokens: Array<Token> = [
        {
            image: stonk_img,
            address: rewardTokenAddr,
            name: "STONK",
        },
        {
            image: link_img,
            address: linkTokenAddr,
            name: "LINK",
        },
        {
            image: eth_img,
            address: wethTokenAddr,
            name: "WETH",
        },
        {
            image: dai_img,
            address: fauTokenAddr,
            name: "DAI",
        },
    ];

    return (
        <>
            <h2 className={classes.title}>Stonks 📈</h2>
            <UserWallet supportedTokens={supportedTokens}></UserWallet>;
        </>
    );
};
