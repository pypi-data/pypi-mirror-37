
# XML (source file)

Classes to support reading, modifying and writing XML. Note that namespace support is unfinished, so don't use if you need that!
           
     

## XMLDeclaration (Class)

Validates the declaration and extracts and stores any atrributes. i.e. makes sure it looks like `<?xml attr1="attr1 value" attrN="attrN value?>` and is on a single line.

Used by XML.


## XMLComment (Class)

Stores the comment string.  When retrieved as a string, wraps the comment appropriately with opening and closing strings. i.e. stores `"this is a comment"`, regurgitates `"\<!--this is a comment-->"`

Used by XML.

## XMLCDATA (Class)

Stores the CDATA string.  When retrieved as a string, wraps the comment appropriately with opening and closing strings. i.e. stores `"A9043BC658EFBA6"`, regurgitates `"\<![CDATA[[A9043BC658EFBA6]]>"`

Used by XML.


## XML (Class)

The XML extracts and stores any declaration, comments, values, CDATA and elements. namespaces are extracted, but aren't properly functional yet.

Taking this element:
```xml
<PhysicalAsset assetName="CAS-CASBNU">
	<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
	<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
	<MediaReferenceName>BL77318</MediaReferenceName>
</PhysicalAsset>
```
We have an object with these values:

Field         | Description
--------------|------------
`tag`         | `PhysicalAsset`
`attributes`  | `{"assetName" : "CAS-CASBNU"}`
`children`    | `[XMLComment, XMLComment, XMLElement]`

The children have these values:

Field         | Description
--------------|------------
`comment`     |  ` assetName = concatenation of <TypeofElement> and <FormatofElement> above `

Field         | Description
--------------|------------
`comment`     |  ` From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  `

Field         | Description
--------------|------------
`tag`         | `MediaReferenceName`
`value   `    | `BL77318`

### Useful methods:

Note that a number of these methods should really be considered private, but I wasn't aware of the Python convention for indicating this when it was originally written (ditton use of camelCase).  It's probably worth marking these as private, e.g. rename `getTag` to `__getTag`.


#### find

parameter         | Description
------------------|------------
`element` | a dictionary containing search criteria
`value` | a dictionary containing search criteria
`attribute` | a dictionary containing search criteria
`element` | a dictionary containing search criteria


search_criteria dictionary:
```python        
{'Element'   : """Describes the path to the node of the XML tree
                   e.g. <MediaRequest><VersionNumber>
                   Attributes may also be added, which can help
                   narrow the search when there are many elements
                   of the same type at the same level.
                   e.g. <MediaRequest><AudioTrack trackNumber="1">""",
                 
 'Value'     : """Only nodes with this value will be matched.
                  This is useful for checking that a value
                  is present.""",
                 
 'Attribute' : """If a particular attribute of an element is
                  what we're interested in rather than the
                  whole element, then the named attribute
                  value is returned."""}
```                        

Examples:

```python
>>> element = XML.XMLElement("""<MediaRequest OriginatingSystem="OSCAR">
...                                 <VersionNumber>12345</VersionNumber>
...                                 <AudioTrack TrackNumber="1">
...                                     <Level>-23</Level>
...                                 </AudioTrack>
...                                 <AudioTrack TrackNumber="2">
...                                     <Level>-23</Level>
...                                 </AudioTrack>
...                             </MediaRequest>""")
>>> 
>>> print element.search({'Element':'<MediaRequest><AudioTrack TrackNumber="1">'})
<AudioTrack TrackNumber="1">
    <Level>-23</Level>
</AudioTrack>
>>> 
>>> print element.search({'Element':'<MediaRequest><VersionNumber>',
...                        'Value'  :'12345'})
<VersionNumber>12345</VersionNumber>
>>> 
>>> print element.search({'Element':'<MediaRequest>',
...                       'Attribute':'OriginatingSystem'})
OSCAR
```

#### exists

parameter         | Description
------------------|------------
`search_criteria` | See search

Returns a True if there's a hit:

```python
>>> print element.exists({'Element':'<MediaRequest><VersionNumber>'})
True
>>> 
>>> print element.exists({'Element':'<MediaRequest><SomethingMadeUp>'})
False 
```

#### dictionary

parameter           | Description
--------------------|------------
`include_first_tag` | Defaults to False. See below for an example. Usually, if you have an element, you know where you are in the tree, and the tag of the element is an inconvenience.

This returns the XMLElement tree tags and value as a Python dictionary:

```python
>>> import XML
>>> import pprint
>>> 
>>> xml = XML.XML("""<?xml version = "1.0" encoding = "UTF-8"?>
...                  <MediaRequest OriginatingSystem="OSCAR" attribute2="OSCAR">
...                      <VersionNumber>12345</VersionNumber>
...                      <AudioTrack TrackNumber="1">
...                          <Level someattr="x">-1</Level>
...                      </AudioTrack>
...                      <AudioTrack TrackNumber="2">
...                          <Level>-2</Level>
...                      </AudioTrack>
...                      <AudioTrack TrackNumber="3">
...                          <Level>-3</Level>
...                      </AudioTrack>
...                  </MediaRequest>""")
>>> 
>>> media_request = xml.find({'Element':'<MediaRequest>'})
>>> pprint.pprint(media_request.dictionary())
{'@OriginatingSystem': u'OSCAR',
 '@attribute2': u'OSCAR',
 u'AudioTrack': [{'@TrackNumber': u'1',
                  u'Level': {'@someattr': u'x', u'Level': u'-1'}},
                 {'@TrackNumber': u'2', u'Level': u'-2'},
                 {'@TrackNumber': u'3', u'Level': u'-3'}],
 u'VersionNumber': u'12345'}
>>> 
>>> audio_track_1_element = xml.find({'Element':'<MediaRequest><AudioTrack TrackNumber="1">'})
>>>
>>> pprint.pprint(audio_track_1_element.dictionary())
{'@TrackNumber': u'1', u'Level': {'@someattr': u'x', u'Level': u'-1'}}
>>>
>>> pprint.pprint(audio_track_1_element.dictionary(include_first_tag=True))
{u'AudioTrack': {'@TrackNumber': u'1',
                 u'Level': {'@someattr': u'x', u'Level': u'-1'}}}
```112

