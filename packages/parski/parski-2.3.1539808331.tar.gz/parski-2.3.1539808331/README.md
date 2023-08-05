# Parski

### Python Module for accessing and parsing data from the inventory API.


## Install

    pip install -I parski

Make sure to include the -I to overwrite to the newest version.
    
## Import
In your python file, put the import statement at the top:

    import parski
    
## Methods

- get_data
- filter_data

<br><br>

# get_data

get_data grabs data from either the an api or a local file, saves it to a local file, and outputs the data.  Currently, the headers of the api request are hard-coded to that of the AWS inventory api, but the plan is to take in the headers when the method is called to make the module more flexible in the future.

A sample method call would look something like this

    data = parski.get_data(url='https://api_data_place/v2/dataset', file_name='output.json', source="file").data

This call would try to upload the data from 'output.json' and then would try to make the api call if the file doesn't exist.  If this is the case, it would then output the data from the api to a new file 'output.json' and return it as the variable data.

## Example Usage

    get_data_object = parski.get_data(url=None, file_name='output.json', source="file", key_var="PCT_API_READ_KEY", silent=False, write_file=True)
    
    data = get_data_object.data
    status_code = get_data_object.status_code
    error_msg = get_data_object.error_msg

## Input Parameters

**url** (default: None): url of the api call.  No api call will be attempted if left blank

**file_name** (default: 'output.json'):  the file name of both the file load and the file write relative to the current directory. 

**source** (default: 'file'):  the preferred source to pull the data from.  If the 'file' option is chosen, parski will attempt to get the data from the file before attempting an api request defined in the url parameter.  If the 'api' option is chosen, parski will ignore any existing file and pull straight from the api.  The default is 'file' to save on time, but if you need to be sure that the data is up-to-date, you can feed it 'api'.

**key_var** (default: 'PCT_API_READ_KEY'):  Choose what environment variable to load in when accessing the API.  It's set to the default PCT_API_READ_KEY, but if you're a Grant-like person and can't stick to convention, you can change it to whatever you have saved your api key under.

**silent** (default: False): set to True to suppress console output.

**write_file** (default: True):  set to False to prevent writing file.

## Output Parameters

**data** : The data found by the get request.

**status_code**:  HTTP status code for the request.

**error_msg**:  Error message associated with any failure of the get request.

## Empty Example

A call of:

    data = parski.get_data().data

would try to load from 'output.json', and fail if 'output.json' can't be found, since no api url is specified.

<br><br>

# filter_data

filter_data takes in a dataset and one or more search dictionaries and returns the items in the dataset that meet the criteria of the search dictionaries.

A basic dictionary and call would look like so:

    search_dict = {'Alias': 'digital-public-cloudops'}

    results = parski.filter_data(data, search_dict).results

Where results would be all the items in data that have an Alias containing "digital-public-cloudops".

## Example Usage

    filter_data_object = parski.filter_data(data, search_input, max_results=5000, silent=False)
    
    results = filter_data_object.results
    metrics = filter_data_object.metrics

## Input Parameters

**max_results** (default: 5000): change the maximum amount of returned results

**silent** (default: False): set to True to suppress console output.

## Output Parameters

**results** : The data elements that passed the filtering.

**metrics** : Dict of metrics for the filtering process contaning the counts of missing keys and regex errors


## Advanced Usage

filter_data can search as deep as required in any data structure, as long as the search dictionary matches the structure.  A more complicated example:

    search_dict = {'NetworkInterfaceSet': [{'PrivateIpAddresses': [{'PrivateIpAddress': '172.31.48.10'}]}]}

This would search the dataset for items with a key 'NetworkInterfaceSet', then for an element in an array inside that is an object with key 'PrivateIpAddresses', then for an element inside the array stored in 'PrivateIpAddresses' that has an object with key 'PrivateIpAddress', and check if the value of that key is '172.31.48.10'.

If that seems needlessly convoluted, it's not.  That's where the PrivateIpAddress natively lives in the API response before it's bubbled up to the top level key of 'PrivateIpAddress'.

In any case, the filter_data can go as deep as you need it to go with no additional configuration

### A word on arrays

Any time an array is part of the data structure, if an entry exists in the search dictionary, the filter function will search all elements of the array, and return the item in results if it exists at any index.

If multiple array elements exist in the search dictionary, the filter function will return the item only if all the array items (and any deeper structures) exists in any order in the array.  However, while the order of the array elements doesn't matter, the parameters expressed in the SAME element of a search dictionary array must exist in the SAME element of the data.

For instance:

    search_dict = {'Tags': [{'Key': 'Name', 'Value': 'ISS'}, {'Key': 'env', 'Value': 'prod'}]}

would return any data items with a Tag with Key 'Name' and 'Value' ISS' AND ANOTHER Tag with Key 'env' and 'Value' 'prod'.  It would not, however, return a data item with a Tag with Key 'Name' and Value 'prod', since that combination is not in the same element of the array in the search dictionary.

In other words,

    search_dict = {'Tags': [{'Key': 'Name', 'Value': 'ISS'}, {'Key': 'env', 'Value': 'prod'}]}

is a very different search than:

    search_dict = {'Tags': [{'Key': 'Name', 'Value': 'prod'}, {'Key': 'env', 'Value': 'ISS'}]}

### Searching by Launch Time

To search for all resources launched within a certain time frame, use either format below:

    2016-06-01/2017-01-31
    (2016/06/01)(2017/01/31)

Example:

    search_dict = {'LaunchTime': '2016-06-01/2017-01-31'}

The example above would return all resources launched between (and including) June 1, 2016 and January 31, 2017.

You can also retrieve all resources launched AFTER a certain date by entering only the BEGINNING date.

    search_dict = {'LaunchTime': '2015-12-31'}

This example would return all resources launched December 31, 2015 or after.


### AND vs OR

Any elements in a search dictionary will be AND'd together.  However, in place of a single search dictionary, an array of search dictionaries can be input to the filter_data function.  The results of each search dictionary will be OR'd together to create the final results.   For instance:

    search_array = [{'PrivateIpAddress': '10.231.46.213'}, {'PrivateIpAddress': '10.231.46.101'}, {'PrivateIpAddress': '10.231.46.178'}]

    results = parski.filter_data(data, search_array)

would return the data from all three IP addresses.


### Additional Information

The default mode for searching is actually search paths rather than search dictionaries.  The filter function actually converts the search dictionaries to search paths before running the query, but it supports search dictionaries, since they are more human-readable.  An array of search paths, look something like this:

    [{'path': [0, u'Alias'], 'value': u'digital-public-cloudops'}, {'path': [0, u'Tags', 0, u'Key'], 'value': u'env'}, {'path': [0, u'Tags', 0, u'Value'], 'value': u'dev'}]

You may find this structure easier for constructing queries automatically.
