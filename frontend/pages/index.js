import styled from "styled-components";

import Card from "../common/components/Card";
import Gallery from "../common/components/Gallery";
import Meals from "../common/data/Meals";
import NavBar from "../common/components/NavBar";
import { useGlobalState } from "../common/hooks/useGlobalStore";

const PageContent = styled.div`
    background: #fff9f7;
    margin-top: 80px;
`;

export default function Home() {
    // TODO: Shopping List page
    // TODO: Fix ingredients
    // TODO: Backend API
    // TODO: Infinite Scroll - https://ellismin.com/2020/05/next-infinite-scroll/
    // TODO: Backend - Approx costings
    // TODO: Low priority - Fix searchbar for mobile
    const { query } = useGlobalState();

    const does_match = (meal) => {
        return (
            // In name
            meal.name.toUpperCase().includes(query.toUpperCase()) ||
            // In labels
            meal.meal_attributes.some((item) =>
                item.replace("_", " ").toUpperCase().includes(query.toUpperCase())
            ) ||
            // In type
            meal.meal_type.toUpperCase().includes(query.toUpperCase())
        );
    };

    return (
        <div>
            <NavBar></NavBar>
            <PageContent>
                <Gallery>
                    {Meals.map((meal) => {
                        if (does_match(meal)) {
                            return <Card {...meal}></Card>;
                        }
                    })}
                </Gallery>
            </PageContent>
        </div>
    );
}
