import facebook, sys

file = sys.argv[1]

graph = facebook.GraphAPI(access_token='EAAD4OYlDv3gBACJsFLTokUWb9LPs6tWaBZBj4JFWzddCNR8HiZA5if1q8xDCRdkCoxXxwg8cJutKQsVxRHqRYUkHoA70imbcQoGsFkffDo2k2SDHtl52mmQ2ZCeZAoD4eMunAXZAgTevdiOc8525I36zP66AoCt7a7AsE0V9hsQZDZD', version='2.6')
page_id = "253185248400673"
graph.put_photo(image=open(file, 'rb'), album_path=page_id + "/photos")

