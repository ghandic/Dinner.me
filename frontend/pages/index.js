import styled from "styled-components";
import useSWR from "swr";

import Card from "../common/components/Card";
import Gallery from "../common/components/Gallery";
import NavBar from "../common/components/NavBar";
import { useGlobalState } from "../common/hooks/useGlobalStore";

const PageContent = styled.div`
    background: #fff9f7;
    margin-top: 80px;
`;

const fetcher = (url) => fetch(url).then((r) => r.json());

export default function Home() {
    // TODO: Fix ingredients
    // TODO: Backend - Approx costings
    // TODO: Low priority - Fix searchbar for mobile
    const { query } = useGlobalState();
    const { data: meals, error } = useSWR(`${process.env.backendHost}/dinner/recipes`, fetcher);

    console.log()

    if (error) return <div>failed to load</div>;
    if (!meals) return <div>loading...</div>;

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
                    {meals.map((meal, index) => {
                        if (does_match(meal)) {
                            return <Card key={index} {...meal}></Card>;
                        }
                    })}
                </Gallery>
            </PageContent>
        </div>
    );
}
