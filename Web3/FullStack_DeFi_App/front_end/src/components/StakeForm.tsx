import { Token } from "./Main";
import { useEthers, useNotifications, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { Button, CircularProgress, Input, Snackbar } from "@material-ui/core";
import React, { useEffect, useState } from "react";
import { useStakeTokens } from "../hooks/useStakeTokens";
import { utils } from "ethers";
import { Alert } from "@material-ui/lab";

export interface StakeFormProps {
    token: Token;
}

export const StakeForm = ({ token }: StakeFormProps) => {
    const { address: tokenAddress, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenBalance(tokenAddress, account);
    const formattedTokenBalance: number = tokenBalance
        ? parseFloat(formatUnits(tokenBalance, 18))
        : 0;
    const { notifications } = useNotifications();

    const [amount, setAmount] = useState<
        number | string | Array<number | string>
    >(0);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount =
            event.target.value === "" ? "" : Number(event.target.value);
        setAmount(newAmount);
    };

    const { approveAndStake, state: approveAndStakeErc20State } =
        useStakeTokens(tokenAddress);

    const handleStakeSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString());
        return approveAndStake(amountAsWei.toString());
    };

    const isMining = approveAndStakeErc20State.status === "Mining";

    const [showERC20ApprovalSuccess, setShowERC20ApprovalSuccess] =
        useState(false);
    const [showStakeTokenSuccess, setShowStakeTokenSuccess] = useState(false);

    useEffect(() => {
        if (
            notifications.filter(
                (notif) =>
                    notif.type === "transactionSucceed" &&
                    notif.transactionName === "Approve ERC20 transfer"
            ).length > 0
        ) {
            setShowERC20ApprovalSuccess(true);
            setShowStakeTokenSuccess(false);
        }
        if (
            notifications.filter(
                (notif) =>
                    notif.type === "transactionSucceed" &&
                    notif.transactionName === "Stake Tokens"
            ).length > 0
        ) {
            setShowERC20ApprovalSuccess(false);
            setShowStakeTokenSuccess(true);
        }
    }, [notifications, showERC20ApprovalSuccess, showStakeTokenSuccess]);

    const handleCloseSnack = () => {
        setShowERC20ApprovalSuccess(false);
        setShowStakeTokenSuccess(false);
    };

    return (
        <>
            <div>
                <Input onChange={handleInputChange}></Input>
                <Button
                    onClick={isMining ? () => {} : handleStakeSubmit}
                    disabled={isMining}
                    color="primary"
                    size="large"
                >
                    {isMining ? (
                        <CircularProgress size={28}></CircularProgress>
                    ) : (
                        "STAKEAME DADDY UWU"
                    )}
                </Button>
            </div>
            <Snackbar
                open={showERC20ApprovalSuccess}
                autoHideDuration={5000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity={"success"}>
                    ERC-20 token transfer approved!
                </Alert>
            </Snackbar>
            <Snackbar
                open={showStakeTokenSuccess}
                autoHideDuration={5000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity={"success"}>
                    Token Staked!
                </Alert>
            </Snackbar>
        </>
    );
};
