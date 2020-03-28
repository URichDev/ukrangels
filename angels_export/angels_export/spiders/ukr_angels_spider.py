import scrapy


class UkrAngelsSpider(scrapy.Spider):
    name = 'ukr_angels_spider'
    start_urls = ['http://ukrainian-angels.com.ua/product_list/']

    # Выбор на главной странице блока с категориями
    def parse(self, response):

        # Перебор категорий
        for line in response.css('div.one-cat'):
            category_name = line.css('div.cat-name>a::text').extract_first()
            url = line.css('div.cat-name>a::attr(href)').extract_first()
            url = response.urljoin(url)

            # Переход по ссылке категории и вызов функции для сбора данных подкатегорий. Передается имя категории, для присваивания к товару
            yield scrapy.Request(url=url, callback=self.parse_subcategory,
                                 cb_kwargs=dict(category_name=category_name))

    # Выбор блока с подкатегориями в определенной категории
    def parse_subcategory(self, response, category_name):

        # Перебор подкатегорий
        for line in response.css('div.one-cat'):
            subcategory_name = line.css('div.cat-name>a::text').extract_first()
            category_name = f'{category_name} > {subcategory_name}'
            url = line.css('div.cat-name>a::attr(href)').extract_first()
            url = response.urljoin(url)

            # Переход по ссылке подкатегории и вызов функции для сбора данных о продуктах.
            # Передается имя категории и подкатегории, для присваивания к товару
            yield scrapy.Request(url=url, callback=self.parse_products, cb_kwargs=dict(category_name=category_name))

    # Выбор блока с товарами в определенной подкатегории
    def parse_products(self, response, category_name):

        # Перебор подкатегорий
        for line in response.css('div.one-item'):
            url = line.css('div.one-item>a::attr(href)').extract_first()
            url = response.urljoin(url)

            # Переход по ссылке продукта и вызов функции для сбора данных о продукте.
            # Передается имя категории и подкатегории, для присваивания к товару
            yield scrapy.Request(url=url, callback=self.parse_product,
                                 cb_kwargs=dict(category_name=category_name, url=url))

    # Выбор блока с информацией о товаре
    def parse_product(self, response, category_name, url):

        price = response.css('div.price-item::text').extract_first()

        # Удаляем в конце побел и .грн
        price = price.split()
        price = price[0]

        if response.css('div.old_price::text'):
            regular_price = response.css('div.old_price::text').extract_first()

            # Удаляем в конце побел и .грн
            regular_price = regular_price.split()
            regular_price = regular_price[0]
        else:
            regular_price = ''

        # Сбор url всех изображений товара и вывод их через запятую
        img_urls = ''
        for images in response.css('div.small-image'):
            img_urls += response.urljoin(images.css('div.small-image>a::attr(href)').extract_first())+','

        # Удаляем в конце строки 2 символа, запятую и пробел
        img_urls = img_urls[:(len(img_urls) - 1)]

        yield {
            'type' : 'simple',
            'sku' : '',
            'name' : response.css('h1.b-title::text').extract_first(),
            'status' : 1,
            'featured' : 1,
            'catalog_visibility' : 'visible',
            'short_description' : '',
            'description' : response.css('div.b-description').extract_first(),
            'date_on_sale_from' : '',
            'date_on_sale_to' : '',
            'tax_status' : 'taxable',
            'tax_class' : 'standard',
            'stock_status' : 1,
            'backorders' : 0,
            'sold_individually' : 1,
            'weight' : '',
            'height' : '',
            'reviews_allowed' : 1,
            'purchase_note' : '',
            'price' : price,
            'regular_price' : regular_price,
            'manage_stock/stock_quantitiy' : 100,
            'category_ids' : category_name,
            'tag_ids' : '',
            'shipping_class_id' : 'worldwide',
            'attributes' : '',
            'attributes_1' : '',
            'default_attributes' : '',
            'attributes_2' : '',
            'image_id/gallery_image_ids' : img_urls,
            'attributes_3' : '',
            'downloads' : '',
            'downloads_4' : '',
            'download_limit' : '',
            'download_expiry' : '',
            'parent_id' : '',
            'upsell_ids' : '',
            'cross_sell_ids' : ''
        }
