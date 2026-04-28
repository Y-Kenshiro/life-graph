# 相関係数の箱ひげ図の作成
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_box(dir, file_name1, file_name2, figure_name):
    j_csv = pd.read_csv(f"{dir}{file_name1}.csv", encoding="utf-8")
    j_data = j_csv["correlation"]
    s_csv = pd.read_csv(f"{dir}{file_name2}.csv", encoding="utf-8")
    s_data = s_csv["correlation"]
    save_name = f"{dir}/{figure_name}"
    box(j_data, s_data, save_name)

def box(j_data, s_data, save_name):
    # IDごとの相関係数データがDataFrame（df）にあると想定
    # 例: columns=['ID', 'Condition', 'Correlation']
    j_temp = j_data.copy()
    j_temp['type'] = 'JSON形式'
    s_temp = s_data.copy()
    s_temp['type'] = 'Story形式'
    combined = pd.concat([j_temp, s_temp], ignore_index=True)

    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x='type', y='correlation', data=combined) # [, whis=float('inf')]外れ値表示なしにしたいとき
    for i, group in enumerate(combined['type'].unique()):
        y_vals = combined[combined['type'] == group]['correlation']
        # 最大値
        ax.text(i, y_vals.max(), f'{y_vals.max():.4f}',
                ha='center', va='bottom', color='red', fontsize=16)
        # 最小値
        ax.text(i, y_vals.min(), f'{y_vals.min():.4f}',
                ha='center', va='top', color='blue', fontsize=16)
    plt.ylabel('順位相関係数', fontsize=18)
    plt.xlabel('形式', fontsize=18)
    plt.xticks(fontsize=16)
    plt.ylim(-1.2, 1.2) # 相関係数の範囲に固定
    plt.tight_layout()
    plt.savefig(save_name, dpi=300, bbox_inches='tight')

# TIPI
create_box(
    dir="Gemini/TIPI/Corr",
    file_name1="JSON_nofig",
    file_name2="Story_nofig",
    figure_name="box_nofig"
)
# PVQ
create_box(
    dir="Gemini/PVQ/Corr",
    file_name1="JSON_nofig",
    file_name2="Story_nofig",
    figure_name="box_nofig"
)