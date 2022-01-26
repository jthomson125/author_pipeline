import csv
from google.cloud import storage


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    client = storage.Client()

    bucket = client.get_bucket('york-project-bucket')

    folder = 'jthomson/2021-12-17-17-01'

    blob_list = []

    single_file = [['author', 'points']]

    for blob in bucket.list_blobs(prefix=folder):
        blob_list.append(blob.name)

        blob_list.pop(0)
        if blob_list[0] == f'{folder}_SUCCESS':
            blob_list.pop(0)

    for item in blob_list:
        blob = bucket.get_blob(item)
        downloaded_blob = blob.download_as_string()
        decoded_blob = downloaded_blob.decode("utf-8")
        decoded_list = decoded_blob.split('\n')
        decoded_list.pop(0)
        decoded_list.pop(-1)
        for row in decoded_list:
            row_list = row.split(',')
            single_file.append(row_list)

    with open('final-list.csv', 'w', encoding="utf-8") as file:
        write = csv.writer(file)
        write.writerows(single_file)

    new_blob_upload = bucket.blob(f'{folder}author_rankings.csv')

    new_blob_upload.upload_from_filename('final-list.csv', content_type='text/csv')






