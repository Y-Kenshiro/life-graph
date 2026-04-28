import py7zr
import getpass
import os
import json
import tempfile
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Akima1DInterpolator
import textwrap
from adjustText import adjust_text

class Make_prompt():
    def __init__(self, user_id):
        self.user_id = user_id
        self.json_data = self.read_file_in_7z()

    def read_file_in_7z(self):
        archive_path = f"User/Data/survey_result_{self.user_id}.7z"
        target_filename = f"survey_result_{self.user_id}.json"
        if not os.path.exists(archive_path):
            print(f"エラー: ファイルが見つかりません -> {archive_path}")
            return None

        try:
            password = getpass.getpass(".7zファイルのパスワードを入力してください: ")

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

    def save_prompt_to_file(self, prompt_string, save_dir):
        with open(save_dir, "w", encoding="utf-8") as f:
            f.write(prompt_string)

    def demo_info(self):
        json_data = self.json_data
        age = json_data["age"]
        gender = json_data["gender"]
        job = json_data["job"]
        info_string = f"あなたは{age}歳の{gender}で、職業は{job}です。"
        return info_string

    def json_prompt_formatter(self):
        #save_dir = "Prompt/Life_Prompt/Json.txt"
        json_data = self.json_data
        prompt_string = ("""あなたは［人生体験］に書かれている人生を歩んできました。あなたの役割は、与えられた人生を歩んできた人物を演じることです。まず、人生の中であなたの性格や価値観がどのように変化し、確立されていったかを分析してください。分析結果からあなたの性格を2文程度で定義し、与えられたテストに回答してください。
#［人生体験］
""")
        data=[]
        for d in json_data["life"][1:]:
            #d.pop("順番")
            #d.pop("最重要")
            order = ["年齢", "エピソード", "幸福度"]
            sorted = {k: d[k] for k in order if k in d}
            data.append(sorted)
        prompt_string += json.dumps(data, ensure_ascii=False, indent=2)
        #self.save_prompt_to_file(prompt_string, save_dir)
        print("人生体験プロンプトを作成しました！")
        return prompt_string

    def story_prompt_formatter(self):
        #save_dir = "Prompt/Life_prompt/Story.txt"
        json_data = self.json_data
        prompt_string = ("""あなたは［人生体験］に書かれている人生を歩んできました。あなたの役割は、与えられた人生を歩んできた人物を演じることです。まず、人生の中であなたの性格や価値観がどのように変化し、確立されていったかを分析してください。分析結果からあなたの性格を2文程度で定義し、与えられたテストに回答してください。
#［人生体験］
""")
        data = json_data["life"][1:]
        for d in data:
            episode = d["エピソード"].replace('\n','')
            prompt_string += f'{d["年齢"]}歳のとき、{episode}(この時の幸福度:{d["幸福度"]})'
        #self.save_prompt_to_file(prompt_string, save_dir)
        print("人生体験プロンプトを作成しました！")
        return prompt_string

    def life_graph_fig(self):
        # --- 日本語フォントの設定 ---
        # Matplotlibで日本語を表示するための設定
        # ご自身のPCにインストールされているフォントを指定してください (例: 'MS Gothic', 'Meiryo', 'Hiragino Sans')
        plt.rcParams['font.family'] = 'Yu Gothic'
        plt.rcParams['axes.unicode_minus'] = False # マイナス記号の文字化けを防ぐ

        # --- グラフにプロットする人生の出来事データ ---
        # データを年齢、幸福度、ラベルに分割
        data = self.json_data["life"]
        ages = []
        happiness = []
        labels = []
        i = 0
        while i < len(data):
            ages.append(data[i]["年齢"])
            happy = []
            label = []
            important = 0
            happy.append(data[i]["幸福度"])
            label.append(data[i]["エピソード"].split("。")[0])
            while i+1 < len(data) and data[i]["年齢"] == data[i+1]["年齢"]:
                happy.append(data[i+1]["幸福度"])
                label.append(data[i+1]["エピソード"].split("。")[0])
                if str(data[i]["最重要"]) == "true":
                    important = i
                i+=1
            if important == 0:
                happiness.append(sum(happy)/len(happy))
                combined = "。\n".join(label)
                labels.append(combined)
            else:
                happiness.append(data[important]["幸福度"])
                labels.append(data[important]["エピソード"].split("。")[0])
            i+=1
        #print(ages)
        #print(happiness)

        # --- グラフ描画 ---
        fig, ax = plt.subplots(figsize=(14, 8))

        # Akima補間で滑らかな線を作成
        x_smooth = np.linspace(min(ages), max(ages), 300)
        akima_interpolator = Akima1DInterpolator(ages, happiness)
        y_smooth = akima_interpolator(x_smooth)

        # 滑らかな線をプロット
        ax.plot(x_smooth, y_smooth, '-', color='royalblue', linewidth=3, alpha=0.8, label='幸福度の推移')

        # 各イベントの点をプロット
        ax.plot(ages, happiness, 'o', color='darkorange', markersize=12, mec='white', mew=1.5, label='主要な出来事')

        """
        # --- 各イベントにテキストと矢印で注釈を追加（左右配置ロジック付き）---
        annotations = []
        for i, label in enumerate(labels):
            # デフォルトのオフセットと配置
            x_offset = 0
            y_offset = 15
            ha = 'center' # 水平方向の配置
            va = 'bottom' # 垂直方向の配置 (デフォルトは点の上)

            # --- ここからが新しい配置ロジック ---
            # 点がピークか谷かを判定 (最初と最後の点は除く)
            is_peak = (i > 0 and i < len(ages) - 1 and
                        happiness[i] > happiness[i-1] and happiness[i] > happiness[i+1])
            is_valley = (i > 0 and i < len(ages) - 1 and
                        happiness[i] < happiness[i-1] and happiness[i] < happiness[i+1])

            if is_peak:
                # 山（ピーク）の場合：テキストを上に配置
                va = 'bottom'
                y_offset = 15
            elif is_valley:
                # 谷（バレー）の場合：テキストを下に配置
                va = 'top'
                y_offset = -15
            else:
                # 坂の途中の場合：テキストを左右に配置
                va = 'center'
                y_offset = 0

                # 坂の向きを判断して左右を決定
                if i == 0: # 最初の点
                    slope_is_up = happiness[i+1] > happiness[i]
                else: # 2番目以降の点
                    slope_is_up = happiness[i] > happiness[i-1]

                if slope_is_up:
                    # 上り坂の場合：テキストを左に配置
                    ha = 'right'
                    x_offset = -0.5
                else:
                    # 下り坂の場合：テキストを右に配置
                    ha = 'left'
                    x_offset = 0.5

            # 「誕生」のテキストがY軸と重ならないように特別処理
            if ages[i] == 0:
                ha = 'left'
                x_offset = 0.5
                va = 'center'
                y_offset = 0

            if ages[i] ==max(ages):
                ha='left'
                x_offset = 0.5
                va = 'center'
                y_offset = 0

            wrapped_label = textwrap.fill(label, width=6)

            annotations.append(
                ax.annotate(wrapped_label,
                        xy=(ages[i], happiness[i]),
                        xytext=(ages[i] + x_offset, happiness[i] + y_offset),
                        ha=ha,
                        va=va,
                        fontsize=12,
                        arrowprops=dict(arrowstyle="->",
                                        connectionstyle="arc3,rad=0.2",
                                        color="gray",
                                        shrinkB=5
                                    )
                    )
            )
        # adjust_textでラベルの重なりを調整
        adjust_text(annotations, ax=ax, arrowprops=dict(arrowstyle="->", color="gray"))
        #"""
        # --- グラフの装飾 ---
        ax.axhline(0, color='gray', linestyle='--', linewidth=1)
        ax.set_title('人生の幸福度グラフ', fontsize=22, pad=20, weight='bold')
        ax.set_xlabel('年齢', fontsize=20)
        ax.set_ylabel('幸福度', fontsize=20)
        ax.set_xlim(min(ages) - 2, max(ages) + 5)
        ax.set_ylim(-110, 110)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(fontsize=12, loc='lower right')
        ax.tick_params(axis='both', which='major', labelsize=12)
        fig.tight_layout()

        # --- ファイルとして保存 ---
        #plt.savefig('lifeline.png', dpi=300)

        return fig
