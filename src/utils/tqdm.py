GETTING_PRODUCTS_CONFIG = dict(
    bar_format="{postfix[0]}: {postfix[value]}",
    postfix={0: "Products received", "value": 0},
    leave=False,
)

FORMATTING_PRODUCTS_CONFIG = dict(
    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    ncols=100,
    desc="Formatting products",
    leave=False,
)

CREATING_EXCEL_CONFIG = dict(
    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    ncols=100,
    desc="Inserting products into the excel file",
    leave=False,
)

SAVING_EXCEL_CONFIG = dict(
    bar_format="{desc}",
    desc="Saving excel file...",
    leave=False,
)
