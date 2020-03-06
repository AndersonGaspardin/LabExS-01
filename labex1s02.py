#pandas
import requests
import json
import csv


token = input("Informe seu token do github: ")

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer '+token,
}

data_file = open('output.csv', 'w') 

csv_writer = csv.writer(data_file) 
        
endCursor = "null"

count = 0

isHeader = 1

while(count < 20):
	data = '''
    {
    search(query: "stars:>100", type: REPOSITORY, first: 50{AFTER}) {
        pageInfo{
        hasNextPage
        endCursor
    }
    edges {
      node {
        ... on Repository {
          nameWithOwner,
          stargazers {
            totalCount
          }
          primaryLanguage {
          name: name
          }
        }
      }
    }
  }
}

'''
	response = requests.post('https://api.github.com/graphql', headers=headers, data=data)

	if response.status_code != 200:
		print (f"Problema!\nRode novamente ou revise o codigo.")
	
	json_data = json.loads(response.text)

	for repositorios in json_data['data']['search']['nodes']:
		
		if isHeader:
			header = repositorios.keys()
			csv_writer.writerow(header)
			isHeader = 0
			
		csv_writer.writerow(repositorios.values()) 
	
	
	endCursor = '\\"'+json_data['data']['search']['pageInfo']['endCursor']+'\\"'	
	
	count = count + 1
	
data_file.close() 