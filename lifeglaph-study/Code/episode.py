# reasonに含まれるエピソードを取り出す。
import json
import numpy as np
import pandas as pd
import re

def load_file(model, J_S, user_id):
    load_file_name = f"{model}/CleanedData/{J_S}/{user_id}-question.json"
    with open(load_file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def tipi_episode(result):
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
            "外向性": [],
            "協調性": [],
            "勤勉性": [],
            "神経症傾向": [],
            "開放性": []
        }
        for t in result:
            for item in tipi:
                if t["question"] == item["question"]:
                    reason = t["reason"]
                    ages = re.findall(r"(\d{1,2})歳", reason)
                    counter[item["domain"]].extend(int(age) for age in ages)
        return counter

def tipi_result(model="Gemini", J_S="JSON_nofig", ids=[]):
    for user_id in ids:
        data = load_file(model, J_S, user_id)
        tipis = []
        for i in range(1,4):
            tipi = {}
            tipi["回答者"] = f"{i}"
            tipi.update(tipi_episode(data[f"give_tipi_{i}"]))
            tipis.append(tipi)
        tipi = {"回答者": "llm"}
        for key in ["外向性", "協調性", "勤勉性", "神経症傾向", "開放性"]:
            # 各リストの共通部分を取得
            common_values = set(tipis[0][key]).intersection(tipis[1][key], tipis[2][key])
            tipi[key] = list(common_values) if common_values else None  # 共通部分がない場合は None
        tipis.append(tipi)

        save_dir = f"{model}/TIPI/Episode/{J_S}/{user_id}.csv"
        df = pd.DataFrame(tipis)
        df.to_csv(save_dir, index=False, encoding="utf-8")

def pvq_episode(result):
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
        counter = {
            "AC": [], "BE": [], "CO": [], "HE": [], "PO": [],
            "SE": [], "SD": [], "ST": [], "TR": [], "UN": []
        }
        for p in result:
            for item in pvq:
                if p["question"] == item["question"]:
                    reason = p["reason"]
                    ages = re.findall(r"(\d{1,2})歳", reason)
                    counter[item["value"]].extend(int(age) for age in ages)
        return counter

def pvq_result(model="Gemini", J_S="JSON_nofig", ids=[]):
    for user_id in ids:
        llm_data = load_file(model, J_S, user_id)
        pvqs = []
        for i in range(1,4):
            pvq = {}
            pvq["回答者"] = f"{i}"
            pvq.update(pvq_episode(llm_data[f"give_pvq_{i}"]))
            pvqs.append(pvq)
        pvq = {"回答者": "llm"}
        for key in ["AC", "BE", "CO", "HE", "PO", "SE", "SD", "ST", "TR", "UN"]:
            # 各リストの共通部分を取得
            common_values = set(pvqs[0][key]).intersection(pvqs[1][key], pvqs[2][key])
            pvq[key] = list(common_values) if common_values else None  # 共通部分がない場合は None
        pvqs.append(pvq)

        save_dir = f"{model}/PVQ/Episode/{J_S}/{user_id}.csv"
        df = pd.DataFrame(pvqs)
        df.to_csv(save_dir, index=False, encoding="utf-8")

ids = [
    "01","02","03","04","05","06","07","08","09","10",
    "11","12","13","14","15","16","17","18","19","20",
    "21","22","23","24","25","26","27","28","29"
]
models = ["Gemini", "GPT", "Grok"]
J_S = ["JSON_nofig", "Story_nofig"]

for model in models:
    for type in J_S:
        tipi_result(model=model, J_S=type, ids=ids)
        pvq_result(model=model, J_S=type, ids=ids)