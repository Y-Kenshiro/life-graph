# 性格特性・価値観傾向の計算
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

def tipi_tend(result):
        tipi = [
            {"question": "活発で、外向的だと思う", "domain": "外向性", "reverse": False},
            {"question": "他人に不満をもち、もめごとを起こしやすいと思う", "domain": "協調性", "reverse": True},
            {"question": "しっかりしていて、自分に厳しいと思う", "domain": "勤勉性", "reverse": False},
            {"question": "心配性で、うろたえやすいと思う", "domain": "神経症傾向", "reverse": False},
            {"question": "新しいことが好きで、変わった考えをもつと思う", "domain": "開放性", "reverse": False},
            {"question": "ひかえめで、おとなしいと思う", "domain": "外向性", "reverse": True},
            {"question": "人に気をつかう、やさしい人間だと思う", "domain": "協調性", "reverse": False},
            {"question": "だらしなく、うっかりしていると思う", "domain": "勤勉性", "reverse": True},
            {"question": "冷静で、気分が安定していると思う", "domain": "神経症傾向", "reverse": True},
            {"question": "発想力に欠けた、平凡な人間だと思う", "domain": "開放性", "reverse": True}
        ]
        counter = {
            "外向性": 0,
            "協調性": 0,
            "勤勉性": 0,
            "神経症傾向": 0,
            "開放性": 0
        }
        for t in result:
            for item in tipi:
                if t["question"] == item["question"]:
                    rating = t["answer"]
                    if item["reverse"]:
                        rating = 8 - rating
                    counter[item["domain"]] += rating
        return counter

def tipi_result(model="Gemini", J_S="JSON_nofig", ids=[]):
    for user_id in ids:
        user_data, llm_data = load_files(model, J_S, user_id)
        tipis = []
        tipi = {"回答者": "user"}
        tipi.update(tipi_tend(user_data["tipi"]))
        tipis.append(tipi)
        llm_tipis = []
        for i in range(1,4):
            tipi = {}
            tipi["回答者"] = f"{i}"
            tipi.update(tipi_tend(llm_data[f"give_tipi_{i}"]))
            tipis.append(tipi)
            llm_tipis.append(tipi)
        tipi = {"回答者": "llm"}
        for key in ["外向性", "協調性", "勤勉性", "神経症傾向", "開放性"]:
            tipi[key] = np.mean([llm_tipis[i][key] for i in range(3)])
        tipis.append(tipi)

        save_dir = f"{model}/TIPI/Tend/{J_S}/{user_id}.csv"
        df = pd.DataFrame(tipis)
        df.to_csv(save_dir, index=False, encoding="utf-8")

