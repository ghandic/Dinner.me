import pytest

from ..dinnerme.models.dinnerme.recipe import *


@pytest.mark.parametrize(
    "ingredient_input, expected",
    [
        (
            "400g tomato paste, 295ml whole-egg mayonnaise and 500ml barbecue sauce",
            [
                Ingredient(amount=400, unit="g", name="tomato paste"),
                Ingredient(amount=295, unit="ml", name="whole-egg mayonnaise"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "2 x 400g tomato paste, 295ml whole-egg mayonnaise and 500ml barbecue sauce",
            [
                Ingredient(amount=2 * 400, unit="g", name="tomato paste"),
                Ingredient(amount=295, unit="ml", name="whole-egg mayonnaise"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "2 x 400g tomato paste, 3 x 295ml whole-egg mayonnaise and 500ml barbecue sauce",
            [
                Ingredient(amount=2 * 400, unit="g", name="tomato paste"),
                Ingredient(amount=3 * 295, unit="ml", name="whole-egg mayonnaise"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "2 x 400g tomato paste, 3 x 295ml whole-egg mayonnaise and 10 x 500ml barbecue sauce",
            [
                Ingredient(amount=2 * 400, unit="g", name="tomato paste"),
                Ingredient(amount=3 * 295, unit="ml", name="whole-egg mayonnaise"),
                Ingredient(amount=10 * 500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "2 x 400g tomato paste, 3 x 295ml whole-egg mayonnaise and 1000 x 500ml barbecue sauce",
            [
                Ingredient(amount=2 * 400, unit="g", name="tomato paste"),
                Ingredient(amount=3 * 295, unit="ml", name="whole-egg mayonnaise"),
                Ingredient(amount=1000 * 500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "400g tomato paste and 500ml barbecue sauce",
            [
                Ingredient(amount=400, unit="g", name="tomato paste"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "400g tomato paste and 500ml barbecue sauce (optional)",
            [
                Ingredient(amount=400, unit="g", name="tomato paste"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "400g tomato paste (optional) and 500ml barbecue sauce (optional)",
            [
                Ingredient(amount=400, unit="g", name="tomato paste"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
            ],
        ),
        (
            "400g tomato paste (optional) and 500ml barbecue sauce (optional) and 5ml red wine vinegar",
            [
                Ingredient(amount=400, unit="g", name="tomato paste"),
                Ingredient(amount=500, unit="ml", name="barbecue sauce"),
                Ingredient(amount=5, unit="ml", name="red/white/balsamic vinegar"),
            ],
        ),
        ("400g can tomato paste (optional)", [Ingredient(amount=400, unit="g", name="tomato paste")]),
        ("400g can tomato paste (APPROVED BY RS)", [Ingredient(amount=400, unit="g", name="tomato paste")]),
        ("400g can tomato paste (MAX ALLOWED FOR LC)", [Ingredient(amount=400, unit="g", name="tomato paste")]),
        ("400g can tomato paste (APPROVED BY YN)", [Ingredient(amount=400, unit="g", name="tomato paste")]),
        ("400g can tomato paste, plus extra for greasing", [Ingredient(amount=400, unit="g", name="tomato paste")]),
        ("5 small garlic cloves", [Ingredient(amount=5, unit="", name="garlic clove")]),
        ("5 eggs", [Ingredient(amount=5, unit="", name="egg")]),
        ("⅚ cups eggs", [Ingredient(amount=0.833, unit="cups", name="egg")]),
        ("⅚ cups eggs (optional)", [Ingredient(amount=0.833, unit="cups", name="egg")]),
        ("⅚ tsp balsamic vinegar (optional)", [Ingredient(amount=0.833, unit="tsp", name="balsamic vinegar")]),
        (
            "7 kg balsamic vinegar or red wine vinegar (optional)",
            [Ingredient(amount=7, unit="kg", name="red/white/balsamic vinegar")],
        ),
    ],
)
def test_structure_ingredient(ingredient_input, expected):
    assert sorted(structure_ingredient(ingredient_input), key=lambda x: x.name) == sorted(
        expected, key=lambda x: x.name
    )


@pytest.mark.parametrize(
    "ingredient_input, expected",
    [
        (
            Ingredient(amount=7, unit="kg", name="red/white/balsamic vinegar"),
            Ingredient(amount=7000, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="l", name="red/white/balsamic vinegar"),
            Ingredient(amount=7000, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="tbsp", name="red/white/balsamic vinegar"),
            Ingredient(amount=7 * 17, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="tbs", name="red/white/balsamic vinegar"),
            Ingredient(amount=7 * 17, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="tsp", name="red/white/balsamic vinegar"),
            Ingredient(amount=7 * 5.69, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="g", name="red/white/balsamic vinegar"),
            Ingredient(amount=7, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="ml", name="red/white/balsamic vinegar"),
            Ingredient(amount=7, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="cup", name="red/white/balsamic vinegar"),
            Ingredient(amount=7 * 250, unit="g", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=7, unit="cups", name="red/white/balsamic vinegar"),
            Ingredient(amount=7 * 250, unit="g", name="red/white/balsamic vinegar"),
        ),
    ],
)
def test_standardize_ingredient(ingredient_input, expected):
    assert ingredient_input.standardize() == expected


@pytest.mark.parametrize(
    "ingredient_input, expected",
    [
        (
            [
                Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"),
                Ingredient(amount=4, unit="kg", name="red/white/balsamic vinegar"),
            ],
            Ingredient(amount=7, unit="kg", name="red/white/balsamic vinegar"),
        ),
    ],
)
def test_sum_ingredient_positive(ingredient_input, expected):
    assert sum(ingredient_input) == expected


@pytest.mark.parametrize(
    "ingredient_input",
    [
        (
            [
                Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"),
                Ingredient(amount=4, unit="g", name="red/white/balsamic vinegar"),
            ]
        ),
        (
            [
                Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"),
                Ingredient(amount=4, unit="kg", name="eggs"),
            ]
        ),
    ],
)
def test_sum_ingredient_fail(ingredient_input):
    try:
        sum(ingredient_input)
        assert False
    except TypeError:
        assert True
    except:
        assert False


@pytest.mark.parametrize(
    "ingredient_input, other",
    [
        (
            Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"),
            Ingredient(amount=4, unit="g", name="red/white/balsamic vinegar"),
        ),
        (Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"), ""),
    ],
)
def test_mul_ingredient_fail(ingredient_input, other):
    try:
        ingredient_input * other
        assert False
    except TypeError:
        assert True
    except:
        assert False


@pytest.mark.parametrize(
    "ingredient_input, other, expected",
    [
        (
            Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"),
            5,
            Ingredient(amount=15, unit="kg", name="red/white/balsamic vinegar"),
        ),
        (
            Ingredient(amount=3, unit="kg", name="red/white/balsamic vinegar"),
            2.5,
            Ingredient(amount=3 * 2.5, unit="kg", name="red/white/balsamic vinegar"),
        ),
    ],
)
def test_mul_ingredient_positive(ingredient_input, other, expected):
    assert ingredient_input * other == expected
    assert other * ingredient_input == expected

