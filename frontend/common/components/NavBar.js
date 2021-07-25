import styled from "styled-components";
import CartButton from "./CartButton";
import SearchBar from "./SearchBar";
import ShoppingListButton from "./ShoppingListButton";
import ClearCartButton from "./ClearCartButton";
import { useGlobalState } from "../hooks/useGlobalStore";

const Logo = styled.h1`
    color: ${({ theme }) => theme.colors.primary};
    padding-left: 30px;
    font-family: "Dunbar Tall Medium", Arial, sans-serif;
    user-select: none;
`;

const Nav = styled.div`
    height: 80px;
    position: fixed;
    top: 0;
    width: 100%;
    background: #fff;
    padding-top: 10px;
    z-index: 999;
`;

export default function NavBar({}) {
    const { itemCount } = useGlobalState();
    return (
        <Nav>
            <Logo>Dinner.me</Logo>
            <SearchBar></SearchBar>
            {itemCount > 0 && <ClearCartButton></ClearCartButton>}
            {itemCount > 0 && <ShoppingListButton></ShoppingListButton>}
            <CartButton></CartButton>
        </Nav>
    );
}