def pvq_tend(result):
        pvq = [
            {"question": "ある人は、自分なりの意見を形作ることを大事にしている。", "value": "SD"},
            {"question": "ある人は、自分の国が安全で安定していることを大事にしている。", "value": "SE"},
            {"question": "ある人は、楽しい時間を過ごすことを大事にしている。", "value": "HE"},
            {"question": "ある人は、人を困らせないことを大事にしている。", "value": "CO"},
            {"question": "ある人は、社会の中で弱く傷つきやすい人々が守られることを大事にしている。", "value": "UN"},
            {"question": "ある人は、自分が言った通りに人が動くことを大事にしている。", "value": "PO"},
            {"question": "ある人は、自分が他の人より価値があるとは決して考えないことを大事にしている。", "value": "TR"},
            {"question": "ある人は、自然を大切にすることを大事にしている。", "value": "UN"},
            {"question": "ある人は、いつも何か新しくやる事を探すことを大事にしている。", "value": "ST"},
            {"question": "ある人は、親しい人の世話をすることを大事にしている。", "value": "BE"},
            {"question": "ある人は、お金がもたらす権力を手に入れることを大事にしている。", "value": "PO"},
            {"question": "ある人は、病気を避け、健康を守ることをとても大事にしている。", "value": "SE"},
            {"question": "ある人は、あらゆる人達や集団に対して寛容であることを大事にしている。", "value": "UN"},
            {"question": "ある人は、規則や規定を決して破らないことを大事にしている。", "value": "CO"},
            {"question": "ある人は、自分の人生は自分で決断するということを大事にしている。", "value": "SD"},
            {"question": "ある人は、人生において野心をもつことを大事にしている。", "value": "AC"},
            {"question": "ある人は、伝統的な価値観や物の考え方を持ち続けることを大事にしている。", "value": "TR"},
            {"question": "ある人は、知り合いから絶対の信頼を置かれることを大事にしている。", "value": "BE"},
            {"question": "ある人は、裕福であることを大事にしている。", "value": "PO"},
            {"question": "ある人は、自然を守るための活動に参加することを大事にしている。", "value": "UN"},
            {"question": "ある人は、人を決して苛立たせないことを大事にしている。", "value": "CO"},
            {"question": "ある人は、自分の考えを確立することを大事にしている 。", "value": "SD"},
            {"question": "ある人は、自分の大切な人を助けることをとても大事にしている。", "value": "BE"},
            {"question": "ある人は、自分の身が安全で守られていることを大事にしている。", "value": "SE"},
            {"question": "ある人は、信頼され、頼られる友人となることを大事にしている。", "value": "BE"},
            {"question": "ある人は、人生を刺激的にするようなリスクを負うことを大事にしている 。", "value": "ST"},
            {"question": "ある人は、自分の望むことを他の人にさせる権力をもつことを大事にしている。", "value": "PO"},
            {"question": "ある人は、自立して行動を計画することを大事にしている。", "value": "SD"},
            {"question": "ある人は、誰も見ていない時でも規則を守ることを大事にしている。", "value": "CO"},
            {"question": "ある人は、大きな成功を収めることを大事にしている。", "value": "AC"},
            {"question": "ある人は、家族の習慣や宗教のしきたりに従うことを大事にしている。", "value": "TR"},
            {"question": "ある人は、自分とは違う人の言うことに耳を傾け、理解する事を大事にしている。", "value": "UN"},
            {"question": "ある人は、人生の喜びを味わうことを大事にしている。", "value": "HE"},
            {"question": "ある人は、世界のすべての人々が人生において平等な機会をもつことを大事にしている。", "value": "UN"},
            {"question": "ある人は、謙虚であることを大事にしている。", "value": "TR"},
            {"question": "ある人は、物事を自分で何とかすることを大事にしている。", "value": "SD"},
            {"question": "ある人は、自身の文化に関する伝統的なしきたりを重んじることを大事にしている。", "value": "TR"},
            {"question": "ある人は、周囲の人にやるべきことを指示する立場であることを大事にしている。", "value": "PO"},
            {"question": "ある人は、いかなる法律も遵守することを大事にしている 。", "value": "CO"},
            {"question": "ある人は、あらゆる種類の新しい経験をすることを大事にしている。", "value": "ST"},
            {"question": "ある人は、自分の富が分かる高価なものをもつことを大事にしている。", "value": "PO"},
            {"question": "ある人は、自然環境を破壊や汚染から守ることを大事にしている。", "value": "UN"},
            {"question": "ある人は、あらゆる機会を利用して楽しむことを大事にしている。", "value": "HE"},
            {"question": "ある人は、自分の大切な人が必要とする全てのことに携わることを大事にしている 。", "value": "BE"},
            {"question": "ある人は、自分の功績を人々が認めることを大事にしている。", "value": "AC"},
            {"question": "ある人は、自分の国がすべての脅威から自国を守ることを大事にしている。", "value": "SE"},
            {"question": "ある人は、決して人を怒らせないことを大事にしている。", "value": "CO"},
            {"question": "ある人は、たとえ自分の知らない人であっても、誰もが公正に扱われることを大事にしている。", "value": "UN"},
            {"question": "ある人は、いかなる危険も避けることを大事にしている。", "value": "SE"},
            {"question": "ある人は、今あるものに満足し、それ以上を求めないことを大事にしている。", "value": "TR"},
            {"question": "ある人は、すべての友人や家族が自分に絶対の信頼を寄せられることを大事にしている。", "value": "BE"},
            {"question": "ある人は、やることを自分で自由に選択できることを大事にしている。", "value": "SD"},
            {"question": "ある人は、たとえ自分と意見が反対の立場の人であっても、その人を受け入れることを大事にしている。", "value": "UN"}
        ]
        que_num = {
            "AC": 3, "BE": 6, "CO": 6, "HE": 3, "PO": 6,
            "SE": 6, "SD": 6, "ST": 3, "TR": 6, "UN": 9
        }
        counter = {
            "AC": 0, "BE": 0, "CO": 0, "HE": 0, "PO": 0,
            "SE": 0, "SD": 0, "ST": 0, "TR": 0, "UN": 0
        }
        rate_sum = 0
        for p in result:
            for item in pvq:
                if p["question"] == item["question"]:
                    rating = p["answer"]
                    counter[item["value"]] += rating
                    rate_sum += rating
        rate_ave = rate_sum / 57
        for key,val in que_num.items():
            counter[key] = (counter[key] / val) - rate_ave
        return counter

