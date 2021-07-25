import React from "react";
import { createGlobalStyle, ThemeProvider } from "styled-components";
import { GlobalStateProvider } from "../common/hooks/useGlobalStore";

const GlobalStyle = createGlobalStyle`
body {
    color: #3a3a3a;
    font-weight: 400;
    font-style: normal;
    line-height: 1;
    cursor: default;
    font-size: 1rem;
    font-family: "Galano Grotesque W00 Regular", Arial, sans-serif;
    line-height: 1.2rem;
    margin:0;
}
`;

const theme = {
    colors: {
        primary: "#2e008b",
        accent_1: "#21bbb1",
    },
};

export default function App({ Component, pageProps }) {
    return (
        <>
            <GlobalStyle />
            <ThemeProvider theme={theme}>
                <GlobalStateProvider>
                    <Component {...pageProps} />
                </GlobalStateProvider>
            </ThemeProvider>
        </>
    );
}
