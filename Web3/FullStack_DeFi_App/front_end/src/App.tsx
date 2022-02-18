import React from "react";
import { ChainId, DAppProvider } from "@usedapp/core";
import { Header } from "./components/Header";
import { Container } from "@material-ui/core";
import { Main } from "./components/Main";

function App() {
    return (
        <DAppProvider
            config={{
                supportedChains: [ChainId.Rinkeby],
                notifications: {
                    expirationPeriod: 2000,
                    checkInterval: 2000,
                },
            }}
        >
            <Header></Header>
            <Container maxWidth="md">
                <Main></Main>
            </Container>
        </DAppProvider>
    );
}

export default App;
