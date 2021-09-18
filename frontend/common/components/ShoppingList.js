import onClickOutside from "react-onclickoutside";
import styled from "styled-components";

import { useGlobalDispatch } from "../hooks/useGlobalStore";

const ShoppingListContainer = styled.div`
    color: ${({ theme }) => theme.colors.primary};
    width: 75%;
    height: 75vh;
    border-radius: 10px;
    z-index: 99;
    position: fixed;
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

const CloseButton = styled.div`
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;

    svg {
        height: 2rem;
        width: 2rem;
        fill: ${({ theme }) => theme.colors.primary};
    }

    &:hover {
        color: #fff;
        cursor: pointer;

        & svg {
            & path {
                fill: ${({ theme }) => theme.colors.primary};
            }
            & path.circle {
                color: ${({ theme }) => theme.colors.primary};
            }
        }
    }
`;

function ShoppingList({ content }) {
    const dispatch = useGlobalDispatch();

    ShoppingList.handleClickOutside = () => dispatch({ type: "shopping_list_toggle" });
    if (typeof content.meals === "undefined") return <></>;

    return (
        <ShoppingListContainer>
            <ShoppingListContent>
                <h2>Meals</h2>
                <ul style={{ margin: 0 }}>
                    {Object.keys(content.meals).map((meal_id) => (
                        <li>
                            <a href={content.meals[meal_id].link}>{content.meals[meal_id].name}</a>
                        </li>
                    ))}
                </ul>
                <br />
                <h2 style={{ margin: 0 }}>Shopping List</h2>
                <br />
                <pre style={{ margin: 0 }}>{content.tabulate}</pre>
            </ShoppingListContent>
            <CloseButton onClick={ShoppingList.handleClickOutside}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                    role="img"
                    width="1em"
                    height="1em"
                    preserveAspectRatio="xMidYMid meet"
                    viewBox="0 0 512 512"
                >
                    <path
                        d="M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192s192-86 192-192z"
                        fill="none"
                        stroke="currentColor"
                        stroke-miterlimit="10"
                        stroke-width="32"
                        class="circle"
                    />
                    <path
                        fill="none"
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="32"
                        d="M320 320L192 192"
                    />
                    <path
                        fill="none"
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="32"
                        d="M192 320l128-128"
                    />
                </svg>
            </CloseButton>
        </ShoppingListContainer>
    );
}

const clickOutsideConfig = {
    handleClickOutside: () => ShoppingList.handleClickOutside,
};

export default onClickOutside(ShoppingList, clickOutsideConfig);
