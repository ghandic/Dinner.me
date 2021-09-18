import styled from "styled-components";

import CartButton from "./CartButton";
import ClearCartButton from "./ClearCartButton";
import SearchBar from "./SearchBar";
import ShoppingListButton from "./ShoppingListButton";
import { useGlobalState } from "../hooks/useGlobalStore";
import { useWindowDimensions } from "../hooks/useWindowDimensions";

const Nav = styled.div`
    height: 80px;
    position: fixed;
    top: 0px;
    width: 100%;
    background: #fff;
    z-index: 999;
`;

const NavWrapper = styled.div`
    position: relative;
    // height: 80px;
    row-gap: 0;

    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    top: 50%;
    transform: translateY(-50%);
`;

const Logo = styled.h1`
    color: ${({ theme }) => theme.colors.primary};
    left: 1rem;
    font-family: "Dunbar Tall Medium", Arial, sans-serif;
    user-select: none;
    font-size: 1.5rem;
    margin-left: 20px;

    grid-column-start: 1;
    grid-column-end: 2;
`;

const Buttons = styled.div`
    position: relative;
    grid-column-start: 3;
    grid-column-end: 4;
`;

export default function NavBar({ windowWidth }) {
    const { itemCount } = useGlobalState();

    return (
        <Nav>
            <NavWrapper>
                {windowWidth > 600 ? <Logo>Dinner.me</Logo> : <Logo>DM</Logo>}
                <SearchBar />
                <Buttons>
                    {windowWidth > 600 && itemCount > 0 && <ClearCartButton />}
                    {itemCount > 0 && <ShoppingListButton />}
                    <CartButton />
                </Buttons>
            </NavWrapper>
        </Nav>
    );
}
