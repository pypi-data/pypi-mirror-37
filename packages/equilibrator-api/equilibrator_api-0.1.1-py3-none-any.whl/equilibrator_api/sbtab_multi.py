from sbtab import SBtab
from sbtab.misc import split_sbtabs
import pandas as pd
from io import TextIOWrapper

def ReadMultiSBtab(input_sbtab):
    """
        Reads an SBtab file with multiple tables. In the future will be replace
        with the SBtabDocument class as part of the sbtab package.
        
        Returns:
            A dictionary with the table names as keys and the values are
            SBtabTable objects
    """
    if type(input_sbtab) == str:
        with open(input_sbtab, 'r') as sbtab_file:
            file_content = sbtab_file.read()
        file_name = input_sbtab
    elif isinstance(input_sbtab, TextIOWrapper):
        file_content = input_sbtab.read()
        file_name = 'stdin.tsv'
    else:
        raise ValueError('input_sbtab should be either a string or a TextIOWrapper')
    
    sbtabs = []
    sbtab_strings = split_sbtabs(file_content)
    for i, sbtab_s in enumerate(sbtab_strings):
        name_single = str(i) + '_' + file_name
        sbtab_single = SBtab.SBtabTable(sbtab_s, name_single)
        sbtabs.append(sbtab_single)

    tdict = {GetTableName(t) : t for t in sbtabs}
    return tdict

def ToDataFrame(sbtab):
    column_names = list(map(lambda s: s[1:], sbtab.columns))
    df = pd.DataFrame(data=sbtab._get_rows(), columns=column_names)
    return df

def GetTableInfo(sbtab):
    return sbtab._get_table_information()

def GetTableName(sbtab):
    return GetTableInfo(sbtab)[1]

def GetCustomTableInfo(sbtab, attribute_name):
    """
        This function is here to fix a bug in the SBtab package.
        Namely, the last attribute value is returned with a " Date=" string
        added to it.
    """
    info_s = sbtab._get_custom_table_information(attribute_name)
    if info_s.find(' Date=') != -1:
        return info_s.replace(' Date=', '')
    else:
        return info_s

if __name__ == '__main__':
    tdict = ReadMultiSBtab('tests/EMP_glycolysis_full_SBtab.tsv')
    print(ToDataFrame(tdict['RelativeFlux']))
    print(GetCustomTableInfo(tdict['ConcentrationConstraint'], 'Unit'))
    print(GetCustomTableInfo(tdict['Parameter'], 'IonicStrength'))
    print(GetCustomTableInfo(tdict['Parameter'], 'pH'))