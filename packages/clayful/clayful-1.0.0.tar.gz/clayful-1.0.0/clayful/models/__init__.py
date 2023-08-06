from clayful.models.brand import Brand
from clayful.models.cart import Cart
from clayful.models.catalog import Catalog
from clayful.models.collection import Collection
from clayful.models.country import Country
from clayful.models.coupon import Coupon
from clayful.models.currency import Currency
from clayful.models.customer import Customer
from clayful.models.discount import Discount
from clayful.models.downloadable import Downloadable
from clayful.models.group import Group
from clayful.models.image import Image
from clayful.models.impression import Impression
from clayful.models.order import Order
from clayful.models.order_tag import OrderTag
from clayful.models.payment_method import PaymentMethod
from clayful.models.product import Product
from clayful.models.review import Review
from clayful.models.review_comment import ReviewComment
from clayful.models.shipping_method import ShippingMethod
from clayful.models.store import Store
from clayful.models.subscription import Subscription
from clayful.models.subscription_plan import SubscriptionPlan
from clayful.models.tax_category import TaxCategory
from clayful.models.tracker import Tracker
from clayful.models.wish_list import WishList

def register_models(clayful):

	setattr(clayful, 'Brand', Brand.config(clayful))
	setattr(clayful, 'Cart', Cart.config(clayful))
	setattr(clayful, 'Catalog', Catalog.config(clayful))
	setattr(clayful, 'Collection', Collection.config(clayful))
	setattr(clayful, 'Country', Country.config(clayful))
	setattr(clayful, 'Coupon', Coupon.config(clayful))
	setattr(clayful, 'Currency', Currency.config(clayful))
	setattr(clayful, 'Customer', Customer.config(clayful))
	setattr(clayful, 'Discount', Discount.config(clayful))
	setattr(clayful, 'Downloadable', Downloadable.config(clayful))
	setattr(clayful, 'Group', Group.config(clayful))
	setattr(clayful, 'Image', Image.config(clayful))
	setattr(clayful, 'Impression', Impression.config(clayful))
	setattr(clayful, 'Order', Order.config(clayful))
	setattr(clayful, 'OrderTag', OrderTag.config(clayful))
	setattr(clayful, 'PaymentMethod', PaymentMethod.config(clayful))
	setattr(clayful, 'Product', Product.config(clayful))
	setattr(clayful, 'Review', Review.config(clayful))
	setattr(clayful, 'ReviewComment', ReviewComment.config(clayful))
	setattr(clayful, 'ShippingMethod', ShippingMethod.config(clayful))
	setattr(clayful, 'Store', Store.config(clayful))
	setattr(clayful, 'Subscription', Subscription.config(clayful))
	setattr(clayful, 'SubscriptionPlan', SubscriptionPlan.config(clayful))
	setattr(clayful, 'TaxCategory', TaxCategory.config(clayful))
	setattr(clayful, 'Tracker', Tracker.config(clayful))
	setattr(clayful, 'WishList', WishList.config(clayful))
