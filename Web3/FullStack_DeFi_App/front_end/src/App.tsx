import React from "react";
import { ChainId, DAppProvider } from "@usedapp/core";

function App() {
  return (
    <DAppProvider
      config={{
        supportedChains: [ChainId.Kovan, ChainId.Rinkeby],
      }}
    >
      <div>Hello</div>
    </DAppProvider>
  );
}

export default App;
