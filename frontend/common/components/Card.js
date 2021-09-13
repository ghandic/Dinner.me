import styled from "styled-components";

import { useGlobalDispatch, useGlobalState } from "../hooks/useGlobalStore";

const CardContainer = styled.div`
    overflow: hidden;
    background-color: #fff;
    border-radius: 8px;
    border: 1px solid #ffe8de;
    width: 436px;
    margin: 20px;
    position: relative;
`;

const CardLink = styled.a`
    color: #3a3a3a;
    text-decoration: none;
`;

const CardImage = styled.img`
    max-width: 100%;
    height: auto;
    -ms-interpolation-mode: bicubic;
    display: inline-block;
    vertical-align: middle;
    width: 100%;
    border: 0;
`;

const CardDetails = styled.div`
    padding: 15px;
    position: relative;
`;

const CardType = styled.div`
    color: ${({ theme }) => theme.colors.accent_1};
    text-transform: uppercase;
    font-size: 0.75rem;
    margin-bottom: 0.5rem;
    line-height: 1;
    user-select: none;
`;

const CardServings = styled.div`
    color: ${({ theme }) => theme.colors.accent_1};
    text-transform: uppercase;
    font-size: 0.75rem;
    
    line-height: 1;
    user-select: none;
    position: absolute;
    top: 1rem;
    right: 1rem;
    // left: 50%;
    // transform: translate(-50%, 0);
`;

const CardTitle = styled.h2`
    font-weight: 400;
    line-height: 1.5;
    margin: 0;
    font-size: 24px;
    letter-spacing: 0;
`;

const CardSubtitle = styled.h3`
    font-size: 16px;
    letter-spacing: 0;
    margin: 0 0 15px;
    padding: 0;
    line-height: 1.31;
    font-weight: 400;
`;

const CardLabels = styled.ul`
    list-style: none;
    margin: 20px 0 5px;
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 2.5rem;
    font-family: inherit;
    padding: 0;
    user-select: none;
`;

const CardLabel = styled.li`
    margin: 0 10px 5px 0;
    border-radius: 100px;
    background-color: #f4f2f9;
    color: #3a3a3a;
    display: inline-block;
    font-size: 10px;
    letter-spacing: 1px;
    line-height: 16px;
    padding: 6px 10px;
    text-transform: uppercase;
`;

const AddToCart = styled.div`
    width: 30px;
    height: 30px;
    background: ${({ theme }) => theme.colors.accent_1};
    border-radius: 10px;
    position: absolute;
    right: 1rem;
    bottom: 1rem;
    line-height: 30px;
    text-align: center;
    color: #fff;
    cursor: pointer;
    transition: 0.1s;

    &:hover {
        color: ${({ theme }) => theme.colors.accent_1};
        box-shadow: inset 0 0 0 2px ${({ theme }) => theme.colors.accent_1};
        background: #fff;
    }
    user-select: none;
`;

const ItemCount = styled(AddToCart)`
    box-shadow: inset 0 0 0 2px ${({ theme }) => theme.colors.accent_1};
    right: 55px;
    color: ${({ theme }) => theme.colors.accent_1};
    background: unset;
    cursor: default;
`;

const RemoveFromCart = styled(AddToCart)`
    right: 95px;
    line-height: 28px;
`;

export default function Card({
    id = "",
    image = { medium: "" },
    meal_type = "",
    recipe_card_url = "",
    name = "",
    subtitle = "",
    meal_attributes = [],
    serves = 2
}) {
    const { items } = useGlobalState();
    const itemCount = items.filter((item) => item.id === id)?.[0]?.quantity || 0;
    const dispatch = useGlobalDispatch();

    const details = {
        id: id,
        image: image.thumbnail,
        name: name,
        link: recipe_card_url
    };

    return (
        <CardContainer>
            <CardImage src={image.medium}></CardImage>
            <CardDetails>
                

                <CardType>{meal_type}</CardType>

                <CardTitle>
                    <CardLink href={recipe_card_url} target="_blank">
                        {name}
                    </CardLink>
                </CardTitle>
                <CardSubtitle>
                    <CardLink href={recipe_card_url} target="_blank">
                        {subtitle}
                    </CardLink>
                </CardSubtitle>
                <CardLabels>
                    {meal_attributes.map((label, index) => (
                        <CardLabel key={index}>{label.replace("_", " ").toUpperCase()}</CardLabel>
                    ))}
                </CardLabels>
                <CardServings>Serves: {serves}</CardServings>
            </CardDetails>
            {itemCount > 0 && (
                    <RemoveFromCart
                        onClick={() => {
                            dispatch({ type: "reduce_item", value: details });
                        }}
                    >
                        -
                    </RemoveFromCart>
                )}
                <ItemCount>{itemCount}</ItemCount>
                <AddToCart
                    onClick={() => {
                        dispatch({ type: "add_item", value: details });
                    }}
                >
                    +
                </AddToCart>
        </CardContainer>
    );
}
