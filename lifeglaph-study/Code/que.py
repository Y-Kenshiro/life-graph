# ユーザーの回答とLLMの平均回答をまとめる
import json
import pandas as pd
import numpy as np

def load_files(model, J_S, user_id):
    # 参加者データを読み込む
    user_file = f"User/Answer/{user_id}.json"
    with open(user_file, "r", encoding="utf-8") as f:
        user_data = json.load(f)
    # LLMデータを読み込む
    llm_file = f"{model}/CleanedData/{J_S}/{user_id}-question.json"
    with open(llm_file, "r", encoding="utf-8") as f:
        llm_data = json.load(f)
    return user_data, llm_data

def que_ans(result):
    changed = {}
    for r in result:
        changed[r["question"]] = r["answer"]
    return changed

def tipi_result(model, J_S, user_id):
        user_data, llm_data = load_files(model, J_S, user_id)
        summary = []
        user = {"回答者": "user"}
        user.update(que_ans(user_data["tipi"]))
        summary.append(user)
        llm_tipis = []
        for i in range(1,4):
            llm_tipis.append(que_ans(llm_data[f"give_tipi_{i}"]))
        llm_mean = {"回答者": "llm"}
        llm_mean.update({key: np.mean([llm_tipis[i][key] for i in range(3)]) for key in llm_tipis[0].keys()})
        summary.append(llm_mean)

        save_dir = f"{model}/TIPI/Que/{J_S}/{user_id}.csv"
        df = pd.DataFrame(summary)
        df.to_csv(save_dir, index=False, encoding="utf-8")

def pvq_result(model="Gemini", J_S="JSON_nofig", user_id="01"):
    user_data, llm_data = load_files(model, J_S, user_id)
    summary = []
    user = {"回答者": "user"}
    user.update(que_ans(user_data["pvq"]))
    summary.append(user)
    llm_tipis = []
    for i in range(1,4):
        llm_tipis.append(que_ans(llm_data[f"give_pvq_{i}"]))
    llm_mean = {"回答者": "llm"}
    llm_mean.update({key: np.mean([llm_tipis[i][key] for i in range(3)]) for key in llm_tipis[0].keys()})
    summary.append(llm_mean)

    save_dir = f"{model}/PVQ/Que/{J_S}/{user_id}.csv"
    df = pd.DataFrame(summary)
    df.to_csv(save_dir, index=False, encoding="utf-8")

#model = "Gemini"
model = "GPT"
#model = "Grok"
#ids = ["01"] # まずは動作確認用に1つだけ実行
#ids = ["02","03","04","05","06","07","08","09","10"]
#ids = ["11","12","13","14","15","16","17","18","19","20"]
#ids = ["21","22","23","24","25","26","27","28","29"]
ids = [
    "01","02","03","04","05","06","07","08","09","10",
    "11","12","13","14","15","16","17","18","19","20",
    "21","22","23","24","25","26","27","28","29"
]
for id in ids:
    try:
        tipi_result(model=model, J_S="JSON_nofig", user_id=id)
        pvq_result(model=model, J_S="JSON_nofig", user_id=id)
    except Exception as e:
        print("JSON" + id)
        print(e)
    try:
        tipi_result(model=model, J_S="Story_nofig", user_id=id)
        pvq_result(model=model, J_S="Story_nofig", user_id=id)
    except Exception as e:
        print("Story" + id)
        print(e)
