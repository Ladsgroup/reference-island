# Pipeline Result Schema Reference

## Lines

### `ItemLine`

Result of Pipe 1

```js
{
     "itemId": String // Wikibase QID of the item which contains unreferenced statements and whitelisted external source urls
     
}
```

### `MatchLine` 

Result of Pipes 2, 3, 4

```js
{
    "itemId": String, // Wikibase QID of the item which contains the statement claim
    "statement": StatementBlob, // The statement data to be matched
    "reference": ReferenceBlob // Data regerding the potential matched reference
}
```

## Blobs

### `StatementBlob`

```js
{
    "pid": String, // Wikibase PID of the property of the statement
    "datatype": String, // Wikibase data type see: https://www.wikidata.org/wiki/Special:ListDatatypes
    "value": Mixed // Data describing the matched value from a Wikibase
}
```

#### Potential Values

The `"value"` key in a statement can contain any of the value objects extracted from from a Wikibase JSON representation of an item. Same as the `"value"` key in [Wikibase JSON Response Data Value Documentation](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#data-values-json_datavalues). In the current implementation, supported values are for the following Wikibase data types:

* ##### `"string"` & `"url"`

	In these cases, `"value"` will be a `String` literal value containing the text or url to match e.g.: `"Ludwig Wittgenstein"` or `"http://www.example.com"`

	**Schema Example:**
	
	```js
	{
	    //...
	    "value": String
	}
	```

* ##### `"monolingualtext"`

	In this case the `"value"` is an object containing the text to match and the language it is written in.

	**Schema Example:**

    ```js
    {
        //...
        "value": {
            "text": String, 
            "language": String
        }
    }
    ```

* ##### `"quantity"`

	The `"value"` for quantity will be an object containing various information regarding quantity values. See [quantity](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#quantity-json_datavalues_quantity) in Wikibase JSON Response Documentation.

	**Schema Example:**

    ```js
    {
        //...
        "value": {
            "amount": String, // A string representation of a number including the sign (+/-)
            "unit": String, // 1 for unitless quantities or URI to Wikibase item of unit e.g. "https://www.wikidata.org/wiki/Q11573" 
            "upperBound": String, // Optional string rpresentation fo a number to encode uncertainty
            "lowerBound": String, // Optional string rpresentation fo a number to encode uncertainty
        }
    }
    ```

* #####  `"globe-coordinate"`

	In this case the `"value"` is an object containing coordinate information. For more information see [globecoordinate](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#globecoordinate-json_datavalues_globe) in Wikibase JSON Response Documentation.

	**Schema Example:**

    ```js
    {
        //...
        "value": {
            "latitude": Number, // Floating point number 
            "longitude": Number, // Floating point number 
            "altitude": null, // Unused, always null
            "precision": Number, // Floating point or scientific notation number, null when information is not provided
            "globe": String // URI to Wikibase item of the globe these coordinates are on, e.g. "http://www.wikidata.org/entity/Q2" 
        }
    }
    ```

* ##### `"time"`

    Here the `"value"` will be an object containing date and time information. For more information, see [time](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#time-json_datavalues_time) in Wikibase JSON Response Documentation.

    **Schema Example:**

    ```js
    {
        //...
        "value": {
            "time": String, // A **near** ISO 8601 time representaion
            "timezone": Number, // Unused, currently always 0 
            "before": Number, // Unused, currently always 0
            "after": Number, // Unused, currently always 0
            "precision": Number, // Integer between 0 - 14 represention the precision unit 
            "calendarmodel": String // URI to wikibase item of calendar model, e.g. "http://www.wikidata.org/entity/Q1985727"
        }
    }
    ```

* ##### `"wikibase-item"`

    For this data type `"value"` will be an object containing information about the item id. For more information, see [wikibase-entityid](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#wikibase_entityid-json_datavalues_entityid) in Wikibase JSON Response Documentation.

    **Schema Example**:

    ```js
    {
        //...
        "value": {
            "entity-type": String, // Will always be "item" in this case
            "id": Strong, // Wikibase QID
            "numeric-id": Number // Numeric representation of the above id
          }
    }
    ```

### `ReferenceBlob`

```js
{
    "referenceMetadata": {
        /** 
         * A key value pair representing a "stated in" claim:
         * Key: Always "P248" in our case (Wikidata "stated in" PID)
         * Value: Wikibase QID for an item representing the reference source
         **/
        String: String,
        /** 
         * A key value pair representing an "extrnal id" claim:
         * Key: Wikibase PID representing the extrnal id for the reference source 
         * Value: The id value for the above external id
         **/
        String: String,
        /** 
         * A key value pair representing a "reference URL" claim:
         * Key: Always "P854" in our case (Wikidata "reference URL" PID)
         * Value: The url the data was extracted from
         **/
        String: String,
        "dateRetrieved": String // GMT date-time representation formatted as YYYY-MM-DD HH:MM:SS
    },
    "extractedData": [ Mixed ] // An array of data extracted for this item
}
```

