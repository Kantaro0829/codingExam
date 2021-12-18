from main.main import *


def test_is_existing_id():
    assert is_existing_id(3, [1, 2]) == False
    assert is_existing_id(1, [1, 2]) == True


def test_list_to_dict_by_id():
    list = [
        ['1', '15000'],
        ['2', '5000']
    ]

    dic_by_id = {
        '1': 15000,
        '2': 5000
    }
    count_dic_by_id = {
        '1': 1,
        '2': 1
    }

    l = [dic_by_id, count_dic_by_id]

    t = tuple(l)
    assert list_to_dict_by_id(list) == t


def test_avg_of_each_player():

    dic_by_id = {
        '1': 15000,
        '2': 4,
        '3': 3
    }

    count_dic_by_id = {
        '1': 1,
        '2': 3,
        '3': 2
    }

    expected = {'1': Decimal('15000'), '2': Decimal('1'), '3': Decimal('2')}

    assert avg_of_each_player(count_dic_by_id, dic_by_id) == expected


def test_ranking():

    list = [
        ('player0001', Decimal('10000')),
        ('player0002', Decimal('10000')),
        ('player0003', Decimal('9000')),
        ('player0004', Decimal('9000')),
        ('player0005', Decimal('9000')),
        ('player0006', Decimal('999')),
        ('player0007', Decimal('998')),
    ]

    expected_list = [
        [1, 'player0001', Decimal('10000')],
        [1, 'player0002', Decimal('10000')],
        [3, 'player0003', Decimal('9000')],
        [3, 'player0004', Decimal('9000')],
        [3, 'player0005', Decimal('9000')],
        [6, 'player0006', Decimal('999')],
        [7, 'player0007', Decimal('998')]
    ]

    assert ranking(list) == expected_list
