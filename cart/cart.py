from shop.models import Product, ProductCode, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    # =========================
    # ADD (WITH OPTIONAL CODE)
    # =========================
    def add(self, key, quantity, code_id=None):
        """
        key: str, either "3" or "3-12"
        quantity: int
        code_id: optional, ProductCode id
        """

        # Append code to key if provided
        if code_id:
            cart_key = f"{key}-{code_id}"
        else:
            cart_key = str(key)

        print("Cart Key:", cart_key)
        print("Quantity:", quantity)

        if cart_key in self.cart:
            # optional: increase quantity instead of replacing
            self.cart[cart_key] += quantity
        else:
            self.cart[cart_key] = quantity

        self.session.modified = True

        # If user is authenticated, save to Profile
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart).replace("'", '"')
            current_user.update(old_cart=cart_str)

    # =========================
    # LENGTH
    # =========================
    def __len__(self):
        return sum(self.cart.values())

    # =========================
    # CART TOTAL
    # =========================
    def cart_total(self):
        total = 0

        for key, qty in self.cart.items():

            # 🔹 NEW: parse key
            if "-" in key:
                product_id, _ = key.split("-")
                product_id = int(product_id)
            else:
                product_id = int(key)

            product = Product.objects.get(id=product_id)

            if product.is_available:
                if product.has_discount:
                    total += product.price_with_discount() * qty
                else:
                    total += product.price * qty

        return total

    # =========================
    # GET PRODUCTS
    # =========================
    def get_prods(self):
        product_ids = []

        for key in self.cart.keys():
            if "-" in key:
                product_id, _ = key.split("-")
            else:
                product_id = key
            product_ids.append(int(product_id))

        return Product.objects.filter(id__in=product_ids)

    # =========================
    # GET QUANTITIES
    # =========================
    def get_quants(self):
        return self.cart

    def get_codes(self, product_id):
        """Return a list of code IDs for a given product in the cart."""
        codes = []
        product_id_str = str(product_id)

        for key in self.cart.keys():
            if key.startswith(product_id_str + "-"):  # only keys with codes
                _, code_id = key.split("-")
                codes.append(code_id)

        return codes

    # =========================
    # UPDATE
    # =========================
    def update(self, key, quantity):
        quantity = int(quantity)

        if key in self.cart:
            self.cart[key] = quantity
            self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", '"')
            current_user.update(old_cart=carty)

        return self.cart

    # =========================
    # DELETE
    # =========================
    def delete(self, key):
        if key in self.cart:
            del self.cart[key]
            self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", '"')
            current_user.update(old_cart=carty)
