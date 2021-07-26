import styled from "styled-components";
import { useGlobalState, useGlobalDispatch } from "../hooks/useGlobalStore";
import Cart from "./Cart";

const Counter = styled.div`
    position: relative;
`;

const CounterValue = styled.div`
    border: 2px solid #fff;
    position: absolute;
    bottom: -1em;
    right: -1em;
    font-size: 10px;
    height: 2.2em;
    width: 2.2em;
    background: ${({ theme }) => theme.colors.primary};
    color: #fff;
    text-align: center;
    align-items: center;
    display: flex;
    justify-content: center;
    border-radius: 100%;
    user-select: none;
`;

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
    right: 40px;
    top: 25px;
    transition: 0.3s;
    font-size: 22px;
    z-index: 3;

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

const Overlay = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
    background: #000;
    opacity: 0.5;
`;

export default function CartButton({}) {
    const { itemCount, cartVisible } = useGlobalState();
    const dispatch = useGlobalDispatch();
    return (
        <>
            {cartVisible && <Overlay></Overlay>}
            <Button
                onClick={() => {
                    (itemCount > 0 || cartVisible) && dispatch({ type: "cart_toggle" });
                }}
                className="ignore-react-onclickoutside"
                active={cartVisible}
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                    focusable="false"
                    width="1.15em"
                    height="1em"
                    preserveAspectRatio="xMidYMid meet"
                    viewBox="0 0 2048 1792"
                >
                    <path d="M1920 768q53 0 90.5 37.5T2048 896t-37.5 90.5t-90.5 37.5h-15l-115 662q-8 46-44 76t-82 30H384q-46 0-82-30t-44-76l-115-662h-15q-53 0-90.5-37.5T0 896t37.5-90.5T128 768h1792zM485 1568q26-2 43.5-22.5T544 1499l-32-416q-2-26-22.5-43.5T443 1024t-43.5 22.5T384 1093l32 416q2 25 20.5 42t43.5 17h5zm411-64v-416q0-26-19-45t-45-19t-45 19t-19 45v416q0 26 19 45t45 19t45-19t19-45zm384 0v-416q0-26-19-45t-45-19t-45 19t-19 45v416q0 26 19 45t45 19t45-19t19-45zm352 5l32-416q2-26-15.5-46.5T1605 1024t-46.5 15.5t-22.5 43.5l-32 416q-2 26 15.5 46.5t43.5 22.5h5q25 0 43.5-17t20.5-42zM476 292l-93 412H251l101-441q19-88 89-143.5T601 64h167q0-26 19-45t45-19h384q26 0 45 19t19 45h167q90 0 160 55.5t89 143.5l101 441h-132l-93-412q-11-44-45.5-72t-79.5-28h-167q0 26-19 45t-45 19H832q-26 0-45-19t-19-45H601q-45 0-79.5 28T476 292z" />
                </svg>
                <Counter>{itemCount > 0 && <CounterValue>{itemCount}</CounterValue>}</Counter>
            </Button>
            {cartVisible && <Cart></Cart>}
        </>
    );
}
