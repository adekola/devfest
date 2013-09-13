import httplib2

post_data = '{"user_id": 2039904923474, "title": "Eat boli", "text": "i will like to eat boli at 3:00pm"}'

h = httplib2.Http()

resp, content = h.request('http://localhost:8080/addToDoForUser', 
        'POST', 
        post_data ,
        headers={'Content-Type': 'application/json'})

print content
