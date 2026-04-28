# スピアマンの順位相関係数を計算するコード
#  -> 保存先は"[test]/Corr
import pandas as pd
from scipy.stats import spearmanr

def make_csv(dir, data):
    # データフレーム化
    df_results = pd.DataFrame(data)

    # 全体の平均行を作成
    ave = pd.DataFrame([{
        "id": "ave",
        "correlation": df_results["correlation"].mean(),
        "pvalue": df_results["pvalue"].mean()
    }])

    # 最終結果の結合
    final_df = pd.concat([ave,df_results], ignore_index=True)
    final_df.to_csv(dir, index=False, encoding="utf-8")

def calculate_correlation(id, user, llm):
    # データの準備
    user = user.values.flatten()
    llm = llm.values.flatten()
    # 相関係数を計算する
    corr1, pval1 = spearmanr(user, llm)
    results = [
        {
            "id": id,
            "correlation": corr1,
            "pvalue": pval1
        }
    ]
    return results

def corr(ids, load_dir, save_dir):
    data = []
    for id in ids:
        csv = pd.read_csv(f"{load_dir}/{id}.csv", encoding="utf-8")
        # tipiのcorrelation
        user = csv[csv["回答者"] == "user"].drop(columns=["回答者"])
        llm = csv[csv["回答者"] == "llm"].drop(columns=["回答者"])
        data += calculate_correlation(
            user=user,
            llm=llm,
            id=id
        )
    # csvファイルで保存する
    make_csv(save_dir, data)

ids = [
    "01","02","03","04","05","06","07","08","09","10",
    "11","12","13","14","15","16","17","18","19","20",
    "21","22","23","24","25","26","27","28","29"
]
#model = "Gemini"
model = "GPT"
#model = "Grok"
#J_S = "JSON_nofig"
J_S = "Story_nofig"
# TIPIの相関係数を計算して保存する
corr(
    ids,
    load_dir=f"{model}/TIPI/Tend/{J_S}",
    save_dir=f"{model}/TIPI/Corr/{J_S}.csv"
)
# PVQの相関係数を計算して保存する
corr(
    ids,
    load_dir=f"{model}/PVQ/Tend/{J_S}",
    save_dir=f"{model}/PVQ/Corr/{J_S}.csv"
)
