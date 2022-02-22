from flask import Flask

app = Flask(__name__)def

@app.route('/')

def getVideos():

api_key = "AIzaSyCw36olQLlK9JBS0ULYrn3k0DRcB6uIM8c"
	os.environ["OAUTHLIB_INSECURE_TRANSORT"] = "1"

	api_service_name = "youtube"
	api_version = "v3"
	client = build(api_service_name, api_version, developerKey=api_key)
	request = client.search().list(
		part="snippet",
		channelId="UCppy4jafHu51iCMl-7qVbFA",
		type="video",
		maxResults=50,
		order='videoCount'
	)
	
	json_data = request.execute()

	#with open('results.json', 'w', encoiding='ascii') as write_file:
	#	json.dump(json_data, write_file)

	#with open("results.json", "r", encoding='ascii') as read_file:
	#	json_data = json.load(read_file)
	videos_list = json_data['items']

	for i in videos_list:
		print("ID: %s, Title:%s" % (i['id']['videoId'], i['snippet']['title']))

	#print(json.dumps(json_data, indent=4, sort_keys=True, ensure_ascii=False))