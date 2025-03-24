import os
script_dir = os.path.dirname(__file__)

filepath = os.path.join(script_dir, 'sample.txt')
# file_content = ['Line1\n', 'Line2\n']
# with open(filepath, 'a', encoding='utf-8') as file:
#     content = file.writelines(file_content)

# file_content = ''
# if os.path.exists(filepath):
#     with open(filepath, 'r', encoding='utf-8') as file:
#         file_content = file.readlines()
#         # print(f'readlines: {content_readlines}')

#         # file.seek(0)
#         # content_read = file.read()
#         # print(f'read: {content_read}')
#         # for line in file:
#         #     print(line.strip())

#         # print(file.readline())
#         # print(file.readline())
#         # import pdb; pdb.set_trace()

#     with open('copy_sample.txt', 'a', encoding='utf-8') as file:
#         content = file.writelines(file_content)

import json

json_data = {'name': 'Mike', 'age': 24}
with open('sample.json', 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)