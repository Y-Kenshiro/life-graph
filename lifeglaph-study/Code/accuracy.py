# 回答の正確度を計算するコード
#  -> 保存先は"[test]/Acc"
import pandas as pd

def make_csv(dir, data):
    # データフレーム化
    df_results = pd.DataFrame(data)

    # 全体の平均行を作成
    ave = pd.DataFrame([
        {
            "id": "origin_ave",
            "accuracy": df_results[df_results["id"].str.contains("origin")]["accuracy"].mean(),
        },{
            "id": "binary_ave",
            "accuracy": df_results[df_results["id"].str.contains("binary")]["accuracy"].mean(),
        }
    ])

    # 最終結果の結合
    final_df = pd.concat([ave,df_results], ignore_index=True)
    final_df.to_csv(dir, index=False, encoding="utf-8")

def calculate_accuracy(id, user, llm_origin, llm_binary):
    # データの準備
    user = user.values.flatten()
    origin = llm_origin.values.flatten()
    binary = llm_binary.values.flatten()

    # 一致度を計算する
    match_origin = (user == origin).sum() / len(user)  # user と json の一致度
    match_binary = (user == binary).sum() / len(user)  # user と story の一致度

    results = [
        {
            "id": f"origin_{id}",
            "accuracy": match_origin
        },
        {
            "id": f"binary_{id}",
            "accuracy": match_binary
        }
    ]
    return results

def tipi_acc(ids, load_dir, save_dir):
    data = []
    for id in ids:
        csv = pd.read_csv(f"{load_dir}/{id}.csv", encoding="utf-8")
        # tipiのcorrelation
        user = csv[csv["回答者"] == "user"].drop(columns=["回答者"])
        llm_origin = csv[csv["回答者"] == "llm"].drop(columns=["回答者"])
        # - 2値変換する
        llm_binary = llm_origin.copy()
        llm_binary.iloc[:, 1:] = llm_binary.iloc[:, 1:].map(lambda x: 1 if x > 4 else (0 if x == 4 else -1))
        data += calculate_accuracy(
            id=id,
            user=user,
            llm_origin=llm_origin,
            llm_binary=llm_binary,
        )
    # csvファイルで保存する
    make_csv(save_dir, data)

def pvq_acc(ids, load_dir, save_dir):
    data = []
    for id in ids:
        csv = pd.read_csv(f"{load_dir}/{id}.csv", encoding="utf-8")
        # tipiのcorrelation
        user = csv[csv["回答者"] == "user"].drop(columns=["回答者"])
        llm_origin = csv[csv["回答者"] == "llm"].drop(columns=["回答者"])
        # - 2値変換する
        llm_binary = llm_origin.copy()
        llm_binary.iloc[:, 1:] = llm_binary.iloc[:, 1:].map(lambda x: 1 if x >= 4 else -1)
        data += calculate_accuracy(
            id=id,
            user=user,
            llm_origin=llm_origin,
            llm_binary=llm_binary,
        )
    # csvファイルで保存する
    make_csv(save_dir, data)

ids = [
    "01","02","03","04","05","06","07","08","09","10",
    "11","12","13","14","15","16","17","18","19","20",
    "21","22","23","24","25","26","27","28","29"
]
#model = "Gemini"
#model = "GPT"
model = "Grok"
J_S = "JSON_nofig"
#J_S = "Story_nofig"
tipi_acc(
    ids,
    load_dir=f"{model}/TIPI/Que/{J_S}",
    save_dir=f"{model}/TIPI/Acc/{J_S}.csv"
)
pvq_acc(
    ids,
    load_dir=f"{model}/PVQ/Que/{J_S}",
    save_dir=f"{model}/PVQ/Acc/{J_S}.csv"
)
