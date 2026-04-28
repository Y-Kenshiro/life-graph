# 性格特性・価値観ごとの平均絶対誤差の計算
#  -> 保存先は"[test]/MAE"
import pandas as pd
from sklearn.metrics import mean_absolute_error

def mae(ids, load_dir, save_dir):
    data = []
    for id in ids:
        csv = pd.read_csv(f"{load_dir}/{id}.csv", encoding="utf-8")
        user = csv[csv["回答者"] == "user"].drop(columns=["回答者"])
        llm = csv[csv["回答者"] == "llm"].drop(columns=["回答者"])
        data.append(
            abs(user.values - llm.values).flatten()
        )
    data = pd.DataFrame(data, columns=user.columns)
    data_mean = data.mean()
    data.loc["average"] = data_mean

    data.to_csv(f"{save_dir}", encoding="utf-8")

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
# TIPI
mae(
    ids,
    load_dir=f"{model}/TIPI/Tend/{J_S}",
    save_dir=f"{model}/TIPI/MAE/{J_S}.csv"
)
# PVQ
mae(
    ids,
    load_dir=f"{model}/PVQ/Tend/{J_S}",
    save_dir=f"{model}/PVQ/MAE/{J_S}.csv"
)