If the element has attributes, they're added to the dictionary with an `'@'` prefix.  If it's a leaf node with a value and attributes, rather than just a value, a dictionary is created containing the attributes and value, with the key for the value being the tag.

#### find

parameter    | Description
-------------|------------
`path`       | a list of tags, which can include attributes
`whereValue` | a value to match.


Search for a matching element:

```python
$ python
Python 2.7.8 (v2.7.8:ee879c0ffa11, Jun 29 2014, 21:07:35) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import XML
>>> element = XML.XMLElement("""<PhysicalAsset assetName="CAS-CASBNU">
...                                 <!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
...                                 <!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
...                                 <MediaReferenceName>BL77318</MediaReferenceName>
...                                 <Appendix>1</Appendix>
...                                 <Appendix>2</Appendix>
...                                 <Appendix>3</Appendix>
...                                 <Appendix>4</Appendix>
...                             </PhysicalAsset>""")
>>> element.find(path = [u'PhysicalAsset assetName="CAS-CASBNU"',u'MediaReferenceName'])
<XML.XMLElement object at 0x1025e8c10>
>>> element.find(path = [u'PhysicalAsset assetName="CAS-CASBNU"',u'MediaReferenceName']).value
u'BL77318'
>>>
```

`None` is returned if there are no matches:
```python
>>> element.find(path = [u'PhysicalAsset assetName="TAPE"',u'MediaReferenceName']) == None
True
```

A list of elements is returned if there are more than one match:
```python
>>> element.find(path = [u'PhysicalAsset',u'Appendix'])
[<XML.XMLElement object at 0x1025e8b50>, <XML.XMLElement object at 0x1025e8c50>, <XML.XMLElement object at 0x1025e8c90>, <XML.XMLElement object at 0x1025e8cd0>]
>>> element.find(path = [u'PhysicalAsset',u'Appendix'])[2].value
u'3'
>>> 
```

#### remove


parameter    | Description
-------------|------------
`path`       | a list of tags, which can include attributes
`value`      | a value to match.

Performs a `find` and removes the found element or elements:

```python
>>> print element
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
    <Appendix>1</Appendix>
    <Appendix>2</Appendix>
    <Appendix>3</Appendix>
    <Appendix>4</Appendix>
</PhysicalAsset>
>>> 
>>> element.remove(path=[u'PhysicalAsset assetName="CAS-CASBNU"',u'Appendix'], value = '2')
>>> print element
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
    <Appendix>1</Appendix>
    <Appendix>3</Appendix>
    <Appendix>4</Appendix>
</PhysicalAsset>
>>>
>>> element.remove(path=[u'PhysicalAsset assetName="CAS-CASBNU"',u'Appendix'])
>>> print element
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
</PhysicalAsset>
```

#### add

parameter    | Description
-------------|------------
`bytes`      | a string or a StringReader object

Adds XML as a childe of the element:

```python
>>> 
>>> element.add("""<Appendices/>""")
>>> 
>>> print element
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
    <Appendices/>
</PhysicalAsset>
>>> 
```

#### addAtPath

parameter    | Description
-------------|------------
`path`       | a list of tags, which can include attributes
`bytes`      | a string or a StringReader object

Adds XML as a childe of the element:

```python
>>> element.addAtPath(path  = [u'PhysicalAsset',u'Appendices'],
...                   bytes = """<title>Appendix 1</title>""")
>>> 
>>> print element
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
    <Appendices>
        <title>Appendix 1</title>
    </Appendices>
</PhysicalAsset>
```

#### replace

parameter    | Description
-------------|------------
`bytes`      | a string or a StringReader object
`path`       | a list of tags, which can include attributes
`value`      | a value to match.

Substitues an element for the new XML:

```python
>>> 
>>> element.replace(bytes = """<index>
...                                <page>1</page>
...                                <value>How to use XMLElement</value>
...                             </index>""",
...                 path  = [u'PhysicalAsset',u'Appendices'])
>>> print element
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
    <index>
        <page>1</page>
        <value>How to use XMLElement</value>
    </index>
</PhysicalAsset>
>>> 
```

#### replaceValueAtPath

parameter    | Description
-------------|------------
`path`       | a list of tags, which can include attributes
`whereValue` | (optional) a value to match.
`newValue`   | The new value. Optional. If `None`, will remove the element at the path.

Replaces the value at the element found at the path with the new value.:

```python
>>> 
>>> element.replaceValueAtPath(path     = [u'PhysicalAsset',u'index',u'value'],
...                            newValue = "Confessions of a Python Developer")
>>> print element 
<PhysicalAsset assetName="CAS-CASBNU">
<!-- assetName = concatenation of <TypeofElement> and <FormatofElement> above -->
<!-- From spec: "List of tape storage formats : BetaSp; DigiBeta; MiniDV; etc."  -->
    <MediaReferenceName>BL77318</MediaReferenceName>
    <index>
        <page>1</page>
        <value>Confessions of a Python Developer</value>
    </index>
</PhysicalAsset>
```





# [StringReader][StringReader]

Used by XML to navigate the XML string, search for tags, extract data etc.

You may see this class used occasionally in tests. That's no longer required. XML's initialisation used to require data in this form.  Now it tries to convert data to StringReader first.
