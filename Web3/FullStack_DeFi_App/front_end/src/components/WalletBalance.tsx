import { Token } from "./Main";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { BalanceBox } from "./BalanceBox";
export interface WalletBalanceProps {
    token: Token;
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token;
    const { account } = useEthers();

    const tokenBalance = useTokenBalance(address, account);
    const formattedBalance = tokenBalance
        ? parseFloat(formatUnits(tokenBalance, 18))
        : 0;
    return (
        <BalanceBox
            label={`Your unstaked ${name} balance`}
            imgSrc={image}
            amount={formattedBalance}
        ></BalanceBox>
    );
};
