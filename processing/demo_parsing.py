import requests
import argparse
import time

SERVER_PATH = "http://api.italianlp.it"


def api_load_document(text, async_call):
    r = requests.post(SERVER_PATH + '/documents/',
                      data={'text': text,
                            'extra_tasks': ['syntax'],
                            'lang': "IT",
                            'async': async_call})

    api_doc_id = r.json()['id']

    return api_doc_id


def api_get_result_sync(api_doc_id):
    result = requests.get(SERVER_PATH + '/documents/details/%s' % api_doc_id,
                          {'requested_output': "conll", 'conll_level': "parsed"})
    return result.json()['output']


def api_get_result_async(api_doc_id, page):
    url = f"{SERVER_PATH}/documents/details/{api_doc_id}?page={page}"
    result = requests.get(url)
    return result.json()


def get_morphosyntacic_features(tok):
    ms_feats = ['num', 'per', 'mod', 'gen', 'ten']
    ms_string = []
    for feat in ms_feats:
        if tok[feat] is not None:
            ms_string.append(f'{feat}={str(tok[feat])}')
    if ms_string:
        ms_string = '|'.join(ms_string)
    else:
        ms_string = '_'
    return ms_string


def format_aync_output(sentence):
    sorted_feats = ['sequence', 'word', 'lemma', 'cpos', 'pos', 'dep_parent_sequence', 'dep_type']

    sentence_tokens = []
    for tok in sentence['tokens']:
        token_str = [str(tok[feat]) for feat in sorted_feats]
        if token_str[-2] == 'None':
            token_str[-2] = '0'
        token_str.insert(-2, get_morphosyntacic_features(tok))
        sentence_tokens.append(token_str)
    return sentence_tokens


def write_aync_output_to_file(out_path, api_doc_id, out_sentences):
    with open(out_path, 'w+') as out_file:
        out_file.write(f'<doc id="{api_doc_id}">\n\n')
        for sentence in out_sentences:
            for token in sentence:
                out_file.write('\t'.join(token) + '\n')
            out_file.write('\n')
        out_file.write('</doc>')


def parse_text_async(api_doc_id):
    page = 1
    out_sentences = []

    while True:
        document_details = api_get_result_async(api_doc_id, page)

        # WAITING FOR COMPLETE EXECUTION OF TASKS
        if not document_details['parsing_executed']:
            print("Waiting for results...")
            time.sleep(5)
            continue

        # ALL TASKS COMPLETED
        for sentence in document_details['sentences']['data']:
            formatted_tokens = format_aync_output(sentence)
            out_sentences.append(formatted_tokens)

        if document_details['sentences']['next']:
            # FETCH NEW PAGE
            page += 1
        else:
            # NOTHING MORE TO FETCH
            break
    return out_sentences


def call_parsing_api(api_doc_id, out_path, async_call):
    if async_call:
        parsing = parse_text_async(api_doc_id)
        write_aync_output_to_file(out_path, api_doc_id, parsing)
    else:
        parsing = api_get_result_sync(api_doc_id)
        with open(out_path, 'w') as out_file:
            out_file.write(parsing)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file_path', required=True,
                        help='Percorso del file su cui eseguire il POS tagging.')
    parser.add_argument('-a', '--async_call', action='store_true',
                        help='Flag che indica se eseguire la chiamata alle API in modo asincrono.')
    parser.add_argument('-o', '--output_file_path', default=None,
                        help='Percorso del file su cui salvare il risultato del parser. Se non viene fornito, '
                             'il risultato viene salvato su un file con lo stesso nome del file di input, '
                             'ma con estensione ".parsed".')

    args = parser.parse_args()

    if args.output_file_path is None:
        args.output_file_path = '.'.join(args.input_file_path.split('.')[:-1]) + '.parsed'

    with open(args.input_file_path, 'r', encoding='utf-8') as src_file:
        text = src_file.read()

    api_doc_id = api_load_document(text, args.async_call)
    call_parsing_api(api_doc_id, args.output_file_path, args.async_call)


if __name__ == '__main__':
    main()
