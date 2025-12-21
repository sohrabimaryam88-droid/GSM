import re,os
import pandas as pd
from pathlib import Path
# ###########
from dotenv import load_dotenv
load_dotenv() 
input_path_rldepext=os.getenv("input_path_rldepext")

def import_rldepext():
    try:
        file_path = Path(input_path_rldepext)
        if not file_path.exists():
            print(f"Error: File not found at path: {file_path}")
            return pd.DataFrame()        
        
        with open(file_path, 'r', encoding='cp1252') as file:

            content = file.read()
            records = []
            ne_sections = re.split(r'(eaw)', content)
            b_sections = []

            for section in ne_sections:
                m = re.search(r'(B\d+E)', section)
                if m:
                    b_sections.append(section)            
            
            for section in b_sections:
                cell_blocks = re.split(r'\n(?=CELL\s+CGI)', section)    
                m = re.search(r'(B\d+E);', section)
                if m:
                    bsc = m.group(1)  #    "B7267E"
                else:
                    bsc = None
                   
                for block in cell_blocks:
                        record = {'BSC': bsc} 

                        
                        if 'TH' not in block:
                            continue 
                        # ---------- first section : CELL  CGI BSIC  BCCHNO  AGBLK  MFRMS  IRC  ----------                                  
                        m = re.search(
                            
                            r'\n(TH\d{4}\w)\s+'
                            r'(\d+-\d+-\d+-\d+)\s+'
                            r'(\d+)\s+'
                            r'(\d+)'
                            r'(?:\s+(\d+))?'
                            r'(?:\s+(\d+))?'
                            r'(?:\s+(\d+))?',
                            block
                        )
                        if m:
                            record['CELL'] = m.group(1)
                            record['CGI'] = m.group(2)
                            record['BSIC'] = m.group(3)
                            record['BCCHNO'] = m.group(4)
                            record['AGBLK'] = m.group(5)
                            record['MFRMS'] = m.group(6)
                            record['IRC'] = m.group(7)
                        # ---------- second section : TYPE  BCCHTYPE FNOFFSET  XRANGE  CSYSTYPE ----------
                        m = re.search(
                            r'\n(EXT|INT)\s+.*?(GSM\d+)',
                            block,
                            re.S
                        )
                        if m:
                            record['TYPE'] = m.group(1)
                            record['CSYSTYPE'] = m.group(2)

                        # ----------  third section: CELLIND  RAC  RIMNACC  GAN  DFI ----------
                        m = re.search(
                            r"(H'\w+)\s+(\d+)\s+(OFF|ON)\s+(NO|YES)\s+(ALLOWED|RESTRICTED)",
                            block
                        )
                        if m:
                            record['CELLIND'] = m.group(1)
                            record['RAC'] = m.group(2)
                            record['RIMNACC'] = m.group(3)
                            record['GAN'] = m.group(4)
                            record['DFI'] = m.group(5)
                        if record:
                            records.append(record)   
        finalDf_RLDEPEXT = pd.DataFrame(records)


        
        
        finalDf_RLDEPEXT=finalDf_RLDEPEXT.drop_duplicates().reset_index(drop=True)                    


        if not finalDf_RLDEPEXT.empty:
            #finalDf_RLDEPEXT.to_csv('finalDf_RLDEPEXT.csv', index=False, encoding='utf-8-sig')       
            return finalDf_RLDEPEXT
    
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return pd.DataFrame()
    
    except Exception as e:
        print(f"An error occurred in rldepext: {e}")
        return pd.DataFrame()
if __name__=="__main__":
    df=import_rldepext()
    df.to_csv("df_rldepext.csv")
    print(df)    