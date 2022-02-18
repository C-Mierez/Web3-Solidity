import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    container: {
        display: "inline-grid",
        gridTemplateColumns: "auto auto auto",
        gap: theme.spacing(1),
        alignItems: "center",
    },
    tokenImg: {
        width: "32px",
    },

    amount: {
        fontWeight: 700,
    },
}));

export interface BalanceBoxProps {
    label: string;
    imgSrc: string;
    amount: number;
}

export const BalanceBox = ({ label, imgSrc, amount }: BalanceBoxProps) => {
    const classes = useStyles();

    return (
        <div className={classes.container}>
            <div>{label}</div>
            <div className={classes.amount}>{amount}</div>
            <img
                className={classes.tokenImg}
                src={imgSrc}
                alt="Token Logo"
            ></img>
        </div>
    );
};
