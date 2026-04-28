# LLMの出力データをクリーニングするコード
#  整形できてないこともあるので、必ず整形データをチェックする
import getpass
import py7zr
import os
import json
import tempfile
import pandas as pd

def cleaning_que(input_filename):
    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        # 整形後のデータを入れるための新しい辞書
            cleaned_data = {}
        # 各キーとバリューを処理
        for key, value in data.items():
            # バリューが文字列で、JSONコードブロックが含まれているかチェック
            if isinstance(value, str) and "```json" in value:
                # 説明文とJSON文字列部分に分割
                parts = value.split("```json", 1)
                intro_text = parts[0].strip()
                json_string = parts[1].strip()
                # 末尾の ``` 以降を削除
                json_string = json_string.split("\n```", 1)
                json_string = json_string[0].strip()
                # JSON文字列をクリーニング
                json_string = json_string.replace("\n", "").strip()

                # 3. JSON文字列をPythonオブジェクト（リストや辞書）に変換
                try:
                    parsed_json = json.loads(json_string)
                    cleaned_data[key] = parsed_json
                except json.JSONDecodeError as e:
                    print(f"エラー: '{key}' のJSONデータの解析に失敗しました。 - {e}")
                    cleaned_data[key] = value # 失敗した場合は元の値を入れる
            elif isinstance(value,str) and "[\n  {\n" in value:
                json_string = value[value.index("[\n  {\n"):]

                # 3. JSON文字列をPythonオブジェクト（リストや辞書）に変換
                try:
                    parsed_json = json.loads(json_string)
                    cleaned_data[key] = parsed_json
                except json.JSONDecodeError as e:
                    print(f"エラー: '{key}' のJSONデータの解析に失敗しました。 - {e}")
                    cleaned_data[key] = value # 失敗した場合は元の値を入れる
            else:
                # JSONコードブロックが含まれていない場合は、そのままコピー
                cleaned_data[key] = value

        return cleaned_data
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_filename}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

def cleaning_scenario(input_filename):
    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        # 整形後のデータを入れるための新しい辞書
            cleaned_data = {}

        # VALUENETの結果を特別に処理
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
        for i in range(3):
            valuenet_key = f"give_valuenet_{i+1}"
            if valuenet_key in cleaned_data:
                valuenet_results = cleaned_data[valuenet_key]
                for pair_key, pair_value in valuenet_results.items():
                    if isinstance(pair_value, str) and "```json" in pair_value:
                        parts = pair_value.split("```json", 1)
                        intro_text = parts[0].strip()
                        json_string = parts[1].strip()
                        json_string = json_string.split("\n```", 1)[0].strip()
                        json_string = json_string.replace("\n", "").strip()
                        try:
                            parsed_json = json.loads(json_string)
                            valuenet_results[pair_key] = parsed_json
                        except json.JSONDecodeError as e:
                            print(f"エラー: '{pair_key}' のJSONデータの解析に失敗しました。 - {e}")
                            valuenet_results[pair_key] = pair_value
                cleaned_data[valuenet_key] = valuenet_results
        return cleaned_data
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_filename}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

def read_file_in_7z(user_id):
        archive_path = f"User/Data/survey_result_{user_id}.7z"
        target_filename = f"survey_result_{user_id}.json"
        if not os.path.exists(archive_path):
            print(f"エラー: ファイルが見つかりません -> {archive_path}")
            return None

        try:
            password = getpass.getpass(".7zファイルのパスワードを入力してください: ")

            with tempfile.TemporaryDirectory() as tmpdir:
                with py7zr.SevenZipFile(archive_path, mode='r', password=password) as z:
                    print(f"'{target_filename}' を展開しています...")
                    z.extract(targets=[target_filename], path=tmpdir)

                # 展開されたファイルを確認
                extracted_path = os.path.join(tmpdir, target_filename)
                if not os.path.exists(extracted_path):
                    print(f"\nエラー: {target_filename} がアーカイブ内に存在しません。")
                    return None

                # JSONを読み込む
                with open(extracted_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    print("JSONデータの読み込みに成功しました！")
                    return json_data

        except py7zr.exceptions.PasswordRequired:
            print("\nエラー: このファイルはパスワードで保護されています。")
        except py7zr.exceptions.Bad7zFile:
            print("\nエラー: パスワードが間違っているか、ファイルが破損しています。")
        except Exception as e:
            print(f"\n予期せぬエラーが発生しました: {e}")
        return None

def extract_user_answer(ids):
    for user_id in ids:
        user_data = read_file_in_7z(user_id)
        user_answer = {}
        # 辞書リストをDataFrameに変換
        df_tipi = pd.DataFrame(user_data["tipi"])
        df_pvq = pd.DataFrame(user_data["pvq"])

        # 列名（キー）を一括でリネーム
        df_tipi = df_tipi.rename(columns={"rating": "answer"})
        df_pvq = df_pvq.rename(columns={"rating": "answer"})

        # 必要ならまた辞書リストに戻す
        user_answer["tipi"] = df_tipi.to_dict(orient="records")
        user_answer["pvq"] = df_pvq.to_dict(orient="records")

        output_filename = f"User/Answer/{user_id}.json"
        # 整形したデータを新しいJSONファイルに書き込む
        with open(output_filename, "w", encoding="utf-8") as f:
            # indent=2 で見やすく整形、ensure_ascii=False で日本語の文字化けを防ぐ
            json.dump(user_answer, f, ensure_ascii=False, indent=2)

        print(f"処理が完了しました！ '{output_filename}' を確認してください。")

def extract_llm_answer_que(model, J_S, ids):
    for id in ids:
        input_filename = f"{model}/Data/{J_S}/{id}-question.json"
        output_filename = f"{model}/CleanedData/{J_S}/{id}-question.json"
        cleaned_data = {}
        cleaned_data.update(cleaning_que(input_filename))
        # 整形したデータを新しいJSONファイルに書き込む
        with open(output_filename, "w", encoding="utf-8") as f:
            # indent=2 で見やすく整形、ensure_ascii=False で日本語の文字化けを防ぐ
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

        print(f"処理が完了しました！ '{output_filename}' を確認してください。")

def extract_llm_answer_scenario(model, J_S, ids):
    for id in ids:
        input_filename = f"{model}/Data/{J_S}/{id}-scenario.json"
        output_filename = f"{model}/CleanedData/{J_S}/{id}-scenario.json"
        cleaned_data = {}
        cleaned_data.update(cleaning_scenario(input_filename))
        # 整形したデータを新しいJSONファイルに書き込む
        with open(output_filename, "w", encoding="utf-8") as f:
            # indent=2 で見やすく整形、ensure_ascii=False で日本語の文字化けを防ぐ
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

        print(f"処理が完了しました！ '{output_filename}' を確認してください。")

#model = "Gemini"
#model = "GPT"
model = "Grok"
#ids = ["01"]
#ids = ["02","03","04","05","06","07","08","09","10"]
#ids = ["11","12","13","14","15","16","17","18","19","20"]
#ids = ["21","22","23","24","25","26","27","28","29"]
ids = [
    #"01","02","03","04","05","06","07","08","09","10",
    #"11","12","13","14","15","16","17","18","19","20",
    #"21","22","23","24","25","26","27","28","29"
    "20"
]

#extract_user_answer(ids=ids)
extract_llm_answer_que(model=model, J_S="JSON_nofig", ids=ids)
extract_llm_answer_que(model=model, J_S="Story_nofig", ids=ids)