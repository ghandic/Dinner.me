import styled from "styled-components";

import { useGlobalDispatch, useGlobalState } from "../hooks/useGlobalStore";

const Button = styled.div`
    border: 2px solid ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.primary};

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
    right: calc(1rem + (2 * var(--size)) + (2 * var(--logo-gap)));
    top: 50%;
    transform: translateY(-50%);

    & svg {
        width: calc(var(--size) * var(--ratio));
        height: calc(var(--size) * var(--ratio));
        margin-top: calc(var(--size) * var(--x-ratio-2));
        fill: ${({ theme }) => theme.colors.primary};
    }

    &:hover {
        background: ${({ theme }) => theme.colors.primary};
        color: #fff;
        cursor: pointer;

        & svg {
            & g {
                fill: #fff;
            }
        }
    }
`;
export default function ClearCartButton({}) {
    const { items } = useGlobalState();
    const dispatch = useGlobalDispatch();
    return (
        <Button
            onClick={() => {
                items.length > 0 && dispatch({ type: "clear_items" });
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
        </Button>
    );
}
