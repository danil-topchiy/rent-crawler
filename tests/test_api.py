import pytest
import random

from rent_crawler.core.models import RentObject, CityDistrict
from rent_crawler.core.api import DEFAULT_PAGE_SIZE


@pytest.mark.usefixtures('testapp', 'db')
class TestRentObjectApi:

    def test_search_order(self, testapp, db):
        rent_objects_num = 5
        for i in range(rent_objects_num):
            RentObject.objects.create(title='{}'.format(i), price=random.randint(1000, 20000))
        res = testapp.get('/api/rent-objects')
        data = res.json['data']
        count = res.json['count']
        assert len(data) == count == rent_objects_num
        # check default order is new first
        assert int(data[0]['title']) > int(data[1]['title'])

        # old first
        res = testapp.get('/api/rent-objects?order_by=date')
        data = res.json['data']
        assert int(data[0]['title']) < int(data[1]['title'])

        # by price ascending
        res = testapp.get('/api/rent-objects?order_by=price')
        data = res.json['data']
        assert int(data[0]['price']) < int(data[1]['price'])

        # by price desc
        res = testapp.get('/api/rent-objects?order_by=-price')
        data = res.json['data']
        assert int(data[0]['price']) > int(data[1]['price'])
        assert True

    def test_pagination(self, testapp):
        total_objects_count = DEFAULT_PAGE_SIZE + 1
        for i in range(total_objects_count):
            RentObject.objects.create(title=str(i))

        res = testapp.get('/api/rent-objects?page=1&order_by=date')
        data = res.json['data']
        assert data[-1]['title'] == str(DEFAULT_PAGE_SIZE - 1)

        res = testapp.get('/api/rent-objects?page=2&order_by=date')
        count = res.json['count']
        data = res.json['data']
        assert count == total_objects_count
        assert len(data) == 1
        assert data[0]['title'] == str(DEFAULT_PAGE_SIZE)

    def test_rooms_filter(self, testapp):
        for rooms_count in range(1, 5):
            RentObject.objects.create(title='test title', rooms=rooms_count)
            RentObject.objects.create(title='test title', rooms=rooms_count)

        for rooms_count in range(1, 5):
            rooms_filter = 1
            res = testapp.get('/api/rent-objects?rooms={}'.format(rooms_filter))
            data = res.json['data']
            assert len(data)
            assert all([each['rooms'] == rooms_filter for each in data])

    def test_prices_filter(self, testapp):
        prices_range = [each * 1000 for each in range(1, 10)]
        for price in prices_range:
            RentObject.objects.create(title='test title', price=price)

        # test low price
        low_price = 3000
        res = testapp.get('/api/rent-objects?low_price={}'.format(low_price))
        count = res.json['count']
        data = res.json['data']
        assert count == len([each for each in prices_range if each >= low_price])
        assert all([each['price'] >= low_price for each in data])

        # test high price
        high_price = 7000
        res = testapp.get('/api/rent-objects?high_price={}'.format(high_price))
        count = res.json['count']
        data = res.json['data']
        assert count == len([each for each in prices_range if each <= high_price])
        assert all([each['price'] <= high_price for each in data])

        # test prices range
        res = testapp.get('/api/rent-objects?high_price={}&low_price={}'.format(high_price, low_price))
        count = res.json['count']
        data = res.json['data']
        assert count == len([each for each in prices_range if low_price <= each <= high_price])
        assert count == RentObject.objects.filter(price__lte=high_price).filter(price__gte=low_price).count()
        assert all([low_price <= each['price'] <= high_price for each in data])

    def test_city_district_filter(self, testapp):
        city_district_title_1 = 'Печерский'
        city_district_title_2 = 'Шевченковский'
        city_district_1 = CityDistrict.objects.create(title=city_district_title_1)
        city_district_2 = CityDistrict.objects.create(title=city_district_title_2)

        for i in range(10):
            district = city_district_1 if i % 2 else city_district_2
            RentObject.objects.create(title='test title', city_district=district)

        # test prices range
        res = testapp.get('/api/rent-objects?city_district={}'.format(city_district_1.id))
        count = res.json['count']
        data = res.json['data']
        assert count == RentObject.objects.filter(city_district=city_district_1).count()
        assert all([each['cityDistrictTitle'] == city_district_title_1 for each in data])

    def test_search_filter(self, testapp):
        title_search_phrase = 'find me in title, please'
        text_search_phrase = 'find me in text, please'
        for _ in range(10):
            RentObject.objects.create(title='test title', text='hello, world!', rooms=1)
        RentObject.objects.create(title="random {} random".format(title_search_phrase), text='random text')
        RentObject.objects.create(title='random title', text="test {} test".format(text_search_phrase))
        RentObject.objects.create(title='test {} test'.format(title_search_phrase),
                                  text="test {} test".format(text_search_phrase))

        # test search that doesn't exist with rooms number that exists, to approve right OR, AND filters
        res = testapp.get('/api/rent-objects?search={}&rooms=1'.format('doesn\'t exist'))
        count = res.json['count']
        data = res.json['data']
        assert count == 0
        assert not data

        # test in title
        res = testapp.get('/api/rent-objects?search={}'.format(title_search_phrase))
        count = res.json['count']
        data = res.json['data']
        assert count == 2
        assert len(data) == 2

        # test in text
        res = testapp.get('/api/rent-objects?search={}'.format(text_search_phrase))
        count = res.json['count']
        data = res.json['data']
        assert count == 2
        assert len(data) == 2