def pvq_result(model="Gemini", J_S="JSON_nofig", ids=[]):
    for user_id in ids:
        user_data, llm_data = load_files(model, J_S, user_id)
        pvqs = []
        pvq = {"回答者": "user"}
        pvq.update(pvq_tend(user_data["pvq"]))
        pvqs.append(pvq)
        llm_pvqs = []
        for i in range(1,4):
            pvq = {}
            pvq["回答者"] = f"{i}"
            pvq.update(pvq_tend(llm_data[f"give_pvq_{i}"]))
            pvqs.append(pvq)
            llm_pvqs.append(pvq)
        pvq = {"回答者": "llm"}
        for key in ["AC", "BE", "CO", "HE", "PO", "SE", "SD", "ST", "TR", "UN"]:
            pvq[key] = np.mean([llm_pvqs[i][key] for i in range(3)])
        pvqs.append(pvq)

        save_dir = f"{model}/PVQ/Tend/{J_S}/{user_id}.csv"
        df = pd.DataFrame(pvqs)
        df.to_csv(save_dir, index=False, encoding="utf-8")

"""
def valuenet_tend(valuenet_results):
        pairs = [
            ["un-be", "be-un"], ["un-co", "co-un"], ["un-tr", "tr-un"], ["un-se", "se-un"], ["un-po", "po-un"],
            ["un-ac", "ac-un"], ["un-he", "he-un"], ["un-st", "st-un"], ["un-sd", "sd-un"],
            ["be-co", "co-be"], ["be-tr", "tr-be"], ["be-se", "se-be"], ["be-po", "po-be"], ["be-ac", "ac-be"],
            ["be-he", "he-be"], ["be-st", "st-be"], ["be-sd", "sd-be"],
            ["co-tr", "tr-co"], ["co-se", "se-co"], ["co-po", "po-co"], ["co-ac", "ac-co"], ["co-he", "he-co"],
            ["co-st", "st-co"], ["co-sd", "sd-co"],
            ["tr-se", "se-tr"], ["tr-po", "po-tr"], ["tr-ac", "ac-tr"], ["tr-he", "he-tr"], ["tr-st", "st-tr"],
            ["tr-sd", "sd-tr"],
            ["se-po", "po-se"], ["se-ac", "ac-se"], ["se-he", "he-se"], ["se-st", "st-se"], ["se-sd", "sd-se"],
            ["po-ac", "ac-po"], ["po-he", "he-po"], ["po-st", "st-po"], ["po-sd", "sd-po"],
            ["ac-he", "he-ac"], ["ac-st", "st-ac"], ["ac-sd", "sd-ac"],
            ["he-st", "st-he"], ["he-sd", "sd-he"],
            ["st-sd", "sd-st"]
        ]
        tend = {
            "un": 0, "be": 0, "co": 0, "tr": 0, "se": 0,
            "po": 0, "ac": 0, "he": 0, "st":0 , "sd": 0
        }
        for pair in pairs:
            try:
                result = valuenet_results[f"{pair}"]["selected_scenario"]
                if result[0] == "-":
                    result = result[1:]
                df_1 = pd.read_csv(f"Evaluation_matrix/VALUENET/pairs/{pair[0]}.csv")
                df_2 = pd.read_csv(f"Evaluation_matrix/VALUENET/pairs/{pair[1]}.csv")
                if result in df_1["scenario"].values:
                    tend[pair[0].split("-")[0]] += 1
                    #tend[pair[1].split("-")[0]] -= 1
                elif result in df_2["scenario"].values:
                    tend[pair[1].split("-")[0]] += 1
                    #tend[pair[0].split("-")[0]] -= 1
            except:
                continue
        #print(tend)
        return tend
"""
"""
def valuenet_result(model="Gemini", J_S="JSON_nofig", user_id="01"):
        user_data, llm_data = load_files(model, J_S, user_id)
        valuenets = []
        valuenet = {"回答者": "user"}
        valuenet.update(valuenet_tend(user_data["valuenet"]))
        valuenets.append(valuenet)
        llm_valuenets = []
        for i in range(3):
            valuenet = {}
            valuenet["回答者"] = f"{i}"
            valuenets.append(valuenet_tend(llm_data[f"give_valuenet_{i+1}"]))
            llm_valuenets.append(valuenet_tend(llm_data[f"give_valuenet_{i+1}"]))
        valuenet = {"回答者": "llm"}
        for key in ["AC", "BE", "CO", "HE", "PO", "SE", "SD", "ST", "TR", "UN"]:
            valuenet[key] = np.mean([llm_valuenets[i][key] for i in range(3)])
        valuenets.append(valuenet)

        save_dir = f"{model}/VALUENET/Tend/{J_S}/{user_id}.csv"
        df = pd.DataFrame(valuenets)
        df.to_csv(save_dir, index=False, encoding="utf-8")
"""

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
tipi_result(model=model, J_S="JSON_nofig", ids=ids)
tipi_result(model=model, J_S="Story_nofig", ids=ids)
pvq_result(model=model, J_S="JSON_nofig", ids=ids)
pvq_result(model=model, J_S="Story_nofig", ids=ids)
#valuenet_result(model="Gemini", J_S="JSON_nofig", user_id="01")
