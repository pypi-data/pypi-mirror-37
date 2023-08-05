def nested_underscore(data):
    markup = ''
    for result in data['results']:
        for term in result['results'][0]['result']['_terms']:
            try:
                for att in term['_attributes']:
                    markup += ('<strong>' + att['_field_name'] + '</strong><br>')
                    markup += (att['_chardata'] + '<br>')
            except KeyError:
                pass
    return markup


def related(data):
    markup = ''
    for result in data['results']:
        for term in result['results'][0]['result']['_terms']:
            main = term['_chardata']
            markup += ('<strong>' + main + '</strong> ')
            for att in term['_attributes']:
                markup += (att['_chardata'] + ' ')
            markup += '<br>'
    return markup


annerlike_afrikaans = nested_underscore
aws_2017 = nested_underscore
aws_woordelys = nested_underscore


def dac(data):
    markup = ''
    for entry in data['results'][0]['results'][0]['result']['entries']:
        source = entry['dataset']
        markup += f'<strong>{source}</strong><br>'
        for html in entry['html']:
            markup += html

    return markup


def ewa(data):
    markup = ''
    for result in data['results'][0]['results']:
        markup += result['result']['html'][0]
    return markup


def aanlyn(data):
    markup = ''
    for entry in data['results'][0]['results'][0]['result']['entries']:
        source = entry['dataset']
        markup += f'<strong>{source}</strong><br>'
        for html in entry['html']:
            markup += html
    return markup


hataanlyn = aanlyn

kollokasiewoordeboek = nested_underscore
kookkuns = nested_underscore
blokkieswoordeboek = related
thesaurus = related
viva_gesegdes = nested_underscore
wat = aanlyn


def simple_html(data):
    markup = ''
    for result in data['results'][0]['results']:
        for html in result['result']['html']:
            markup += html
    return markup


def trans(data):
    markup = ''
    for result in data['results']:
        for term in result['results'][0]['result']['_terms']:
            markup += ('<strong>' + term['_field_name'] + '</strong><br>' +
                       term['_chardata'] + '<br>')

    return markup


longmanonline = aanlyn

chemiewoordeboek = nested_underscore
fisikawoordeboek = nested_underscore
paramediesewoordeboek = nested_underscore
transtips_english = trans
transtips_setswana = trans
wat_praat_jy = simple_html
tweetaligevoorsetsel_woordeboek = simple_html
wynindustriewoordeboek = nested_underscore
wikipedia = simple_html
afrikaanse_voelname = simple_html
