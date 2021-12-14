import csv
from pathlib import Path

def csv_to_list(filepath):
    print("=====================function csv_to_list=====================")
    result_list = []
    print("カレントディレクトリ:", Path.cwd().resolve())
    with open(filepath, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)


        print(csvreader)

        print("----------------------------")

        for index, row in enumerate(csvreader):
            if index is not 0:
                temp = []
                temp = [row[1], str(row[2])]
                
                result_list.append(temp)

    print(result_list)
    return result_list


"""
すでに処理したことのあるIDか判別する
"""
def is_id_existed(id, id_list):
    isExisting = False
    for i in id_list:
        if id == i:
            print(id, "はすでに存在している")
            isExisting = True

    return isExisting

"""
dic_by_id：idごとのスコアの合計値
count_dic_by_id：idごとのログの個数
に分ける

"""
def list_to_dict_by_id(list):
    print("=====================function list_to_dict_by_id=====================")
    ids = [] #処理したIDを保存 primary
    dic_by_id = {} #idごとのスコアの合計値
    count_dic_by_id = {} #idごとのログの個数


    for i in list:
        print(dic_by_id)
        if ids:
            if is_id_existed(i[0], ids):
                print(dic_by_id[i[0]])

                count_dic_by_id[i[0]] += 1 #それぞれ値代入
                dic_by_id[i[0]] =  int(dic_by_id[i[0]]) + int(i[1]) #それぞれ値代入

            if not is_id_existed(i[0], ids):
                ids.append(i[0])#新規のIDを処理済みとして保存
                dic_by_id[i[0]] = int(i[1]) #それぞれ値代入
                count_dic_by_id[i[0]] = 1 #それぞれ値代入

        else:
            #最初だけids(list)に値が存在してないので処理する
            print("else: ", i[0])
            ids.append(i[0]) #それぞれ値代入
            dic_by_id[i[0]] = i[1] #それぞれ値代入
            count_dic_by_id[i[0]] = 1 #それぞれ値代入
            print("else: ", dic_by_id)
        
    return dic_by_id, count_dic_by_id

#各プレイヤーの平均値を求める
def avg_of_each_player(count_dic, score_dic):
    avg_dic_by_id = {}
    for k, v in score_dic.items():
        avg_dic_by_id[k] = int(v / count_dic[k])
        print(k, v)

    return avg_dic_by_id

"""
ランキングをつける関数
"""
def ranking(list):
    print(list)
    result_list = []

    flg = False #連続で同じスコアが続いているか判断
    amount_of_player = 0 #ランキング内のプレイヤー合計
    privious_score = 0 #一つ前に調べたIDのスコア
    privious_rank = 0 #一つ前に調べたIDのランク

    for index, row in enumerate(list):
        temp_array = []
        print(index, row)

        if privious_score == row[1] and flg == False:#同じスコアが2連続のとき
            flg = True
            privious_rank = amount_of_player
            temp_array.append(amount_of_player)
            temp_array.append(row[0])
            temp_array.append(row[1])
            amount_of_player += 1

        elif privious_score == row[1] and flg == True:#同じスコアが3連続以上のとき
            flg = True
            temp_array.append(privious_rank)
            temp_array.append(row[0])
            temp_array.append(row[1])
            amount_of_player += 1

        else:# １つ目のスコアと今のスコアが違うとき
            flg = False
            privious_score = row[1]

            if amount_of_player < 10:#ランク１０位以内は記録する
                amount_of_player = index + 1
                temp_array.append(amount_of_player)
                temp_array.append(row[0])
                temp_array.append(row[1])

        result_list.append(temp_array)
    return result_list

"""
csv file 生成
"""
def list_to_csv(list):
    # csvモジュールを使って1行の内容をCSVファイルに書き込み
    with open('./csv/output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["rank","player_id", "mean_score"])

    # csvモジュールを使って複数行の内容をCSVファイルに書き込み
    with open('./csv/output.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)



def main():
    filename = './csv/input.csv'
    list_of_all = csv_to_list(filename)
    score_dic_by_id, count_dic_by_id = list_to_dict_by_id(list_of_all)
    print("idごとのスコアの合計")
    print(score_dic_by_id)
    print("idごとのプレイ回数")
    print(count_dic_by_id)

    result = avg_of_each_player(count_dic_by_id, score_dic_by_id)
    print(result)

    sorted_list = sorted(result.items(), key = lambda x : x[1], reverse=True)#スコアをもとに降順でソート
    
    ranked_list = ranking(sorted_list)


    print("===================最終結果=======================")
    print(ranked_list)
    list_to_csv(ranked_list)
    

    



if __name__ == "__main__":
    main()
