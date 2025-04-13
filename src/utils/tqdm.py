PRODUCTS_PARSING_CONFIG = dict(
    bar_format="{postfix[0]}: {postfix[value]}",
    postfix={0: "Products parsed", "value": 0},
    leave=False,
)

CREATING_EXCEL_CONFIG = dict(
    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    ncols=100,
    desc="Inserting products into the excel file",
)
