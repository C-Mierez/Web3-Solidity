import { Token } from "./Main";
import { Box, makeStyles, Tab } from "@material-ui/core";
import React, { useState } from "react";
import { TabContext, TabList, TabPanel } from "@material-ui/lab";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from "./StakeForm";

interface UserWalletProps {
    supportedTokens: Array<Token>;
}

const useStyles = makeStyles((theme) => ({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4),
    },
    box: {
        backgroundColor: "white",
        borderRadius: "25px",
    },
    header: {
        color: "white",
    },
}));

export const UserWallet = ({ supportedTokens }: UserWalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);

    const onChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue));
    };

    const classes = useStyles();

    return (
        <Box>
            <h1 className={classes.header}>Wallet</h1>
            <Box className={classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList aria-label="stake form tabs" onChange={onChange}>
                        {supportedTokens.map((token, index) => {
                            return (
                                <Tab
                                    label={token.name}
                                    value={index.toString()}
                                    key={index}
                                ></Tab>
                            );
                        })}
                    </TabList>
                    {supportedTokens.map((token, index) => {
                        return (
                            <TabPanel value={index.toString()} key={index}>
                                <div className={classes.tabContent}>
                                    <WalletBalance
                                        token={
                                            supportedTokens[selectedTokenIndex]
                                        }
                                    ></WalletBalance>
                                    <StakeForm
                                        token={supportedTokens[index]}
                                    ></StakeForm>
                                </div>
                            </TabPanel>
                        );
                    })}
                </TabContext>
            </Box>
        </Box>
    );
};
