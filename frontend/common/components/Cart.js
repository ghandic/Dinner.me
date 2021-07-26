import styled from "styled-components";
import { useGlobalDispatch, useGlobalState } from "../hooks/useGlobalStore";
import onClickOutside from "react-onclickoutside";

const CartContainer = styled.div`
    color: ${({ theme }) => theme.colors.primary};
    width: 350px;
    height: 500px;
    border-radius: 10px;
    z-index: 99;
    position: absolute;
    right: 40px;
    top: 80px;
    background: #fff;
    overflow: auto;
`;

const CartTitle = styled.h2`
    line-height: 22px;
    text-align: center;
`;
const ItemList = styled.table`
    position: relative;
    padding: 15px;
    text-align: left;
    width: 100%;
`;
const Item = styled.tr`
    list-style: none;
    line-height: 20px;
`;
const ItemThumbnail = styled.img`
    width: 50px;
    height: 50px;
`;
const ItemName = styled.p`
    font-size: 12px;
    margin: unset;
    max-width: 80%;
`;
const ItemQuantity = styled.p`
    font-size: 10px;
    margin: unset;
    width: 3em;
`;
const ItemTrashIcon = styled.div`
    cursor: pointer;
    margin-top: 5px;

    & svg {
        & g {
            fill: red;
        }
    }
`;

function Cart() {
    const { items } = useGlobalState();
    const dispatch = useGlobalDispatch();
    Cart.handleClickOutside = () => dispatch({ type: "cart_toggle" });
    return (
        <CartContainer>
            <CartTitle>Meal Plan</CartTitle>
            <ItemList>
                {items.map((item) => (
                    <Item>
                        <td>
                            <ItemThumbnail src={item.image}></ItemThumbnail>
                        </td>
                        <td>
                            <ItemName>{item.name}</ItemName>
                        </td>
                        <td>
                            <ItemQuantity>x {item.quantity}</ItemQuantity>
                        </td>
                        <td>
                            <ItemTrashIcon
                                onClick={() => {
                                    dispatch({
                                        type: "remove_item",
                                        value: {
                                            id: item.id,
                                            image: item.image.thumbnail,
                                            name: item.name,
                                        },
                                    });
                                }}
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    aria-hidden="true"
                                    focusable="false"
                                    width="1em"
                                    height="1em"
                                    preserveAspectRatio="xMidYMid meet"
                                    viewBox="0 0 16 16"
                                >
                                    <g>
                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                                        <path
                                            fill-rule="evenodd"
                                            d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
                                        />
                                    </g>
                                </svg>
                            </ItemTrashIcon>
                        </td>
                    </Item>
                ))}
            </ItemList>
        </CartContainer>
    );
}

const clickOutsideConfig = {
    handleClickOutside: () => Cart.handleClickOutside,
};

export default onClickOutside(Cart, clickOutsideConfig);
