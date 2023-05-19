from playwright.async_api import async_playwright, TimeoutError
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datamodel import ProductPerPage, ProductDetail, ProductSEO
from helper import BASE_URL, logging, route_intercept, write_json_file
from parser import get_colour_and_size


async def run_playwright(page_start=1, page_end=51):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(60000)
        await page.route("**/*", route_intercept)
        page_no = page_start-1
        while True:
            page_no += 1
            if page_no > page_end:
                break
            try:
                url = urljoin(BASE_URL,"c/men/mens-clothing/casual-shirts?pageNumber="+str(page_no))
                await page.goto(url)

                # Perform actions on the page
                await page.wait_for_selector('//ul[@data-automation="product-grid"]')

                # Get the page content
                page_content = await page.content()

                # Parse the HTML using BeautifulSoup
                soup = BeautifulSoup(page_content, "lxml")
                # Find and extract the product information using XPath
                product_elements = soup.select('li[data-automation="product-grid-item"]')
                results_per_page = []
                results_per_page_dict = []
                for p in product_elements:
                    product_id = p.get("id")
                    product_brand = p.select_one('span[data-automation="product-brand"]').text
                    product_name = p.select_one('span[data-automation="product-name"]').text
                    product_url = p.select_one('a').get('href')
                    price_was = ""
                    check_price_was = p.select_one('span[data-automation="product-price-was"]')
                    if check_price_was is not None:
                        price_was = p.select_one('span[data-automation="product-price-was"]').text
                    price_now = ""
                    check_price_now = p.select_one('span[data-automation="product-price-now"]')
                    if check_price_now is not None:
                        price_now = p.select_one('span[data-automation="product-price-now"]').text
                    item = ProductPerPage (
                        product_id=product_id,
                        product_name=product_name,
                        product_brand=product_brand,
                        product_detail_url=urljoin(BASE_URL, product_url),
                        product_price_was=price_was,
                        product_price_now=price_now
                    )
                    # print(asdict(item))
                    results_per_page.append(item)
                    results_per_page_dict.append(asdict(item))
                
                # todo : change filename dynamic
                write_json_file("product_page_"+str(page_no)+".json",results_per_page_dict)

                # go to each product page
                for p in results_per_page:
                    try:
                        await page.goto(p.product_detail_url)
                        await page.wait_for_selector('div#add-to-bag')
                        # Get the page content
                        page_content = await page.content()
                        # Parse the HTML using BeautifulSoup
                        soup = BeautifulSoup(page_content, "lxml")

                        # Product SEO
                        meta_title = soup.select_one('title').text
                        meta_desc = soup.select_one('meta[data-automation="meta-description"]').text
                        seo_product_schema = ""
                        seo_product_review = ""

                        check_seo_product_schema = soup.select_one('script[data-automation="seo-product-schema"]')
                        if check_seo_product_schema is not None:
                            seo_product_schema = soup.select_one('script[data-automation="seo-product-schema"]').decode_contents()
                        
                        check_seo_product_review = soup.select_one('script[data-automation="product-review-seo-schema"]')
                        if check_seo_product_review is not None:
                            seo_product_review = soup.select_one('script[data-automation="product-review-seo-schema"]').decode_contents()
                        
                        product_seo = ProductSEO(
                            title=meta_title,
                            description=meta_desc,
                            product_schema=seo_product_schema,
                            product_review_schema=seo_product_review
                        )

                        variants = []
                        all_colour_variants_wrapper = soup.select('div[data-automation="pdp-colour-container-desktop"]')
                        if len(all_colour_variants_wrapper) == 0:
                            # only one color
                            print("only one variant")
                            variant = get_colour_and_size(soup, page.url)
                            variants.append(asdict(variant))
                        else:
                            # multiple colors
                            print("multiple color variants")
                            color_wrapper = all_colour_variants_wrapper[0]
                            get_variant_urls = color_wrapper.select('a')
                            variant_urls = []
                            for v in get_variant_urls:
                                variant_urls.append(urljoin(BASE_URL, v.get("href")))

                            for v in variant_urls:
                                print("ACCESSING VARIANT PAGE: "+v)
                                print("-----")
                                try:
                                    # driver.get(url)
                                    await page.goto(v)
                                    await page.wait_for_selector('div#add-to-bag')
                                    page_content = await page.content()
                                    soup = BeautifulSoup(page_content, "lxml")
                                    variant = get_colour_and_size(soup, page.url)
                                    variants.append(asdict(variant))
                                except TimeoutError:
                                    # Handle the TimeoutError
                                    err_msg = "Timeout occurred while accessing : "+page.url
                                    print(err_msg) 
                                    logging.error(err_msg)
                                    continue

                        # print(variants)
                        print(product_seo)
                        product_detail = ProductDetail(
                            product_id = p.product_id,
                            product_brand = p.product_brand,
                            product_name = p.product_name,
                            product_detail_url = p.product_detail_url,
                            product_price_was = p.product_price_was,
                            product_price_now = p.product_price_now,
                            variants = variants,
                            SEO = product_seo
                        )
                        write_json_file(p.product_id+".json",asdict(product_detail))
                    except TimeoutError:
                        # Handle the TimeoutError
                        err_msg = "Timeout occurred while accessing : "+page.url
                        print(err_msg) 
                        logging.error(err_msg)
                        continue

            except TimeoutError:
                # Handle the TimeoutError
                err_msg = "Timeout occurred while accessing : "+page.url
                print(err_msg) 
                logging.error(err_msg)
                continue


        await browser.close()