import facebook
graph = facebook.GraphAPI(access_token='EAAXPZCt3MtbMBAENWQEX6XWWpyJrlSnH5jxZAoBpadMZC50cIP1KaNfYTLFBI6L0IkRMlvZCg9OVFZAW98MWRHFae1518z7GqX7kjE3cYj8rrBnOM8m4BXZBwd2gX1RnjbWJf8UTbB9rvuqdFlZA63dEjpKKrK7XoMIfDekrw8SsgZDZD', version='2.6')
album_id = "1067443953334625"
graph.put_photo(image=open('blank.png', 'rb'), album_path=album_id + "/photos")

