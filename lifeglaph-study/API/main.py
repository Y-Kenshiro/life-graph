from GetData import GetData, GetDataSub

def main_que(model, id, figure=False, demo_info=False):
    print("JSON形式プロンプト")
    settings = {
        "model": model,
        "user_id": id,
        "life_prompt_type": "JSON",
        "demo_info": demo_info,
        "figure": figure,
    }
    GetData(settings).result_question()
    print("終了")
    print("Story形式プロンプト")
    settings["life_prompt_type"] = "Story"
    GetData(settings).result_question()
    print("終了")

# 以下2つは個別呼び出し
def sub_tipi(id):
    print("Json形式プロンプト")
    settings = {
        "user_id": id,
        "life_prompt_type": "Json",
        "demo_info": False,
        "figure": False,
    }
    GetDataSub(settings).tipi_result()
    print("終了")
    print("Story形式プロンプト")
    settings["life_prompt_type"] = "Story"
    GetDataSub(settings).tipi_result()
    print("終了")

def sub_pvq(id):
    print("Json形式プロンプト")
    settings = {
        "user_id": id,
        "life_prompt_type": "Json",
        "demo_info": False,
        "figure": True,
    }
    GetDataSub(settings).pvq_result()
    print("終了")
    print("Story形式プロンプト")
    settings["life_prompt_type"] = "Story"
    GetDataSub(settings).pvq_result()
    print("終了")

# API呼び出し
# 質問紙テストのみ
#model = "Gemini"
#model = "GPT"
model = "Grok"
#ids = ["01"] # まずは動作確認用に1つだけ実行
#ids = ["02","03","04","05","06","07","08","09","10"]
#ids = ["11","12","13","14","15","16","17","18","19","20"]
#ids = ["21","22","23","24","25","26","27","28","29"]
ids = ["20"]
for id in ids:
    print("id: " + id)
    main_que(model=model, id=id, figure=False, demo_info=False)

# シナリオ選択テスト
"""
ids = ["01","02","03","04","05","06","07","08","09","10"]
#ids = ["11","12","13","14","15","16","17","18","19","20"]
#ids = ["21","22","23","24","25","26","27","28","29"]
for id in ids:
    print("id: " + id)
    main_que(model="Gemini", id=id, figure=True, demo_info=False)
#"""