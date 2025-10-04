from typing import Any
from app.utils.io import read_config
from app.customer import Customer
from app.shop import Shop
from app.car import Car


def shop_trip() -> Any:
    config = read_config("config.json")

    fuel_price = config["FUEL_PRICE"]
    customers_data = config["customers"]
    shops_data = config["shops"]

    customers = []
    for customer_data in customers_data:
        car = Car(customer_data["car"]["brand"],
                  customer_data["car"]["fuel_consumption"])
        customer = Customer(
            name=customer_data["name"],
            product_cart=customer_data["product_cart"],
            location=customer_data["location"],
            money=customer_data["money"],
            car=car
        )
        customers.append(customer)

    shops = []
    for shop_data in shops_data:
        shop = Shop(
            name=shop_data["name"],
            location=shop_data["location"],
            products=shop_data["products"]
        )
        shops.append(shop)

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        customer.min_products_cost = float("inf")

        for shop in shops:
            result = shop.total_products_costs(customer.product_cart)
            result1 = customer.trip_cost(shop, fuel_price)
            print(f"{customer.name}'s trip to the {shop.name}"
                  f" costs {result + result1}")
            if result < customer.min_products_cost:
                customer.min_products_cost = result
                customer.best_shop = shop.name

        if customer.can_afford(shop, fuel_price):
            customer.go_to(shop.location)
            for shop in shops:
                if shop.name == customer.best_shop:
                    shop.print_receipt(customer.name, customer.product_cart)

                    customer.go_to(customer.location)
                    money_after_shopping = round(
                        customer.money - (customer.trip_cost(shop, fuel_price)
                                          + customer.min_products_cost), 2)
                    customer.trip_cost(shop, fuel_price)
                    print(f"{customer.name} now has {money_after_shopping}\n")
        if customer.money < customer.min_products_cost:
            print(f"{customer.name} doesn't have enough money"
                  f" to make a purchase in any shop")
