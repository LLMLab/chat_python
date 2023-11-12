import erniebot

functions = functions = [
    {
        'name': 'get_current_temperature',
        'description': "获取指定城市的气温",
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description': "城市名称",
                },
                'unit': {
                    'type': 'string',
                    'enum': [
                        '摄氏度',
                        '华氏度',
                    ],
                },
            },
            'required': [
                'location',
                'unit',
            ],
        },
        'responses': {
            'type': 'object',
            'properties': {
                'temperature': {
                    'type': 'integer',
                    'description': "城市气温",
                },
                'unit': {
                    'type': 'string',
                    'enum': [
                        '摄氏度',
                        '华氏度',
                    ],
                },
            },
        },
    },
]
erniebot.api_type = 'aistudio'
erniebot.access_token = '3c410ce131fe8d246c47e26fdf932cfd44e95aa8'

messages = [
    {
        'role': 'user',
        'content': "深圳市今天气温如何？",
    }
]

response = erniebot.ChatCompletion.create(
    model='ernie-bot',
    messages=messages,
    functions=functions,
)
assert hasattr(response, 'function_call')
function_call = response.function_call
print(function_call)