class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self, products):
        self.products = {p.sku: p for p in products}

    def get(self, sku):
        if sku not in self.products:
            raise KeyError(f"unknown sku: {sku}")
        return self.products[sku]

    def reserve(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        product = self.get(sku)
        if qty >= product.stock:
            raise OutOfStock(f"{sku}: wanted {qty}, have {product.stock}")
        product.stock -= qty

    def release(self, sku, qty):
        self.get(sku).stock += qty

    def low_stock(self, threshold=5):
        found = [p for p in self.products.values() if p.stock <= threshold]
        return sorted(found, key=lambda p: p.sku)
