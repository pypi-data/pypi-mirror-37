# PowerPigeon

PowerPigeon is a async model-based RethinkDB handler. It allows for more structured RethinkDB data, which can be hard to get with NoSQL databases.

## Installation

To install, simply download `PowerPigeon` from PyPi.

## Usage

PowerPigeon is meant to be used inside of async functions. However, we need to create the connection first and in most situations this will want to be done outside of the async function. You can use something like the following code for this:

```py
import rethinkdb as r

r.set_loop_type("asyncio")
connection = <loop>.run_until_complete(r.connect(<connection args>))
```

Everything in the rest of this guide assumes that you are inside of a async function.

PowerPigeon is based on models. A model is a class that contains attributes and meta data. Attributes tell the model what items should be in database items, what type they should be and what they do (whether they are a ID, required or have a default). Attributes should be based on the `BaseAttribute` class which contains the initialisation code needed and the is the base class for attributes. Attributes must also contain a async `encode` and `decode` function. PowerPigeon contains several default attributes:
- `BooleanAttribute` - The attribute used for booleans.
- `TextAttribute` - The attribute used for text.
- `NumberAttribute` - The attribute used for numbers (accounts for the int32 limitation in RethinkDB).
- `JSONAttribute` - The attribute used for JSON.
- `BytesAttribute` - The attribute used for bytes.
- `UTCDateTimeAttribute` - The attribute used for UTC date/time.
- `DateTimeAttribute` - The attribute used for timezone aware date/time.

Attributes are to be initialised in the model. You can use the following keyword arguments with them:
- `required` - This sets if a item is required.
- `item_id` - This sets the item ID. One of these attributes is required.
- `default` - This sets the default item that goes here if the item does not contain it.

This makes our example model look like the following (we will add the `Meta` class later):
```py
class DemoModel(PowerPigeon.Model):
    name = TextAttribute(item_id=True)
    cool = BooleanAttribute(required=True)
```
