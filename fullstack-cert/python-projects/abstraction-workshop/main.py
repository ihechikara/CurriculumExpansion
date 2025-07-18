from abc import ABC, abstractmethod
from typing import List

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class DiscountStrategy(ABC):
    @abstractmethod
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        pass
    @abstractmethod
    def apply_discount(self, product: Product) -> float:
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return self.percent <= 70

    def apply_discount(self, product: Product) -> float:
        return product.price * (1 - self.percent / 100)

class FixedAmountDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return product.price*0.9 > self.amount

    def apply_discount(self, product: Product) -> float:
        return product.price - self.amount

class PremiumUserDiscount(DiscountStrategy):
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        return user_tier.lower() == 'premium'

    def apply_discount(self, product: Product) -> float:
        return product.price * 0.80  # 20% off for premium users

class DiscountEngine:
    def __init__(self, strategies: List[DiscountStrategy]):
        self.strategies = strategies

    def calculate_best_price(self, product: Product, user_tier: str) -> float:
        prices = [product.price]

        for strategy in self.strategies:
            if strategy.is_applicable(product, user_tier):
                discounted = strategy.apply_discount(product)
                prices.append(discounted)

        return min(prices)


if __name__ == "__main__":
    product = Product("Wireless Mouse", 50.0)
    user_tier = "Premium"

    strategies = [
        PercentageDiscount(10),
        FixedAmountDiscount(5),
        PremiumUserDiscount()
    ]

    engine = DiscountEngine(strategies)
    best_price = engine.calculate_best_price(product, user_tier)

    print(f"Best price for {product.name} for {user_tier} user: ${best_price:.2f}")