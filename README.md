This script updates the Algolia Docs index to enable search on https://www.sticky.ai/docs


To get it working:


First up, you must install dependencies. To do this, run:

	./dependencies.bash

This checks whether python dependencies are installed and installs any that are missing.




Second, you must configure your API access so the script can download content from HubSpot and 
upload it into your Algolia search index.

	# Algolia accounts can have multiple apps and we need the ID of the app to use
	algolia_app_id

	# From that app in Algolia, we need the Admin API Key
	algoia_api_key

	# Hubspot blog id is also known as the content_group_id. Find it by signing in to Hubspot, 
	# navigating to the Docs blog and looking at the URL.
	# 		URL Example: https://app.hubspot.com/blog-beta/:portal_id/blogs/:blog_id/manage/posts/all
	hubspot_blog_id

	# Hubspot API key is found by signing in to Hubspot, clicking your profile image in the top right,
	# selecting "Integrations" from the dropdown and then "HubSpot API Key" on the resulting page.
	hubspot_api_key


It's recommended to keep these secrets as environment variables. If you need to save them in a file, see 
the example "config" file. You can put the values in that file and run `source config` to load them as 
environment variables.




Finally, to run the indexing process:
	
	python ./hs-search.py
