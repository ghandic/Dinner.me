import onClickOutside from "react-onclickoutside";
import styled from "styled-components";

import { useGlobalDispatch } from "../hooks/useGlobalStore";

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


const underline = "=".repeat(13)

function ShoppingList({ content }) {
    const dispatch = useGlobalDispatch();

    ShoppingList.handleClickOutside = () => dispatch({ type: "shopping_list_toggle" });
    if (typeof content.meals === "undefined") return <></>

    return (
        <ShoppingListContainer>
            <ShoppingListContent>
                <h2 >Meals</h2>
                <ul  style={{margin:0}}>
                    {Object.keys(content.meals).map((meal_id) => <li><a href={content.meals[meal_id].link}>{content.meals[meal_id].name}</a></li>)}
                </ul>
                <br/>
                <h2 style={{margin:0}}>Shopping List</h2>
                <br/>
                <pre  style={{margin:0}}>{content.tabulate}</pre>
                

            </ShoppingListContent>
        </ShoppingListContainer>
    );
}

const clickOutsideConfig = {
    handleClickOutside: () => ShoppingList.handleClickOutside,
};

export default onClickOutside(ShoppingList, clickOutsideConfig);
