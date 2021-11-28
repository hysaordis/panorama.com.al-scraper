import os


# function to write the news to a file
# takes the news content and the file name as parameters
def saveNews(newslist, path):
    for link, content, date in newslist:
        newspath = path + '\\' + date
        filename = newspath + '\\' + link + '.txt'
        # if the path does not exist, create it
        if not os.path.exists(newspath):
            os.makedirs(newspath)
        # try to open the file and write the news
        # if error occurs, print the error and continue
        try:
            with open(filename, 'w', encoding='utf-16le') as f:
                f.write(content)
                # print the file max name to 10 characters
                print('Saved: ' + filename[-10:])
                f.close()
        except Exception as e:
            print(e)
            continue
    # print the number of news saved
    print('\n' + str(len(newslist)) + ' news saved')
