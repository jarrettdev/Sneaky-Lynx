#%%
import os
from process_output import process_file
import pandas as pd
import json
#%%
youtube_comments_object = process_file('com_youtubei_v1_browse/data.json')

#%%
len(youtube_comments_object)
# %%

# List to store extracted data
comments_data = []
debug_dir = 'debug/'
if not os.path.exists(debug_dir):
    os.makedirs(debug_dir)
    
# Iterate through the youtube_comments_object
for i, comment_object in enumerate(youtube_comments_object):
    if 'contentText' not in str(comment_object):
        print(f'skipping commentitem {i}')
        continue
    endpoints = comment_object.get('onResponseReceivedEndpoints', [])
    for j, endpoint in enumerate(endpoints):
        continuation_items = endpoint.get('appendContinuationItemsAction', {}).get('continuationItems', [])
        if continuation_items == []:
            continuation_items = endpoint.get('reloadContinuationItemsCommand', {}).get('continuationItems', [])
        for k, item in enumerate(continuation_items):
            with open(debug_dir + f'comment{i}_endpoint_{j}item_{k}.json', 'w') as f:
                json.dump(item, f, indent=4)
            comment_renderer = item.get('commentRenderer', {})
            comment_thread_renderer = item.get('commentThreadRenderer', {})
            author_text = comment_renderer.get('authorText', {}).get('simpleText', '')
            content_texts = comment_renderer.get('contentText', {}).get('runs', [])
            content_texts_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('contentText', {}).get('runs', [])
            author_text_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('authorText', {}).get('simpleText', '')
            if content_texts == []:
                print(f'Problem with comment {i} endpoint {j} item {k}')
                
                #print(comment_thread_renderer)
                try:
                    content_texts = comment_thread_renderer.get('comment', {}).get('commentRenderer').get('contentText', {}).get('runs', [])
                except Exception:
                    content_texts = []
                if len(content_texts) != 0:
                    print(f'Found contentText in commentThreadRenderer for comment {i} endpoint {j} item {k}')
                    print(content_texts)
            content_text = ''.join([text_run.get('text', '') for text_run in content_texts])
            print(content_text)
            thumbnails = comment_renderer.get('authorThumbnail', {}).get('thumbnails', [])
            thumbnails_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('authorThumbnail', {}).get('thumbnails', [])
            thumbnail_url = thumbnails[0].get('url') if thumbnails else ''
            published_time_text = comment_renderer.get('publishedTimeText', {}).get('runs', [])[0].get('text', '') if comment_renderer.get('publishedTimeText', {}).get('runs', []) else ''
            published_time_text_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('publishedTimeText', {}).get('runs', [])[0].get('text', '') if comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('publishedTimeText', {}).get('runs', []) else ''
            comment_id = comment_renderer.get('commentId', '')
            comment_id_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('commentId', '')
            video_id = comment_renderer.get('publishedTimeText', {}).get('runs', [])[0].get('navigationEndpoint', {}).get('watchEndpoint', {}).get('videoId', '') if comment_renderer.get('publishedTimeText', {}).get('runs', []) else ''
            video_id_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('publishedTimeText', {}).get('runs', [])[0].get('navigationEndpoint', {}).get('watchEndpoint', {}).get('videoId', '') if comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('publishedTimeText', {}).get('runs', []) else ''
            try:
                comment_likes = comment_renderer.get('actionButtons', {}).get('commentActionButtonsRenderer', {}).get('likeButton', {}).get('toggleButtonRenderer', {}).get('toggledServiceEndpoint', {}).get('performCommentActionEndpoint', {}).get('clientActions', [])[0].get('updateCommentVoteAction', {}).get('voteCount', '').get('simpleText', '')
            except Exception:
                comment_likes = '0'
            try:
                comment_likes_from_thread = comment_thread_renderer.get('comment', {}).get('commentRenderer', {}).get('actionButtons', {}).get('commentActionButtonsRenderer', {}).get('likeButton', {}).get('toggleButtonRenderer', {}).get('toggledServiceEndpoint', {}).get('performCommentActionEndpoint', {}).get('clientActions', [])[0].get('updateCommentVoteAction', {}).get('voteCount', '').get('simpleText', '')
            except Exception:
                comment_likes_from_thread = '0'

            if content_text == '':
                print(f'Content Problem with comment {i} endpoint {j} item {k}')

            if author_text == '':
                author_text = author_text_from_thread
            if thumbnail_url == '':
                thumbnail_url = thumbnails_from_thread[0].get('url', '') if thumbnails_from_thread else ''
            if published_time_text == '':
                published_time_text = published_time_text_from_thread
            if comment_id == '':
                comment_id = comment_id_from_thread
            if video_id == '':
                video_id = video_id_from_thread
            if comment_likes == '0':
                comment_likes = comment_likes_from_thread
            # Append the extracted data to the list
            comments_data.append({
                'Comment_ID': comment_id,
                'Comment_Likes': comment_likes,
                'Author': author_text,
                'Comment': content_text,
                'Thumbnail_URL': thumbnail_url,
                'Published_Time': published_time_text,
                'Video_ID': video_id
            })

# Convert to a DataFrame
df_comments = pd.DataFrame(comments_data)

df_comments['Comment_Likes'] = df_comments['Comment_Likes'].str.replace(',', '').str.replace('.', '').str.replace('M', '000000').str.replace('K', '000')
df_comments['Comment_Likes'] = df_comments['Comment_Likes'].astype(int)
df_comments = df_comments.sort_values(by=['Comment_Likes', 'Video_ID'], ascending=False)
# Print or save to CSV
print(df_comments)
#%%
#drop empty rows
df_comments = df_comments[df_comments['Author'] != '']
df_comments = df_comments.drop_duplicates(['Author', 'Comment', 'Thumbnail_URL', 'Published_Time', 'Video_ID'])
df_comments = df_comments.sort_values(by=['Video_ID', 'Comment_Likes'], ascending=[True, False])
df_comments.to_csv('comments.csv', index=False)

# %%
df_comments['Author'].value_counts().iloc[0:10].plot(kind='bar')
# %%
