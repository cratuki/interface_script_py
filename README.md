Message-oriented data-interchange format.

# Overview

You can get most of the way to understanding Interface Script if you
think of it as being like CSV, but able to support more dimensions.

Example of an Interface Script stream,
```
# assert the message vectors
i person name age
i org name

# messages
person Jane 34
person Steve 33
org "Piccadilly Steamship Company"
org "Victoria Square Consulting"
```

The header lines start with 'i'. That is short for 'interface'. It declares
the types of message that the sender things is can send.

The receiver should check that this matches its own assumptions.

The remaining lines are messages of those forms.


# Key idea: Interface Assertions, Pereto Principle

Interface Assertion address the most common source of bugs seen in message
interchange: field mismatch. (This is often caused by version misalignment.)

When there are different assumptions between the sender and receiver, the
receiver will fail-fast.

# Key idea: All fields are sent as string

This format forces the receiver to parse away from strings for all fields. For
this reason, it should be more robust in practice than interchange formats
which have unenforced typing. (e.g. think of a time when you have received NaN
in a JSON message, and struggled to work out what was doing on.)

# Quite useful for

Configuration files.

Files being sent between systems.

Flexible, easy-to-implement network protocols.

# Less useful for

If you genuinely need complex tree structures, it's a struggle with Interface
Script. In that case, you probably need a document-oriented data interchange
format like XML. (Modest nesting is practical in IS - see the heading Nesting
below.)

# Setup

```
python3 -B -m venv venv
. venv/bin/activate
python3 -B test_is
```

# How to use

## Producer

Write strings. The format is simple enough that it does not need a library.

## Receiver

Here is an example of how you would receive the message format defined above.
Note that we use reflection against the handler. For each message name, you
need a method `on_message_name`, with fields matching the document structure.

Example parse code,
```
import interface_script

DATA = '''
    # assert the message vectors
    i person name age
    i org name

    # messages
    person Jane 34
    person Steve 33
    org "Piccadilly Steamship Company"
    org "Victoria Square Consulting"
'''

class Handler:

    def on_person(self, name, age):
        print("Person: %s/%s"%(name, age))

    def on_org(self, name):
        print("Org: %s"%(name))

def main():
    handler = Handler()
    ob = interface_script.InterfaceScriptParser(handler)
    ob.parse(DATA)

if __name__ == '__main__':
    main()
```

# Details

## Support for other languages

It should be easy to port.

A new consumer would take somewhere between minutes and hours to write. The
line tokeniser is fiddly if you do not have a library for it. But you can find
the logic you need in `interface_script/parser.py`.

## Newlines and whitespace

Windows and unix style will work.

Whitespace is not significant: lines get stripped when they are parsed.

For situations where you needed to send newlines as part of a string, have a
convention of exchanging those fields using base64.

## Encoding

The recipient should assume UTF-8 encoding, and this library does. The
recipient can reject UTF-8 on a business-logic level if they want to.

## Not an IDL

Interface Script is not an Interface Definition Language (IDL).

In an IDL, the recipient uses information from the sender to understand the
structure of the messages. This format should not be used like that.

Here, the sender is asserting the interface as they understand it. If the
receiver disagrees, then it should fail fast.

The author has a background dealing with exchange messaging. A problem that
happens in that domain is that you get two thirds of the way through a day,
and then a message comes through that you don't understand and things start
crashing.

## Compare to CSV

CSV is message-centric. So is Interface Script.

CSV is non-trivial to parse due to quotation mark blocks. A skilled developer
could write a parser inside an hour. All this is also true of Interface
Script. Their notations are similar.

CSV can describe up to two dimensions (it is tabular). Interface Script can
describe an arbitrary number of dimensions.

CSV is weakly defined. Some usages involve a header, others skip the header.
Interafce Script is more strongly defined: you should always declare your
dimensions.

CSV can use its header for the purpose of interface assertions. Interface
Script is more opinionated: you must declare your vectors, and these
declarations should be as assertion (and not regarded as an IDL).

## Compare to JSON

JSON can be document-centric or message-centric. Interface Script is
message-centric.

JSON parsing is more complex than CSV/IS, but a skilled developer could build
a recursive-descent JSON parser within a day.

JSON is more verbose than Interface Script.

JSON lacks interface assertions.

JSON has weak type mechanisms. Interface Script has no type mechanisms.

JSON supports tree structures easily. Interface Script does not.

## Compare to YAML

YAML is document-centric. Interface Script is message-centric.

YAML is harder to parse than JSON, and therefore also harder than IS.

YAML is more verbose than Interface Script.

YAML lacks interface assertions.

YAML supports custom data types. Interface Script has no type mechanisms.

YAML supports tree structures easily. Interface Script does not.

## Compare to XML

XML is document-centric. Interface Script is message-centric.

XML is complex to parse. Writing a parser to support the full spec might take
a single developer a couple of years. People often uses subsets of XML. You
could build a parser to handle the basics inside a day.

XML is verbose, moreso than YAML and JSON.

XML lacks interface assertions.

XML schema is more complicated than interface assertions.

XML has a clear encoding strategy.

XML supports tree structures easily. Interface Script does not.

## Nesting

You can create nested data structures by convention. Example,
```
i bookshelf n
i x_bookshelf
i book title publisher

bookshelf 0
    book "Java NIO" "O'Reilly"
    book "Graphics Programming in Turbo C" "Wiley"
x_bookshelf
```

Stick to lower-case characters and the underscore character. Consider that
your handler method will need to have a valid python message name. For
example, `on_x_bookshelf`.


## Complexity

If you find your format getting complex, review whether you should be doing
all those things in a single communication channel.

Could you instead break the problem up into a few smaller protocols?

## Code source

Adapted from a personal unreleased project, Orchid (2016).

