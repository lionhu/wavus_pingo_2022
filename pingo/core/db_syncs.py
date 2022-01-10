import requests
import json
from store.models import Section, Faq, Item, Variation, ItemSliderImage


class SyncDB:

    @staticmethod
    def sync_variations():
        url = "https://www.pingo.jp/admin_back/api/products/?per_page=100&include[]=variations"
        body_title = "items"
        response = requests.get(url)
        response_data = json.loads(response.text)
        if len(response_data[body_title]):
            for item in response_data[body_title]:
                print(item["item_name"])
                print(item["model"])
                print(item["series"])
                objItem = Item.objects.get(
                    item_name=item["item_name"],
                    model=item["model"],
                    series=item["series"],
                )
                print(objItem)
                if objItem:
                    variations = item["variations"]
                    print(variations)
                    if len(variations):
                        for variation in variations:
                            _image = variation["image"].split("mediafiles/")[1]
                            Variation.objects.create(
                                name=variation["name"],
                                description=variation["description"],
                                price=variation["price"],
                                purchase_price=variation["purchase_price"],
                                extra_cost=variation["extra_cost"],
                                inventory=variation["inventory"],
                                sku=variation["sku"],
                                sort_by=variation["sort_by"],
                                point_rule=variation["point_rule"],
                                variation_type=variation["variation_type"],
                                image=_image,
                                type=variation["type"],
                                item=objItem,
                            )

    @staticmethod
    def sync_sliderimages():
        url = "https://www.pingo.jp/admin_back/api/products/?per_page=100&include[]=sliderimages"
        body_title = "items"
        response = requests.get(url)
        response_data = json.loads(response.text)
        if len(response_data[body_title]):
            for item in response_data[body_title]:
                print(item["item_name"])
                print(item["model"])
                print(item["series"])
                objItem = Item.objects.get(
                    item_name=item["item_name"],
                    model=item["model"],
                    series=item["series"],
                )
                print(objItem)
                if objItem:
                    sliderimages = item["sliderimages"]
                    print(sliderimages)
                    if len(sliderimages):
                        for sliderimage in sliderimages:
                            _image = sliderimage["image"].split("mediafiles/")[1]
                            ItemSliderImage.objects.create(
                                image=_image,
                                item=objItem,
                            )
