# Web Recon
[Source Code](https://github.com/adam-phillipps/recon/tree/master/web_recon/webrecon)
This package is designed to help users search the interwebz for pretty much anything (legal).  You can use this package, which wraps other cloud packages and SDKs for ease of use and integration.

## Goals of this project
- Create a single source code repository that can handle searching
- Allow other projects to use the search with minimal integration and code changes
	- Serverless frameworks like AWS Lambda, Google Cloud Functions, and Azure Automations.  If the platform allows python with dependencies, `webrecon` _should_ be able to run there.
- Container clusters like ECS, EKS, Kubernetes in general, etc.  All the Dockers, basically.

## Use
### Searching with Google CSE
To use Google Custom Search Engine you will want to use the `gcse.search()` function.  You can include the library in your source code by `import`ing `webrecon.gcse`.  See the [docstring](https://github.com/adam-phillipps/recon/blob/master/web_recon/webrecon/webrecon/gcse.py) for up to date notes on params etc.
You can send in any of the parameters that the GCSE API from python offers up and a couple more too.
The updated list of params from the Alphabet-Googlez folks can be found [here](https://developers.google.com/resources/api-libraries/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html) and the current supported list of params for the search from `webrecon.gsce.search()`


- `q` <String>: This parameter is the actual search term.  It can be helpful to use [Google search operators](https://ahrefs.com/blog/google-advanced-search-operators/).
- `filters` <[String]>: Send a list of keys that might be found in the results from the search so that you can filter the results you deal with in your actual final result set.
- `key` <String>: The developer key for Google.  You can find this in your GCSE console (manually log into the browser, amigoritos).
- `cx` <String>: The GCSE ID.  Same story as the `key` parameter.
- `kwargs` <KeyWord Args>: You can pass any number of arguments in as key value pairs, at the end of your parameters list.  These arguments will be dutifully passed along to the actual Google custom search method.

*Example*

	from webrecon import gcse
	...
	res = gcse.search('intext:HUGO BOSS Genesis 2 Virgin Wool Dress Pants',
					  'title',
					  'link',
					  num=3,
					  exactTerm='Genesis 2')

	print(res)
	[
		{
			'title': 'Hugo Boss Pants',
			'link': 'https://www.macys.com/shop/b/hugo-boss-pants?id=78110'
		},
		{
			'title': 'HUGO BOSS 100% Wool Pants for Men for sale | eBay',
			'link': 'https://www.ebay.com/b/HUGO-BOSS-100-Wool-Pants-for-Men/57989/bn_4243898'
		},
		{
			'title': "HUGO BOSS | Trousers for Men | Elegant and Casual Men's Trousers",
			'link': 'https://www.hugoboss.com/us/men-pants/'
		}
	]