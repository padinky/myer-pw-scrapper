from dataclasses import dataclass
from typing import List

@dataclass
class ProductPerPage:
    product_id: str
    product_name: str
    product_brand: str
    product_detail_url: str
    product_price_was: str
    product_price_now: str

@dataclass
class ProductSEO:
    title: str
    description: str
    product_schema: str
    product_review_schema: str

@dataclass
class VariantSize:
    size_name: str
    is_available: bool

@dataclass
class ProductVariant:
    color: str
    sizes: List[VariantSize]
    stock_indicator: str
    url: str

@dataclass
class ProductDetail(ProductPerPage):
    SEO: ProductSEO
    variants: List[ProductVariant]