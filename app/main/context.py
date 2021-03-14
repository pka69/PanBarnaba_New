
VERSION = [
    {
        'version': '0.1',
        'date': '2020/12/05'
    },
    {
        'version': '0.2',
        'date': '2021/02/27'
    },
]
act_version = 1

def global_context(request):
    '''
    return global context values
    '''
    context = {
        'copyright': '2020 KalPiCo',
        'copyright_mail': 'kalpico@gmail.com',
        'version': VERSION[act_version]['version'],
    }
    return context