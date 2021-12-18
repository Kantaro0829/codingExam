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
    print("ほしい戻り値：", list_to_dict_by_id(list))
    print("##################")
    print("タイプ：", type(list_to_dict_by_id(list)))
    print("タイプ：", type((dic_by_id, count_dic_by_id)))
    assert list_to_dict_by_id(list) == t