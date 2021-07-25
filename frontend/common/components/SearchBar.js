import styled from "styled-components";
import { useGlobalState, useGlobalDispatch } from "../hooks/useGlobalStore";

const Search = styled.div`
    width: 50%;
    margin: -47px auto;
    position: relative;
`;

const SearchInput = styled.input`
    width: 100%;
    height: 40px;
    border: unset;
    background-color: #f2f2f2;
    border-radius: 10px;
    padding-left: 45px;
    padding-right: 10px;
    color: ${({ theme }) => theme.colors.primary};
    caret-color: ${({ theme }) => theme.colors.primary};
    line-height: 40px;
    font-size: 18px;

    &:focus {
        outline: none;
    }
`;

const SearchIcon = styled.svg`
    position: absolute;
    top: 9px;
    left: 10px;
    font-size: 25px;

    & path {
        fill: ${({ theme }) => theme.colors.primary};
    }
`;

export default function SearchBar({}) {
    const { query } = useGlobalState();
    const dispatch = useGlobalDispatch();
    return (
        <Search>
            <SearchIcon
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
                focusable="false"
                width="1em"
                height="1em"
                preserveAspectRatio="xMidYMid meet"
                viewBox="0 0 24 24"
            >
                <path d="M10 18a7.952 7.952 0 0 0 4.897-1.688l4.396 4.396l1.414-1.414l-4.396-4.396A7.952 7.952 0 0 0 18 10c0-4.411-3.589-8-8-8s-8 3.589-8 8s3.589 8 8 8zm0-14c3.309 0 6 2.691 6 6s-2.691 6-6 6s-6-2.691-6-6s2.691-6 6-6z" />
            </SearchIcon>
            <SearchInput
                placeholder="Search"
                value={query}
                onInput={(e) => dispatch({ type: "setQuery", value: e.target.value })}
            ></SearchInput>
        </Search>
    );
}
