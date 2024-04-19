from django import template 

register = template.Library()

@register.filter(name = "is_in_cart")
def is_in_cart(product, cart):
    keys = cart.keys()
    for prd_id in keys:
        if(prd_id == ""):
            break
        if (int(prd_id) == int(product.id)):
            return cart.get(prd_id)
    return False

@register.filter(name = "cart_quantity")
def cart_quantity(product, cart):
    amt = cart.get(str(product.id))
    return amt

@register.filter(name = "cart_price")
def cart_price(product, cart):
    amt = cart.get(str(product.id))
    price = product.price
    ans = int(amt) * price
    return ans

@register.filter(name = "cart_total")
def cart_total(product, cart):
    sum = 0
    for p in product:
        sum = sum + cart_price(p, cart)
    return sum

@register.filter(name = "currency")
def currency(number):
    return "₹" + str(number)

@register.filter(name = "mul")
def mul(n1, n2):
    return n1 * n2

@register.filter(name = "sum")
def sum(n1, n2):
    return n1 + n2

@register.filter(name = "cart_num")
def cart_num(cart):
    keys = cart.keys()
    return len(keys)

@register.filter(name = "loop_counter")
def loop_counter(num):
    return range(num)