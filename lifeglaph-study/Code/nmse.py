from sklearn.metrics import mean_squared_error
import pandas as pd

def nmse_pvq_valuenet(ids, load_dir1, key1, load_dir2, key2, save_dir):
    nmse = []
    for id in ids:
        pvq = pd.read_csv(f"{load_dir1}/{id}.csv")
        valuenet = pd.read_csv(f"{load_dir2}/{id}.csv")
        # データの抽出
        pvq_user = pvq[pvq["回答者"] == key1].drop(columns=["回答者"])
        val_user = valuenet[valuenet["回答者"] == key2].drop(columns=["回答者"])
        # 正規化
        # pvq_userの正規化
        row_min = pvq_user.min(axis=1)
        row_max = pvq_user.max(axis=1)
        pvq_user = pvq_user.sub(row_min, axis=0).div((row_max - row_min), axis=0)
        # val_userの正規化
        row_min_v = val_user.min(axis=1)
        row_max_v = val_user.max(axis=1)
        val_user = val_user.sub(row_min_v, axis=0).div((row_max_v - row_min_v), axis=0)
        nmse += calculate_mse(
            id=id,
            pvq=pvq_user,
            valuenet=val_user
        )
    data = pd.DataFrame(nmse)
    data_mean = data.mean()
    data.loc["average"] = data_mean

    data.to_csv(f"{save_dir}", encoding="utf-8")

def calculate_mse(id, pvq, valuenet):
    # データの準備
    pvq = pvq.values.flatten()
    valuenet = valuenet.values.flatten()
    # 2乗誤差を計算する
    mse = mean_squared_error(pvq, valuenet)
    results = [
        {
            "id": f"{id}",
            "mse": mse
        },
    ]
    return results

ids = [
    "01",#"02","03","04","05","06","07","08","09","10",
    #"11","12","13","14","15","16","17","18","19","20",
    #"21","22","23","24","25","26","27","28","29"
]
model = "Gemini"
J_S = "JSON_nofig"
nmse_pvq_valuenet(
    ids,
    load_dir1=f"{model}/PVQ/Tend/{J_S}", key1="user",
    load_dir2=f"{model}/ValueNet/Tend/{J_S}", key2="llm",
    save_dir=f"{model}/NMSE/{J_S}.csv"
)