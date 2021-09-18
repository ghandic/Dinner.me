import styled from "styled-components";
import { useState } from "react";

import Overlay from "./Overlay";
import ShoppingList from "./ShoppingList";
import { useGlobalDispatch, useGlobalState } from "../hooks/useGlobalStore";

const Button = styled.div`
    border: 2px solid ${({ theme }) => theme.colors.primary};
    color: ${(props) => (props.active ? "#fff" : props.theme.colors.primary)};
    background: ${(props) => (props.active ? props.theme.colors.primary : "none")};

    --size: 2rem;
    --ratio: 0.7;
    --x-ratio-2: calc((1 - var(--ratio)) / 2);
    --logo-gap: clamp(0.5rem, 5%, 1rem);

    width: var(--size);
    height: var(--size);
    line-height: calc(var(--size) * var(--ratio)); /* same as height! */
    border-radius: 20%;
    text-align: center;
    position: absolute;
    right: calc(1rem + (1 * var(--size)) + (1 * var(--logo-gap)));
    top: 50%;
    transform: translateY(-50%);
    transition: 0.3s;
    font-size: 22px;

    z-index: ${(props) => (props.active ? 3 : 1)};

    & svg {
        width: calc(var(--size) * var(--ratio));
        height: calc(var(--size) * var(--ratio));
        margin-top: calc(var(--size) * var(--x-ratio-2));
        & path {
            fill: ${(props) => (props.active ? "#fff" : props.theme.colors.primary)};
        }
    }

    &:hover,
    .active {
        background: ${({ theme }) => theme.colors.primary};
        color: #fff;
        cursor: pointer;

        & svg {
            & path {
                fill: #fff;
            }
        }
    }
`;
export default function ShoppingListButton({}) {
    const { items, itemCount, shoppingListVisible } = useGlobalState();
    const dispatch = useGlobalDispatch();
    const [shoppingList, setShoppingList] = useState("");

    return (
        <>
            {shoppingListVisible && <Overlay></Overlay>}
            <Button
                onClick={() => {
                    console.log("Open");
                    if (!shoppingListVisible) {
                        var ids = [];
                        var shoppingList = { meals: {}, tabulate: "" };
                        items.forEach((item) => {
                            for (let index = 0; index < item.quantity; index++) {
                                ids.push(item.id);
                                shoppingList.meals[item.id] = item;
                            }
                        });
                        itemCount > 0 &&
                            fetch(`${process.env.backendHost}/dinner/shopping_list?ids=${ids.join("&ids=")}`)
                                .then((r) => r.json())
                                .then((data) => {
                                    console.log(data);
                                    shoppingList.tabulate = data.tabulate;
                                    setShoppingList(shoppingList);
                                });
                    } else {
                        setShoppingList("");
                    }
                    dispatch({ type: "shopping_list_toggle" });
                }}
                active={shoppingListVisible}
                className="ignore-react-onclickoutside"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                    focusable="false"
                    width="1em"
                    height="1em"
                    preserveAspectRatio="xMidYMid meet"
                    viewBox="0 0 36 36"
                >
                    <path class="clr-i-outline clr-i-outline-path-1" d="M15 8h9v2h-9z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-2" d="M15 12h9v2h-9z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-3" d="M15 16h9v2h-9z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-4" d="M15 20h9v2h-9z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-5" d="M15 24h9v2h-9z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-6" d="M11 8h2v2h-2z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-7" d="M11 12h2v2h-2z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-8" d="M11 16h2v2h-2z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-9" d="M11 20h2v2h-2z" fill="#626262" />
                    <path class="clr-i-outline clr-i-outline-path-10" d="M11 24h2v2h-2z" fill="#626262" />
                    <path
                        d="M28 2H8a2 2 0 0 0-2 2v28a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm0 30H8V4h20z"
                        class="clr-i-outline clr-i-outline-path-11"
                        fill="#626262"
                    />
                </svg>
            </Button>
            {shoppingListVisible && <ShoppingList content={shoppingList}></ShoppingList>}
        </>
    );
}
