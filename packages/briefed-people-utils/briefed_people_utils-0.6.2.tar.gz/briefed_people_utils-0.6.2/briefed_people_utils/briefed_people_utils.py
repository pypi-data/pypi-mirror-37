import json, requests
from bs4 import BeautifulSoup


def get_soup(link):

    try:

        link = link.replace('\n','').strip()
        headers = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(link,headers=headers)

        if response.status_code == requests.codes.ok:
            page = response.content
            soup = BeautifulSoup(page, "lxml")

        else:
            soup = None
            print("Requests returned status_code: {0}. {1}".format(response.status_code,link))

        return soup

    except Exception as e:
        print(str(e))
        print(link)


def prepare_url(host,model_name):
    if model_name:
        url = '{0}api/{1}/update/'.format(host,model_name)
    else:
        url = '{0}api/update/_bulk'.format(host)
    return url


def prepare_headers(token,username,password,json):
    headers = {
        'Authorization': 'Token {0}'.format(token),
        'user': username,
        'password': password,
    }
    if json:
        headers['Content-Type'] = 'application/json'
    return headers


def update_or_create_model_instance(host,token,username,password,data,model_name=None,json=False):

    url = prepare_url(host,model_name)
    headers = prepare_headers(token,username,password,json)
    if json:
        payload = data
        response = requests.put(url,headers=headers,json=payload)
    else:
        response = requests.put(url,headers=headers,data=data)

    return response


def list_model_instances(host,token,username,password,data,model_name,query=None):

    url = prepare_url(host,model_name) + query
    json = None
    headers = prepare_headers(token,username,password,json)
    response = requests.put(url,headers=headers)

    return response


def get_first_name_last_name(raw_name):

    full_name = raw_name.strip().replace('  ',' ').strip()
    full_name_split = full_name.split()
    prepositional_articles = ['von', 'Von', 'VON', 'van', 'Van', 'VAN', 'de', 'De','di','Di','da','Da','du', 'Du', 'des', 'Des', 'del', 'Del', 'della', 'Della','in','In','le','Le','la','La']
    first_name = ''
    last_name = ''

    if len(full_name_split) == 2:
        first_name = full_name_split[0].strip()
        last_name = full_name_split[1].strip()
    else:
        for i in range(len(full_name_split)):
            if any(prepositional_article == full_name_split[i] for prepositional_article in prepositional_articles):
                first_name = raw_name.split(' ',i)[0].strip()
                last_name = raw_name.split(' ',i)[1].strip()

    # If we still have not identified a first_name by this point then we should try
    # something different.
    if not first_name:
        if len(full_name_split) == 3:
            first_name = raw_name.rsplit(' ',1)[0].strip()
            last_name = raw_name.split(' ',2)[2].strip()
        elif len(full_name_split) == 4:
            first_name = raw_name.rsplit(' ',1)[0].strip()
            last_name = raw_name.split(' ',3)[3].strip()

    d = {
        'full_name': full_name,
        'first_name': first_name,
        'last_name': last_name,
    }

    return d


def get_full_name_with_capitalised_surname(raw_name):
    first_name = ''
    last_name = ''
    for word in raw_name.split():
        if word.isupper() and '.' not in word:
            last_name += '{0} '.format(word.strip())
        else:
            first_name += '{0} '.format(word.strip().capitalize())
    first_name = first_name.strip()
    last_name = last_name.strip().title()
    full_name = '{0} {1}'.format(first_name,last_name)

    d = {
        'full_name': full_name.strip(),
        'first_name': first_name,
        'last_name': last_name,
    }

    # If it didn't work then we should try another method.
    if not first_name or not last_name:
        d = get_first_name_last_name(raw_name)

    return d


def extract_full_text(contains_full_text):
    full_text = ''
    for paragraph in contains_full_text.findAll('p'):
        full_text += paragraph.text.strip()
        full_text += '\n'
    full_text = full_text.strip()
    return full_text


def get_link_from_xml_item(item):
    for element in item:
        if str(element).strip().startswith('http'):
            link = element.strip()
            return link


def get_clean_committee_name(committee_name):
    committee_name = committee_name.replace("Committee on ", "").replace("Committee on the ", "").replace("Special committee on","").replace("Subcommittee on ", "").replace("Committee of Inquiry into ", "").replace('(Associated committee)','').replace('Committtee','').replace('European Parliament','').strip()

    if committee_name.startswith("the "):
        clean_committee_name = committee_name[4:]

    elif committee_name == 'Committee of Inquiry to investigate alleged contraventions and maladministration in the application of Union law in relation to money laundering, tax avoidance and tax evasion':
        clean_committee_name = 'Money laundering, tax avoidance and tax evasion'

    else:
        clean_committee_name = committee_name

    if "Delegation" in clean_committee_name:
        clean_committee_name = 'EP {0}'.format(clean_committee_name)
    else:
        clean_committee_name = 'EP {0} Committee'.format(clean_committee_name)

    return clean_committee_name


def extract_screen_name_from_link(link):

    if len(str(link.split('/')[3])) <= 16:
        screen_name = link.split('/')[3]

    elif len(str(link.split('/')[-1])) <=16 and len(str(link.split('/')[-1])) >=1:
        screen_name = link.split('/')[-1]

    else:
        screen_name = None

    return screen_name


def get_twiiter_id_str(screen_name,lambda_client):

    event = {
        "screen_name":screen_name,
    }
    response = lambda_client.invoke(
        FunctionName='twitterFunctions-getID',
        InvocationType='RequestResponse',
        Payload=json.dumps(event),
    )
    id_str = response['Payload'].read().decode("utf-8")
    
    return id_str
