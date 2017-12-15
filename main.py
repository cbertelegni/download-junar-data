import requests
import os
import csv
from time import sleep
from conf import api_url, auth_key

params = {
	'auth_key':auth_key
}

def get_methods_list():

	manifest = []
	r = requests.get(api_url, params=params)

	manifest.append([ "title", "category_name", "description", "created_at", "file_name", "endpoint" ])
	for method in r.json():
		method_name= method["guid"]
		api_method = "%s/data.csv" % method_name
		file_name = "data/%s.csv" % method_name
		url_method = os.path.join( api_url, api_method)
	
		""" Save data """
		r_data = requests.get( url_method, params=params )
		with open(file_name, "w") as file:
			file.write(r_data.text)
			file.close()
		
		""" Append method description to manifest """
		manifest.append([ method["title"], method["category_name"], method["description"], method["created_at"], file_name, (method["endpoint"] if "endpoint" in method else "") ])
		print("%s saved..." % file_name)
		sleep(1)

	""" Save manifest.csv"""
	outfile = open('manifest.csv', 'w')
	writer = csv.writer(outfile)
	for row in manifest:
		writer.writerow(row)
	outfile.close()


if __name__ == "__main__":
	get_methods_list()