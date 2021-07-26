import { useState } from "react";
import styled from "styled-components";
import { useGlobalState, useGlobalDispatch } from "../hooks/useGlobalStore";
import Overlay from "./Overlay";
import ShoppingList from "./ShoppingList";

const Button = styled.div`
    border: 2px solid ${({ theme }) => theme.colors.primary};
    color: ${(props) => (props.active ? "#fff" : props.theme.colors.primary)};
    background: ${(props) => (props.active ? props.theme.colors.primary : "none")};

    width: 40px;
    height: 40px;
    line-height: 45px; /* same as height! */
    border-radius: 20%;
    text-align: center;
    position: fixed;
    right: 160px;
    top: 25px;
    transition: 0.3s;
    font-size: 22px;

    z-index: ${(props) => (props.active ? 3 : 1)};

    & svg {
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
                        items.forEach((item) => {
                            for (let index = 0; index < item.quantity; index++) {
                                ids.push(item.id);
                            }
                        });
                        itemCount > 0 &&
                            fetch(`http://0.0.0.0:8000/report?ids=${ids.join("&ids=")}`)
                                .then((r) => r.text())
                                .then((text) => setShoppingList(text));
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
