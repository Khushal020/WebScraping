import json
import csv

result_json = {'url': 'url', 'text': 'visible_text', 'images': 'images', 'top_img': 'top_image',
                       #'keywords': keywords,
                       #'authors': authors, 'canonical_link': canonical_link, 'title': title, 'meta_data': meta_data,
                       #'movies': movies, 'publish_date': get_epoch_time(publish_date), 'source': source,
                       'summary': 'summary'}

with open('test.csv', 'a+', newline='') as file:
    csv_file = csv.writer(file)
    #csv_file.writerow(['url','text','images','top_img','summary'])
    
    #csv_file.writerow([result_json.get('url'),result_json.get('text'),result_json.get('images'),result_json.get('top_img'),result_json.get('summary'),])
    #csv_file.writerow([result_json.get('url'),result_json.get('text'),result_json.get('images'),result_json.get('top_img'),result_json.get('summary'),])\
    csv_file.writerow(result_json.values())
    print(result_json.values())