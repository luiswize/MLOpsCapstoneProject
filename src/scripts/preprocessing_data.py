import pandas as pd
import numpy as np
import email
import re
import os 
from typing import List
from tqdm import tqdm


def parse_email_document(path: str) -> pd.DataFrame:
    """
    Parses email raw file into a dataframe
    """
    
    # TODO: Some files have encoding troubles, as there are asci characteres that raises troubles in the open() block
    # TODO: Fix the encoding characters trouble
    try:
        with open(path) as f:
            contents = f.read()

        msg = email.message_from_string(contents)    

        if 'Cc' in msg:
            _cc = [re.sub('\s+','', msg['Cc']).split(',')] 
        else: 
            _cc = [np.nan]
            
        if 'Bcc' in msg:
            _bcc = [re.sub('\s+','', msg['Cc']).split(',')] 
        else: 
            _bcc = [np.nan]
            
        if 'To' in msg:
            _to = [re.sub('\s+','', msg['To']).split(',')]
        else:
            _to = [np.nan]
        
        attributes = {  
            "Message-ID": [msg["Message-ID"]],
            "Date": [msg["Date"]],
            "From": [re.sub('\s+','', msg['From']).split(',')],
            "To": _to,
            "Subject": [msg["Subject"]],
            "Cc": _cc,
            "Mime-Version": [msg["Mime-Version"]],
            "Content-Type": [msg["Content-Type"]],
            "Content-Transfer-Encoding": [msg["Content-Transfer-Encoding"]],
            "Bcc": _bcc,
            "X-From": [msg["X-From"]],
            "X-To": [msg["X-To"]],
            "X-cc": [msg["X-cc"]],
            "X-bcc": [msg["X-bcc"]],
            "X-Folder": [msg["X-Folder"]],
            "X-Origin": [msg["X-Origin"]],
            "X-FileName": [msg["X-FileName"]]
        }

        if msg.is_multipart():
            for part in email.get_payload():
                body = part.get_payload() 
        else:
            body = msg.get_payload() 
            
        attributes['body'] = body
        df = pd.DataFrame(attributes, columns=attributes.keys())
        return df
    except:
        pass


def get_email_paths(root_directory: str):
    """
    Get list of all files in subfolders of root directory
    """
    files_to_scratch = []
    for path, subdirs, files in os.walk(root_directory):
        
        for name in files:
            files_to_scratch.append(os.path.join(path, name))
            # print(os.path.join(path, name))
    
    return files_to_scratch


def parse_multiple_emails_document(files: List[str]) -> pd.DataFrame:
    """
    Parse list of mails into a dataframe
    """
    columns = ['Message-ID', 'Date', 'From', 'To', 'Subject', 'Cc', 'Mime-Version',
       'Content-Type', 'Content-Transfer-Encoding', 'Bcc', 'X-From', 'X-To',
       'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName', 'body']
    complete_df = pd.DataFrame(columns=columns)
    
    for path in tqdm(files):
        df = parse_email_document(path)
        complete_df = pd.concat([complete_df, df])
    
    return complete_df.reset_index(drop=True)


if __name__ == "__main__":
    not_spam_path = '/Users/luis.morales/Desktop/MLOpsBootcamp/MLOpsCapstoneProject/data/sagemaker-testing/not_spam'
    spam_path = '/Users/luis.morales/Desktop/MLOpsBootcamp/MLOpsCapstoneProject/data/sagemaker-testing/spam'
    
    output_path = '/Users/luis.morales/Desktop/MLOpsBootcamp/MLOpsCapstoneProject/data/sagemaker-testing/Parsed'
    
    
    not_spam_paths = get_email_paths(not_spam_path)
    spam_paths = get_email_paths(spam_path)
    
    
    not_spam_df = parse_multiple_emails_document(not_spam_paths)
    spam_df = parse_multiple_emails_document(spam_paths)
    
    
    # maildir_df.to_parquet('./../data/preprocessing_output/test.parquet.gzip', compression='gzip', engine='fastparquet')
    not_spam_df.to_parquet(f"{output_path}/not_spam.parquet.gzip", compression='gzip', engine='fastparquet')
    spam_df.to_parquet(f"{output_path}/spam.parquet.gzip", compression='gzip', engine='fastparquet')