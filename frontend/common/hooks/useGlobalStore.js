import makeStore from "../utils/makeStore";

const initialState = {
    items: [],
    itemCount: 0,
    query: "",
};

const globalReducer = (state, action) => {
    switch (action.type) {
        case "reset":
            return initialState;

        case "setQuery":
            return {
                ...state,
                query: action.value,
            };
        case "clear_items":
            return {
                ...state,
                items: [],
                itemCount: 0,
            };
        case "add_item":
            var found = false;
            var newItems = state.items.slice();
            newItems.forEach((item) => {
                if (item.id == action.value.id) {
                    item.quantity++;
                    found = true;
                }
            });
            if (!found) {
                action.value.quantity = 1;
                newItems.push(action.value);
            }

            return {
                ...state,
                items: newItems,
                itemCount: state.itemCount + 1,
            };
        case "remove_item":
            var newItems = state.items.filter((item) => item.id != action.value.id);
            var newCount = newItems.reduce((acc, item) => acc + item.quantity, 0);

            return {
                ...state,
                items: newItems,
                itemCount: newCount,
            };
        case "reduce_item":
            var newItems = state.items.slice();
            var newCount = state.itemCount;
            newItems.forEach((item) => {
                if (item.id == action.value.id) {
                    item.quantity--;
                    newCount--;
                }
            });
            newItems = newItems.filter((item) => item.quantity > 0);

            return {
                ...state,
                items: newItems,
                itemCount: newCount,
            };
        default:
            throw new Error("Unknown action!", action);
    }
};

const [GlobalStateProvider, useGlobalDispatch, useGlobalState] = makeStore(globalReducer, initialState);

export { GlobalStateProvider, useGlobalState, useGlobalDispatch };
