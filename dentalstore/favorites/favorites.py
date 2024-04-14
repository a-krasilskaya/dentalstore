from catalog.models import Product
from dentalstore import settings


class Favorites(object):
    def __init__(self, request):
        """
        Initialize the favorite.
        """
        self.session = request.session
        self.products = self.session.get(settings.FAVORITES_SESSION_ID, [])

    def __iter__(self):
        """
        Iterate over the items in the favorites and get the products
        from the database.
        """
        products = Product.objects.filter(id__in=self.products)
        for product in products:
            yield product

    def __len__(self):
        """
        Count all items in the favorites.
        """
        return len(self.products)

    def add(self, product):
        """
        Add/delete a product to/from favorites.
        """
        if product.id not in self.products:
            self.products.append(product.id)
        self.save()

    def save(self):
        # update the session favorites
        self.session[settings.FAVORITES_SESSION_ID] = self.products
        self.session.modified = True
        print(f'Favorites.py {self.products}')

    def remove(self, product):
        """
        Remove a product from favorites
        :param product:
        :return:
        """
        if product.id in self.products:
            self.products.remove(product.id)
            self.save()

    def clear(self):
        """
        remove cart from session
        :return:
        """
        del self.session[settings.FAVORITES_SESSION_ID]
        self.session.modified = True
