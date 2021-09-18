import styled from "styled-components";
import { useEffect, useRef } from "react";
import { useSWRInfinite } from "swr";

import Card from "../common/components/Card";
import Gallery from "../common/components/Gallery";
import NavBar from "../common/components/NavBar";
import fetcher from "../common/utils/fetch";
import useDebounce from "../common/hooks/useDebounce";
import useOnScreen from "../common/hooks/useOnScreen";
import useWindowDimensions from "../common/hooks/useWindowDimensions";
import { useGlobalState } from "../common/hooks/useGlobalStore";

const PageContent = styled.div`
    background: #fff9f7;
    margin-top: 80px;
`;

const getKey = (pageIndex, previousPageData, query, pageSize) => {
    if (previousPageData && !previousPageData.length && typeof query !== "undefined") return null; // reached the end
    return `${process.env.backendHost}/dinner/recipes?q=${query}&per_page=${pageSize}&page=${pageIndex + 1}`;
};

export default function Home() {
    // TODO: Fix ingredients
    // TODO: Backend - Approx costings
    // TODO: Low priority - Fix searchbar for mobile

    const CARD_WIDTH = 436 + 2 * 20;

    const ref = useRef();
    const isVisible = useOnScreen(ref);
    const { width } = useWindowDimensions();
    const PAGE_SIZE = Math.floor((0.96 * width) / CARD_WIDTH);

    const { query } = useGlobalState();
    const debouncedQuery = useDebounce(query, 500);
    const { data, error, size, setSize, isValidating } = useSWRInfinite(
        (...args) => getKey(...args, debouncedQuery, PAGE_SIZE),
        fetcher
    );

    const recipes = data ? [].concat(...data) : [];
    const isLoadingInitialData = !data && !error;
    const isLoadingMore = isLoadingInitialData || (size > 0 && data && typeof data[size - 1] === "undefined");
    const isEmpty = data?.[0]?.length === 0;
    const isReachingEnd = isEmpty || (data && data[data.length - 1]?.length < PAGE_SIZE);
    const isRefreshing = isValidating && data && data.length === size;

    useEffect(() => {
        if (isVisible && !isRefreshing && !isReachingEnd) {
            setSize(size + 1);
        }
    }, [isVisible, isRefreshing]);

    return (
        <div>
            <NavBar windowWidth={width}></NavBar>
            <PageContent>
                <Gallery>
                    {error ? (
                        <div ref={ref}>Unable to connect to recipe server, retrying in background...</div>
                    ) : (
                        <>
                            {isEmpty ? <p>No recipes found :(</p> : null}
                            {recipes.map((meal, index) => (
                                <Card key={index} {...meal}></Card>
                            ))}
                            <div ref={ref} style={{ position: "absolute", bottom: -20 }}>
                                {!isEmpty &&
                                    (isLoadingMore ? "loading..." : isReachingEnd ? "fin" : "load more")}
                            </div>
                        </>
                    )}
                </Gallery>
            </PageContent>
        </div>
    );
}
