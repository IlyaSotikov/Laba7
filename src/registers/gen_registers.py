# -*- coding: utf-8 -*-
"""
Генерация XML-описания регистров сведений в формате выгрузки конфигурации 1С (dt=8.3.25).
Артефакты складываются в src/registers/<Имя>/ — для последующей сборки cfe в Designer/EDT.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" xmlns:app="http://v8.1c.ru/8.2/managed/application/core" xmlns:v5="http://v8.1c.ru/8.1/data/core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
'''

FOOTER = '</MetaDataObject>\n'

def type_str(length):
    return ('<v5:TypeDescription><v8:TypeName xsi:type="xs:string" xmlns:v8="http://v8.1c.ru/8.1/data/core"'
            ' xmlns:xs="http://www.w3.org/2001/XMLSchema">Строка</v8:TypeName>'
            f'<v8:MaximumLength xmlns:v8="http://v8.1c.ru/8.1/data/core">{length}</v8:MaximumLength>'
            '<v8:QualifiersList xmlns:v8="http://v8.1c.ru/8.1/data/core">'
            f'<v8:Qualifier>{length}</v8:Qualifier></v8:QualifiersList></v5:TypeDescription>')

def type_any():
    return ('<v5:TypeDescription><v8:TypeName xsi:type="xs:string" xmlns:v8="http://v8.1c.ru/8.1/data/core"'
            ' xmlns:xs="http://www.w3.org/2001/XMLSchema">СправочникСсылка</v8:TypeName></v5:TypeDescription>')

def type_date():
    return ('<v5:TypeDescription><v8:TypeName xsi:type="xs:string" xmlns:v8="http://v8.1c.ru/8.1/data/core"'
            ' xmlns:xs="http://www.w3.org/2001/XMLSchema">Дата</v8:TypeName></v5:TypeDescription>')

def dimension(name, tdims, leading=True):
    return (f'<Children><InformationRegisterDimensionV8Content><Name>{name}</Name>'
            f'<Synonym/><Comment/><ToolTip/><Representation/><ConditionPresentation/><ServerPresentation/>'
            f'{tdims}</InformationRegisterDimensionV8Content></Children>')

def resource(name, tdims):
    return (f'<Children><InformationRegisterResourceV8Content><Name>{name}</Name>'
            f'<Synonym/><Comment/><ToolTip/><Representation/><ConditionPresentation/><ServerPresentation/>'
            f'{tdims}</InformationRegisterResourceV8Content></Children>')

def register_xml(name, dims, resources):
    body = ['<InformationRegister>']
    body.append(f'<Properties><Name>{name}</Name><ReportUseTotalsAndGroupByDefaultNo>ложь</ReportUseTotalsAndGroupByDefaultNo></Properties>')
    body.append('<ChildTypes>')
    body.append('<Type>InformationRegisterDimensionV8Content</Type>')
    body.append('<Type>InformationRegisterResourceV8Content</Type>')
    body.append('</ChildTypes>')
    for d in dims:
        body.append(d)
    for r in resources:
        body.append(r)
    body.append('</InformationRegister>')
    return HEADER + '\n'.join(body) + '\n' + FOOTER

REGISTERS = {
    'ЧЗ_МаркиИзЭДО': (
        [('КодМаркировки', type_str(200)), ('ДиадокDocumentId', type_str(200))],
        [('ДокументПоступление', type_any()), ('ДатаИзвлечения', type_date()),
         ('Статус', type_str(20)), ('ДатаЗагрузки', type_date())]),
    'ЧЗ_ОборотМарок': (
        [('КодМаркировки', type_str(200))],
        [('Статус', type_str(20)), ('ДокументСписания', type_any()), ('ПричинаСписания', type_str(40)),
         ('ИННПокупателя', type_str(13)), ('ДиадокDocumentId', type_str(200)), ('ДатаОперации', type_date())]),
    'ЧЗ_СвязиДокументовЭДО': (
        [('Документ1С', type_any()), ('ДиадокDocumentId', type_str(200))],
        [('Направление', type_str(10)), ('СтатусПоследний', type_str(60))]),
    'ЧЗ_ЖурналОбмена': (
        [('ДатаВремя', type_date()), ('Событие', type_str(100))],
        [('Документ1С', type_any()), ('ДиадокDocumentId', type_str(200)), ('КодМаркировки', type_str(200)),
         ('Результат', type_str(20)), ('Комментарий', type_str(1000)), ('Пользователь', type_str(100))]),
}

for name, (dims, res) in REGISTERS.items():
    d = os.path.join(BASE, name)
    os.makedirs(d, exist_ok=True)
    xml = register_xml(name, [dimension(n, t) for n, t in dims], [resource(n, t) for n, t in res])
    with open(os.path.join(d, f'{name}.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    print('OK', name)
