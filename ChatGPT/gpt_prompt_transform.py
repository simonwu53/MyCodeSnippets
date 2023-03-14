import requests
import csv
import json


if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv'
    response = requests.get(url)
    content = response.content.decode('utf-8')
    reader = csv.reader(content.splitlines(), delimiter=',')

    key, value = 'key', 'value'
    template = []
    for i, row in enumerate(reader):
        if i > 0:
            k, v = row
            template.append({key: k, value: v})
    print(f'{i-1} prompts imported.')

    output_file = 'awesome_chatgpt_prompts.json'
    with open(output_file, 'w') as f:
        json.dump(template, f, indent=2)
    print(f'Dumped to file: {output_file}')
