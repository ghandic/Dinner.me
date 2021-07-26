import styled from "styled-components";
import { useGlobalDispatch } from "../hooks/useGlobalStore";
import onClickOutside from "react-onclickoutside";

const ShoppingListContainer = styled.div`
    color: ${({ theme }) => theme.colors.primary};
    width: 75%;
    height: 75vh;
    border-radius: 10px;
    z-index: 99;
    position: absolute;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
    top: 80px;
    background: #fff;
    overflow: auto;
`;

const ShoppingListContent = styled.pre`
    margin: 15px;
`;

function ShoppingList({ content }) {
    const dispatch = useGlobalDispatch();

    ShoppingList.handleClickOutside = () => dispatch({ type: "shopping_list_toggle" });

    return (
        <ShoppingListContainer>
            <ShoppingListContent>{content}</ShoppingListContent>
        </ShoppingListContainer>
    );
}

const clickOutsideConfig = {
    handleClickOutside: () => ShoppingList.handleClickOutside,
};

export default onClickOutside(ShoppingList, clickOutsideConfig);
