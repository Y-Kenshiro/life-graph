from APICall import GeminiContent, GPTContent, GrokContent
import Make_life as mp
import json
import pandas as pd

class GetData():
    def __init__(self, settings):
        self.settings = settings
        self.user_id = settings["user_id"]
        self.prompt_type = settings["life_prompt_type"]
        self.model = settings["model"]
        self.mp_instance = mp.Make_prompt(user_id=self.user_id)
        if settings["demo_info"]:
            self.life_prompt = self.mp_instance.demo_info() + "\n" + self.get_life_prompt(self.prompt_type)
        else:
            self.life_prompt = self.get_life_prompt(self.prompt_type)
        if settings["figure"]:
            self.fig = self.mp_instance.life_graph_fig()
            self.save_dir = f"{self.model}/Data/{self.prompt_type}_fig/{self.user_id}"
        else:
            self.fig = None
            self.save_dir = f"{self.model}/Data/{self.prompt_type}_nofig/{self.user_id}"
        if self.model == "Gemini":
            self.client = GeminiContent()
        elif self.model == "GPT":
            self.client = GPTContent()
        elif self.model == "Grok":
            self.client = GrokContent()

    def get_life_prompt(self, prompt_type):
        prompt = ""
        if prompt_type == "JSON":
            prompt=self.mp_instance.json_prompt_formatter()
        if prompt_type == "Story":
            prompt=self.mp_instance.story_prompt_formatter()
        return prompt

    def survey_tipi(self):
        result={}
        tipi = """"""
        with open("Prompt/Test_prompt/tipi.txt","r",encoding="utf-8") as f:
            for line in f.readlines():
                tipi += line
        prompt = self.life_prompt + "\n\n" + tipi
        #result["tipi_prompt"] = prompt
        try:
            if self.fig != None:
                fig = self.fig
                result["give_tipi_1"] = self.client.give_test_fig(prompt, fig)
                result["give_tipi_2"] = self.client.give_test_fig(prompt, fig)
                result["give_tipi_3"] = self.client.give_test_fig(prompt, fig)
            else:
                result["give_tipi_1"] = self.client.give_test(prompt)
                result["give_tipi_2"] = self.client.give_test(prompt)
                result["give_tipi_3"] = self.client.give_test(prompt)
        except Exception as e:
            print(e)
            return result
        return result

    def survey_pvq(self):
        result={}
        pvq = """"""
        with open("Prompt/Test_prompt/pvq.txt","r",encoding="utf-8") as f:
            for line in f.readlines():
                pvq += line
        prompt = self.life_prompt + "\n\n" + pvq
        #result["pvq_prompt"] = prompt
        try:
            if self.fig != None:
                fig = self.fig
                result["give_pvq_1"] = self.client.give_test_fig(prompt, fig)
                result["give_pvq_2"] = self.client.give_test_fig(prompt, fig)
                result["give_pvq_3"] = self.client.give_test_fig(prompt, fig)
            else:
                result["give_pvq_1"] = self.client.give_test(prompt)
                result["give_pvq_2"] = self.client.give_test(prompt)
                result["give_pvq_3"] = self.client.give_test(prompt)
        except Exception as e:
            print(e)
            return result
        return result

    def survey_selectscenario(self):
        results = {}
        value1 = [
            "ACH", "BEN", "CON", "HED", "POW",
            "SEC", "SEL", "STI", "TRA", "UNI"
        ]
        value2 = [
            "ACH", "BEN", "CON", "HED", "POW",
            "SEC", "SEL", "STI", "TRA", "UNI"
        ]
        did_pairs = []
        for v1 in value1:
            for v2 in value2:
                if v1 != v2:
                    pair1 = f"{v1}-{v2}"
                    pair2 = f"{v2}-{v1}"
                    if pair1 not in did_pairs and pair2 not in did_pairs:
                        scenario = ""
                        try:
                            df_1 = pd.read_csv(f"Evaluation_matrix/VALUENET/pairs/{pair1}.csv")
                            string_1 = df_1.sample(n=1)["scenario"].replace(["'", '"'],"")
                            string_1 = "".join("scenario1: " + string_1 + "\n")
                            df_2 = pd.read_csv(f"Evaluation_matrix/VALUENET/pairs/{pair2}.csv")
                            string_2 = df_2.sample(n=1)["scenario"].replace(["'", '"'],"")
                            string_2 = "".join("scenario2: " + string_2 + "\n")
                            scenario += string_1 + "\n" + string_2
                            #print(scenario)
                            scenario_prompt = """"""
                            with open("Prompt/Test_prompt/valuenet.txt","r",encoding="utf-8") as f:
                                for line in f.readlines():
                                    scenario_prompt += line
                            scenario_prompt = scenario_prompt + "\n" + scenario
                            prompt = self.life_prompt + "\n\n" + scenario_prompt
                            #result[f"{pair}_prompt"] = pair + [string_1, string_2]
                            for i in range(3):
                                result = {}
                                result["pair_value"] = [v1, v2]
                                try:
                                    if self.fig != None:
                                        fig = self.fig
                                        result["answer"] = self.client.give_test_fig(prompt, fig)
                                    else:
                                        result["answer"] = self.client.give_test(prompt)
                                except:
                                    return results
                                results[f"give_valuenet_{i+1}"].append(result)
                            did_pairs.append(pair1)
                            did_pairs.append(pair2)
                        except:
                            continue
        return results

    def result_question(self):
        result = {}
        result["settings"] = self.settings

        if self.life_prompt == "":
            print("missing life prompt")
            return None

        print("tipiテスト")
        result.update(self.survey_tipi())
        print(" -> 終了")

        print("pvqテスト")
        result.update(self.survey_pvq())
        print(" -> 終了")

        with open(f"{self.save_dir}-question.json","w",encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    def result_scenario(self):
        result = {}
        result["settings"] = self.settings

        if self.life_prompt == "":
            return None

        print("selectscenarioテスト")
        result.update(self.survey_selectscenario())
        print(" -> 終了")

        with open(f"{self.save_dir}-scenario.json","w",encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

# 卒研のときの/ディレクトリ調整なし
class GetDataSub():
    def __init__(self, settings):
        self.settings = settings
        self.user_id=settings["user_id"]
        self.prompt_type=settings["life_prompt_type"]
        self.mp_instance = mp.Make_prompt(user_id=self.user_id)
        if settings["demo_info"]:
            self.life_prompt = self.mp_instance.demo_info() + "\n" + self.get_life_prompt(self.prompt_type)
        else:
            self.life_prompt = self.get_life_prompt(self.prompt_type)
        if settings["figure"]:
            self.fig = self.mp_instance.life_graph_fig()
        else:
            self.fig = None
        self.client=GeminiContent()

    def get_life_prompt(self, prompt_type):
        if prompt_type == "Json":
            prompt=self.mp_instance.json_prompt_formatter()
        if prompt_type == "Story":
            prompt=self.mp_instance.story_prompt_formatter()
        return prompt

    def survey_tipi(self):
        result={}
        tipi = """"""
        with open("Prompt/Test_prompt/tipi_sub.txt","r",encoding="utf-8") as f:
            for line in f.readlines():
                tipi += line
        prompt = self.life_prompt + "\n\n" + tipi
        #result["tipi_prompt"] = prompt
        if self.fig != None:
            fig = self.fig
            result["give_tipi_1"] = self.client.give_test_fig(prompt, fig)
            result["give_tipi_2"] = self.client.give_test_fig(prompt, fig)
            result["give_tipi_3"] = self.client.give_test_fig(prompt, fig)
        else:
            result["give_tipi_1"] = self.client.give_test(prompt)
            result["give_tipi_2"] = self.client.give_test(prompt)
            result["give_tipi_3"] = self.client.give_test(prompt)
        return result

    def survey_pvq(self):
        result={}
        pvq = """"""
        with open("Prompt/Test_prompt/pvq_sub.txt","r",encoding="utf-8") as f:
            for line in f.readlines():
                pvq += line
        prompt = self.life_prompt + "\n\n" + pvq
        #result["pvq_prompt"] = prompt
        if self.fig != None:
            fig = self.fig
            result["give_pvq_1"] = self.client.give_test_fig(prompt, fig)
            result["give_pvq_2"] = self.client.give_test_fig(prompt, fig)
            result["give_pvq_3"] = self.client.give_test_fig(prompt, fig)
        else:
            result["give_pvq_1"] = self.client.give_test(prompt)
            result["give_pvq_2"] = self.client.give_test(prompt)
            result["give_pvq_3"] = self.client.give_test(prompt)
        return result

    def tipi_result(self):
        result = {}
        result["settings"] = self.settings

        print("tipiテスト")
        result.update(self.survey_tipi())
        print(" -> 終了")

        with open(f"Data/{self.prompt_type}_prompt/sub_tipi/{self.user_id}.json","w",encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    def pvq_result(self):
        result = {}
        result["settings"] = self.settings

        print("pvqテスト")
        result.update(self.survey_pvq())
        print(" -> 終了")

        with open(f"Data/{self.prompt_type}_prompt/sub_pvq/{self.user_id}.json","w",encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)