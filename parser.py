from datamodel import ProductVariant, VariantSize

def get_colour_and_size(soup, current_url):
    current_color = get_colour(soup)
    sizes, stock_indicator = get_sizes(soup)
    variant = ProductVariant(
        color = current_color,
        sizes = sizes,
        stock_indicator = stock_indicator,
        url = current_url
    )
    return variant

def get_colour(soup):
    return soup.select_one('span[data-automation="pdp-colour-display-value"]').text

def get_sizes(soup):
    sizes = []
    size_wrapper = soup.select_one('div[data-automation="select-size"]')
    get_sizes = size_wrapper.select('input')
    stock_indicator = "not available"
    for size in get_sizes:
        size_name = size.get('value')
        is_available = True
        if size.has_attr('disabled'):
            is_available = False
        item_size = VariantSize(
            is_available = is_available,
            size_name = size_name
        )
        sizes.append(item_size)
        if is_available:
            stock_indicator = "in stock"
    return sizes, stock_indicator