#%%
import os
import json
import csv
#%%
def process_file(filename: str):
    filepath = f'../../output/{filename}'
    with open(filepath, 'r') as f:
        json_str = f.read()
    json_str = '[' + json_str[:-2] + ']'
    json_obj = json.loads(json_str)
    return json_obj
#%%
data = process_file('com_youtubei_v1_live_chat_get_live_chat/data.json')
with open('comments.json', 'w') as f:
    json.dump(data, f)
comments_data = []
#%%
# Open the CSV file for writing
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write the CSV header
    writer.writerow(['Comment Text', 'Author', 'Time', 'Author Photo URL', 'Video ID', 'Timestamp'])

    # Iterate through the data
    for i, action_object in enumerate(data):
        # This part should be adapted to the actual structure of your JSON object
        actions = action_object.get('continuationContents', {}).get('liveChatContinuation', {}).get('actions', [])
        invalidation_id = action_object.get('continuationContents', {}).get('liveChatContinuation', {}).get('continuations', [])[0].get('invalidationContinuationData', {}).get('invalidationId', {})
        if invalidation_id:
            video_id = invalidation_id.get('topic').split('~')[1].split('~')[0]
            timestamp = invalidation_id.get('protoCreationTimestampMs')
        else:
            video_id = 'NO_VIDEO_ID'
            timestamp = 'NO_TIMESTAMP'
        for action in actions:
            if 'addChatItemAction' in action:
                item = action['addChatItemAction']['item']
                if 'liveChatTextMessageRenderer' in item:
                    message_renderer = item['liveChatTextMessageRenderer']
                    print(message_renderer['message']['runs'])
                    comment_text = ''.join([run['text'] for run in message_renderer['message']['runs'] if 'text' in run])
                    author_name = message_renderer['authorName']['simpleText']
                    author_photo_url = message_renderer['authorPhoto']['thumbnails'][0]['url']
                    writer.writerow([comment_text, author_name, timestamp, author_photo_url, video_id, timestamp])

# %%
