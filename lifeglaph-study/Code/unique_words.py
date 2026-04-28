# 特徴語の抽出
import json
from collections import Counter
import csv
import MeCab
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import py7zr
import getpass
import os
import tempfile

# 単語の出現頻度をカウントする関数
def count_word_frequency(text):
    # MeCabのパーサーを初期化
    tagger = MeCab.Tagger()

    # 形態素解析を実行
    node = tagger.parseToNode(text)

    words = []
    while node:
        # 品詞情報を取得
        feature = node.feature.split(',')
        pos = feature[0] # 品詞（名詞、動詞など）

        # 内容語を抽出
        if pos in ['名詞', '動詞', '形容詞', '副詞']:
            words.append(node.surface)

        node = node.next

    # 出現回数をカウント
    return Counter(words)

def read_file_in_7z(user_id):
    archive_path = f"User/Data/survey_result_{user_id}.7z"
    target_filename = f"survey_result_{user_id}.json"
    if not os.path.exists(archive_path):
        print(f"エラー: ファイルが見つかりません -> {archive_path}")
        return None

    try:
        #password = getpass.getpass(".7zファイルのパスワードを入力してください: ")
        password = "Dk2sD@0421mf17"

        with tempfile.TemporaryDirectory() as tmpdir:
            with py7zr.SevenZipFile(archive_path, mode='r', password=password) as z:
                #print(f"'{target_filename}' を展開しています...")
                z.extract(targets=[target_filename], path=tmpdir)

            # 展開されたファイルを確認
            extracted_path = os.path.join(tmpdir, target_filename)
            if not os.path.exists(extracted_path):
                print(f"\nエラー: {target_filename} がアーカイブ内に存在しません。")
                return None

            # JSONを読み込む
            with open(extracted_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                #print("Userデータの読み込みに成功しました！")
                return json_data

    except py7zr.exceptions.PasswordRequired:
        print("\nエラー: このファイルはパスワードで保護されています。")
    except py7zr.exceptions.Bad7zFile:
        print("\nエラー: パスワードが間違っているか、ファイルが破損しています。")
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
    return None

def main_tipi(model, j_s, id):
    # JSONファイルの読み込み
    user = read_file_in_7z(user_id=id)
    episodes = user["life"]
    # CSVファイルの読み込み
    file_path = f"{model}/TIPI/Episode/{j_s}/{id}.csv"
    with open(file_path, encoding="utf-8") as f:
        df = pd.read_csv(file_path, encoding="utf-8")

    # 頻出度分析
    results = {
        "外向性": [],
        "協調性": [],
        "勤勉性": [],
        "神経症傾向": [],
        "開放性": []
    }
    llm = pd.DataFrame(df[df["回答者"] == "llm"].drop(columns=["回答者"]))
    for column in llm.columns:
        ages = llm[column].values[0]
        ages = list(ages)
        episode = [item for item in episodes if item.get("年齢") in ages]
        results[column] += count_word_frequency(episode)

    # 結果をCSV形式で保存
    output_csv = f"{model}/TIPI/Word/{j_s}/{id}.csv"
    with open(output_csv, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Word", "Frequency"])  # ヘッダー行
        for question, freq in results.items():
            for word, count in freq.items():
                writer.writerow([question, word, count])

def main_pvq(model, j_s, id):
    # JSONファイルの読み込み
    user = read_file_in_7z(user_id=id)
    episodes = user["life"]
    # CSVファイルの読み込み
    file_path = f"{model}/PVQ/Episode/{j_s}/{id}.csv"
    with open(file_path, encoding="utf-8") as f:
        df = pd.read_csv(file_path, encoding="utf-8")

    # 頻出度分析
    results = {
        "AC": [], "BE": [], "CO": [], "HE": [], "PO": [],
        "SE": [], "SD": [], "ST": [], "TR": [], "UN": []
    }
    llm = pd.DataFrame(df[df["回答者"] == "llm"].drop(columns=["回答者"]))
    for column in llm.columns:
        ages = llm[column].values[0]
        ages = list(ages)
        episode = [item for item in episodes if item.get("年齢") in ages]
        results[column] += count_word_frequency(episode)

    # 結果をCSV形式で保存
    output_csv = f"{model}/PVQ/Word/{j_s}/{id}.csv"
    with open(output_csv, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Word", "Frequency"])  # ヘッダー行
        for question, freq in results.items():
            for word, count in freq.items():
                writer.writerow([question, word, count])

def summary(dir):
    # 1. 読み込むファイルがあるディレクトリを指定（ここではカレントディレクトリ）
    # 例: "Survey/word_freq/*.csv" のように指定
    path = f"{dir}*.csv"
    files = glob.glob(path)

    all_data = []

    for file in files:
        # ファイル名からIDを取得 (例: "01.csv" -> "01")
        file_name = os.path.basename(file)
        file_id = os.path.splitext(file_name)[0]
        # 数値のみのIDファイル（01.csvなど）だけを対象にする場合のフィルタ
        if not file_id.isdigit():
            continue

        # CSVの読み込み
        df = pd.read_csv(file)

        # ID列を先頭に追加
        df.insert(0, 'ID', file_id)

        all_data.append(df)

    # すべてのデータを結合
    combined_df = pd.concat(all_data, ignore_index=True)

    # 統合したCSVを保存
    combined_df.to_csv(f"{dir}all_word_frequencies.csv", index=False, encoding="utf-8-sig")

    print(f"{len(files)}件のファイルを統合し、all_word_frequencies.csv を作成しました。")

def summary_graph(dir, ids, title):
    # --- 1. マッピングの定義 (質問文からカテゴリへ) ---
    # ※実際のCSV内の質問文と完全に一致させる必要があります
    mapping = {
        # PVQ (10の価値観)
        "自己決定": ["ある人は、自分なりの意見を形作ることを大事にしている。", "ある人は、自分の考えを確立することを大事にしている 。", "ある人は、物事を自分で何とかすることを大事にしている。", "ある人は、自分の人生は自分で決断するということを大事にしている。", "ある人は、自立して行動を計画することを大事にしている。", "ある人は、やることを自分で自由に選択できることを大事にしている。"],
        "普遍主義": ["ある人は、自然を大切にすることを大事にしている。", "ある人は、自然を守るための活動に参加することを大事にしている。", "ある人は、自然環境を 破壊や汚染から守ることを大事にしている。", "ある人は、社会の中で弱く傷つきやすい人々が守られることを大事にしている。", "ある人は、世界のすべての人々が人生において平等な機会をもつことを大事にしている。", "ある人は、たとえ自分の知らない人であっても、誰もが公正に扱われることを大事にしている。", "ある人は、あらゆる人達や集団に対して寛容であることを大事にしている。", "ある人は、自分とは違う人の言うことに耳を傾け、理解する事を大事にしている。", "ある人は、たとえ自分と意見が反対の立場の人であっても、その人を受け入れることを大事にしている。"],
        "博愛": ["ある人は、親しい人の世話をすることを大事にしている。", "ある人は、自分の大切な人を助けることをとても大事にしている。", "ある人は、自分の大 切な人が必要とする全てのことに携わることを大事にしている 。", "ある人は、知り合いから絶対の信頼を置かれることを大事にしている。", "ある人は 、信頼され、頼られる友人となることを大事にしている。", "ある人は、すべての友人や家族が自分に絶対の信頼を寄せられることを大事にしている。"],
        "安全": ["ある人は、病気を避け、健康を守ることをとても大事にしている。", "ある人は、自分の身が安全で守られていることを大事にしている。", "ある人は、 いかなる危険も避けることを大事にしている。", "ある人は、自分の国が安全で安定していることを大事にしている。", "ある人は、いかなる危険も避けることを大事にしている。", "ある人は、自分の国がすべての脅威から自国を守ることを大事にしている。"],
        "協調": ["ある人は、規則や規定を決して破らないことを大事にしている。", "ある人は、誰も見ていない時でも規則を守ることを大事にしている。", "ある人は、 いかなる法律も遵守することを大事にしている 。", "ある人は、人を困らせないことを大事にしている。", "ある人は、人を決して苛立たせないことを大 事にしている。", "ある人は、決して人を怒らせないことを大事にしている。"],
        "伝統": ["ある人は、伝統的な価値観や物の考え方を持ち続けることを大事にしている。", "ある人は、家族の習慣や宗教のしきたりに従うことを大事にしている。", "ある人は、自身の文化に関する伝統的なしきたりを重んじることを大事にしている。", "ある人は、自分が他の人より価値があるとは決して考えないこ とを大事にしている。", "ある人は、謙虚であることを大事にしている。", "ある人は、今あるものに満足し、それ以上を求めないことを大事にしている。"],
        "達成": ["ある人は、人生において野心をもつことを大事にしている。", "ある人は、大きな成功を収めることを大事にしている。", "ある人は、自分の功績を人々 が認めることを大事にしている。"],
        "権力": ["ある人は、自分が言った通りに人が動くことを大事にしている。", "ある人は、自分の望むことを他の人にさせる権力をもつことを大事にしている。", "ある人は、周囲の人にやるべきことを指示する立場であることを大事にしている。", "ある人は、お 金がもたらす権力を手に入れることを大事にしている。", "ある人は、裕福であることを大事にしている。", "ある人は、自分 の富が分かる高価なものをもつことを大事にしている。"],
        "快楽主義": ["ある人は、楽しい時間を過ごすことを大事にしている。", "ある人は、人生の喜びを味わうことを大事にしている。", "ある人は、あらゆる機会を利用して楽しむことを大事にしている。"],
        "刺激": ["ある人は、いつも何か新しくやる事を探すことを大事にしている。", "ある人は、人生を刺激的にするようなリスクを負うことを大事にしている 。", "ある人は、あらゆる種類の新しい経験をすることを大事にしている。"],

        # TIPI-J (5つの性格特性)
        "外向性": ["活発で、外交的だと思う", "ひかえめで、おとなしいと思う"],
        "協調性": ["他人に不満をもち、もめごとを起こしやすいと思う", "人に気をつかう、やさしい人間だと思う"],
        "勤勉性": ["しっかりしていて、自分に厳しいと思う", "だらしなく、うっかりしていると思う"],
        "神経症傾向": ["心配性で、うろたえやすいと思う", "冷静で、気分が安定していると思う"],
        "開放性": ["新しいことが好きで、変わった考えをもつと思う", "発想力に欠けた、平凡な人間だと思う"]
    }

    # 逆引き辞書の作成 (質問文 -> カテゴリ名)
    q_to_cat = {q: cat for cat, qs in mapping.items() for q in qs}

    # 2. 全CSVデータの読み込み
    all_files = glob.glob(os.path.join(dir, "*.csv"))
    selected_files = [f for f in all_files if any(id_str in os.path.basename(f) for id_str in ids)]
    data_list = []

    for f in selected_files:
        df = pd.read_csv(f)
        # カテゴリを紐付け (質問文の末尾の空白などを考慮してstrip()を入れると安全)
        df['Category'] = df['Question'].str.strip().map(q_to_cat)
        data_list.append(df)

    if not data_list:
        print("ファイルが見つかりません。")
        return

    full_df = pd.concat(data_list, ignore_index=True)

    # 3. カテゴリ・単語ごとに合計頻度を計算
    agg_df = full_df.groupby(['Category', 'Word'])['Frequency'].sum().reset_index()

    # 4. カテゴリごとにグラフを作成・保存
    plt.rcParams['font.family'] = 'MS Gothic' # Windows用 (MacはHiragino Sans等)

    categories = agg_df['Category'].dropna().unique()
    for cat in categories:
        # そのカテゴリの上位15単語を取得
        cat_data = agg_df[agg_df['Category'] == cat].sort_values(by='Frequency', ascending=False).head(15)

        plt.figure(figsize=(10, 6))
        plt.barh(cat_data['Word'], cat_data['Frequency'], color='teal')
        plt.xlabel('合計出現頻度')
        plt.title(f'カテゴリ: {cat}')
        plt.gca().invert_yaxis() # 頻度順に上から並べる
        plt.tight_layout()

        # 保存
        plt.savefig(f"{dir}{title}_word_freq_{cat}.png")
        plt.close()
        print(f"Graph saved: {title}_word_freq_{cat}.png")

ids = [
    "01","02","03","04","05","06","07","08","09","10",
    "11","12","13","14","15","16","17","18","19","20",
    "21","22","23","24","25","26","27","28","29"
]
models = ["Gemini", "GPT", "Grok"]
J_S = ["JSON_nofig", "Story_nofig"]

for model in models:
    for j_s in J_S:
        # 語彙ファイルを作成する
        for id in ids:
            main_tipi(model, j_s, id)
            main_tipi(model, j_s, id)
            main_pvq(model, j_s, id)
            main_pvq(model, j_s, id)