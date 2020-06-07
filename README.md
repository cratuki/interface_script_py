Message-oriented data-interchange format.


# Overview

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

The header lines start with 'i'. That is short for 'interface'.

Those header asserts the structure of messages that the sender expects the
receiver to be able to handle.

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

# Useful for

Configuration files.

Files being sent between systems.

Bespoke network protocols.

# Setup

```
python3 -B -m venv venv
. venv/bin/activate
python3 -B test_is
```

# How to use

Producer: Write strings. The format is simple enough that it does not need a
library.

Receiver: look in the test module for a parsing use-case and example code.


# Details

## Original Inspiration

I was working in a domain where I saw people exchanging documents by email. It
was a stupid reality of that situation.

A number of simple issues got pushed to developers due to the complex file
format.

This format allows a larger pool of people to easily support a system. (You
can give them tools to validate their documents before sending.)

The format turned out to be useful for a far broader range of things than just
that. It has become my go-to interchange mechanism. For most purposes, I find
it a better tradeoff than XML, JSON and YAML.

## Support for other languages

It should be easy to port.

A new consumer for it in something between minutes and hours. The most
difficult part of writing a consumer is likely to be the line tokeniser. You
will find business logic for this in `interface_script/parser.py`.

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

## Compare to XML

XML is document-centric. Interface Script is message-centric.

XML is more verbose.

XML lacks interface assertions.

XML makes tree structure easy. In practice, this if often a source of
complexity.

XML schema is more complicated than interface assertions.

XML has a clear encoding strategy.

## Compare to JSON

JSON can be document-centric or message-centric. Interface Script is
message-centric.

JSON is more verbose.

JSON lacks interface assertions.

JSON is somewhat typed. Interface Script is text tokens. The developer should
validate everything.

## Nesting

You can create nested data structures by convention. Example,
```
i bookshelf n
i x/bookshelf
i book title publisher

bookshelf 0
    book "Java NIO" "O'Reilly"
    book "Graphics Programming in Turbo C" "Wiley"
x/bookshelf
```

## Complexity

If you find your format getting complex, review whether you should be doing
all those things in a single communication channel.

Could you instead break the problem up into a few smaller protocols?

## Code source

Adapted from a personal unreleased project, Orchid (2016).

