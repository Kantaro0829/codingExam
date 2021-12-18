import csv
import argparse
from decimal import Decimal, ROUND_HALF_UP


def csv_to_list(filepath):
    result_list = []

    with open(filepath, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)

        for index, row in enumerate(csvreader):

            if index:
                temp = []
                temp = [row[1], str(row[2])]
                result_list.append(temp)

    return result_list


def is_existing_id(id, id_list):
    """
    すでに処理したことのあるIDか判別する
    """
    is_existing = False
    for i in id_list:
        if id == i:
            is_existing = True

    return is_existing


def list_to_dict_by_id(list):
    """
    dic_by_id：idごとのスコアの合計値
    count_dic_by_id：idごとのログの個数
    に分ける
    """
    ids = []  # 処理したIDを保存 primary
    dic_by_id = {}  # idごとのスコアの合計値
    count_dic_by_id = {}  # idごとのログの個数

    for i in list:
        if ids:
            if is_existing_id(i[0], ids):

                count_dic_by_id[i[0]] += 1
                dic_by_id[i[0]] = int(dic_by_id[i[0]]) + int(i[1])

            if not is_existing_id(i[0], ids):

                ids.append(i[0])  # 新規のIDを処理済みとして保存
                dic_by_id[i[0]] = int(i[1])
                count_dic_by_id[i[0]] = 1

        else:
            # 最初だけids(list)に値が存在してないので処理する
            ids.append(i[0])
            dic_by_id[i[0]] = int(i[1])
            count_dic_by_id[i[0]] = 1

    return dic_by_id, count_dic_by_id


def avg_of_each_player(count_dic, score_dic):
    """
    各プレイヤーの平均値を求める(四捨五入)
    """

    avg_dic_by_id = {}
    for k, v in score_dic.items():
        avg_dic_by_id[k] = Decimal(str(float(v) / float(count_dic[k]))).\
            quantize(Decimal('0'), rounding=ROUND_HALF_UP)

    return avg_dic_by_id


def ranking(list):
    """
    ランキングをつける関数
    """
    result_list = []
    multiple_same_rank = False  # 連続で同じスコアが続いているか判断
    amount_of_player = 0  # ランキング内のプレイヤー合計
    privious_score = 0  # 一つ前に調べたIDのスコア
    privious_rank = 0  # 一つ前に調べたIDのランク

    for index, row in enumerate(list):
        temp_array = []

        if privious_score == row[1] and not multiple_same_rank:
            # 同じスコアが2連続のとき
            multiple_same_rank = True
            privious_rank = amount_of_player
            temp_array.append(amount_of_player)
            temp_array.append(row[0])
            temp_array.append(row[1])
            amount_of_player += 1

        elif privious_score == row[1] and multiple_same_rank:
            # 同じスコアが3連続以上のとき
            multiple_same_rank = True
            temp_array.append(privious_rank)
            temp_array.append(row[0])
            temp_array.append(row[1])
            amount_of_player += 1

        else:
            # 前回のスコアと今のスコアが違うとき
            multiple_same_rank = False
            privious_score = row[1]

            if amount_of_player < 10:
                # ランク１０位以内は記録する
                amount_of_player = index + 1
                temp_array.append(amount_of_player)
                temp_array.append(row[0])
                temp_array.append(row[1])

        if temp_array:
            result_list.append(temp_array)

    return result_list

# def list_to_csv(list):
#     """
#     csv file 生成
#     """
#     # tag?header? を最初に書き込み
#     with open('./csv/output.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(["rank", "player_id", "mean_score"])

#     # listの中身をすべてCSVファイルに書き込み
#     with open('./csv/output.csv', 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(list)


def print_final_result(list):

    for index, row in enumerate(list):
        if not index:
            print("rank,player_id,mean_score\n")

        print(f'{row[0]},{row[1]},{row[2]}\n')


def main():
    """
    CLIから引数を受取 -> CSVからリストへ -> リストからUserIdをKEY値としたスコア合計値とプレイ回数を
    それぞれ辞書型で記録 -> 各プレイヤの平均スコア取得 -> ソート -> ランク付け
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()

    filename = args.filepath
    list_of_all = csv_to_list(filename)

    score_dic_by_id, count_dic_by_id = list_to_dict_by_id(list_of_all)

    result = avg_of_each_player(count_dic_by_id, score_dic_by_id)

    sorted_list = sorted(
        result.items(), key=lambda x: x[1], reverse=True)  # スコアをもとに降順でソート

    ranked_list = ranking(sorted_list)

    print_final_result(ranked_list)


if __name__ == "__main__":
    main()
