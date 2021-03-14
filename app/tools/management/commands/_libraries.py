import pandas as pd

from library.models import Library


def importLibraries():
    df = pd.read_excel('Biblioteki v3.xlsm',sheet_name='DKK',index_col=0, header=0, na_values= str)
    lib = []
    for index, row in df.iterrows():
        lib.append(
            Library(
                area=row['PDF File'] if row['PDF File'] else '',
                city=row['Place'] if row['Place'] else '',
                name=row['LibName'] if row['LibName'] else '',
                address1=row['Adr 1'] if row['Adr 1'] else '',
                address2=row['Adr 2'] if row['Adr 2'] else '',
                phone=row['phone'] if row['phone'] else '',
                moderator=row['moderate'] if row['moderate'] else '',
                email=row['email'] if row['PDF File'] else '',
                www=row['www'] if row['email'] else '',
                salutation=row['zwrot'] if row['zwrot'] else '',
                DDK_kids=True if row['dzieci'] == 'tak' else False,
                DDK_alduts=True if row['Dorosli'] == 'tak' else False,
                DDK_young=True if row['mlodziez'] == 'tak' else False,
                DDK_theme=row['Tematyczny'] if row['Tematyczny'] else '',
                notes=row['inne'] if row['inne'] else '',
            )
        )
        if ((index + 1) % 10) == 0:
            Library.objects.bulk_create(lib)
            lib = []
    Library.objects.bulk_create(lib)
