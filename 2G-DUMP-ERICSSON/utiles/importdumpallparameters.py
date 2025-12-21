
import re
import pandas as pd
from pathlib import Path
import os 
from dotenv import load_dotenv
load_dotenv() 
inputfile=os.getenv("input_path_CELLPARA")


def import_cellpara():
    try:

        GSMALLPARAPath=Path(inputfile)


        if not GSMALLPARAPath.is_file():
            print(f"❌ No File: {GSMALLPARAPath}")
            return pd.DataFrame()

        with open(GSMALLPARAPath, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            content = re.sub(r"-{5,}", "", content)
            #content = content.replace("-----------------------------------------------------", "")
            #content = re.sub(r'^-+\s*$', '', content, flags=re.MULTILINE)
        lines = content.strip().split('\n')

        if not lines or len(lines) < 4:
            print("❗ No File")
            return pd.DataFrame()

        header = re.findall(r'\S+', lines[0])
        data_lines = lines[3:]

        final_data = []
        for line in data_lines:
            row = re.findall(r'\S+', line)
            if row:
                final_data.append(row)

        finalDf_CELLPARA = pd.DataFrame(final_data)

        if all(len(row) == len(header) for row in final_data):
            finalDf_CELLPARA.columns = header
        else:
            print("⚠ mismathed between headers and coulmns count.")

        finalDf_CELLPARA = finalDf_CELLPARA.drop_duplicates().reset_index(drop=True)
        finalDf_CELLPARA=finalDf_CELLPARA.replace("NULL","")
        #finalDf_CELLPARA=finalDf_CELLPARA.dropna()
        print(finalDf_CELLPARA)
        


        return finalDf_CELLPARA

    except Exception as e:
        print(f"❌ Error in proccesing all parameters : {e}")
        return pd.DataFrame()



if __name__ == "__main__":

    input_path  = "D:\\4.2G\\2G-DUMP\\data\\AllParameters_15nov"
    import_cellpara()
