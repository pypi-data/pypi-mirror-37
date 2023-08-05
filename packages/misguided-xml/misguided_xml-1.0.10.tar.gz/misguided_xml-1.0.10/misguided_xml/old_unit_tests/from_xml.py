# encoding: utf-8

from future.builtins import str
from fdutil.string_scanner import StringScanner
from misguided_xml.xml import XML, XMLDeclaration

import pprint

if __name__ == u'__main__':

    x = XML(u"""<?xml version="1.0"?>
<!--Comment 1-->
<A>
    1234<![CDATA[[this is <some>
cdata!'"]]>
<!--Comment 2-->
    <B>5678</B>
    <C>6789</C>
<!--Comment 3-->
</A><!--Comment 4-->
""")
    print(str(x))
    pprint.pprint(x.dictionary)
    print(str(XML(u"""<?xml version="1.0"?>
<!--Comment 1-->
<PSLinput version="20160510211557"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns="urn:NNDS:CAB:SIMetadata:PermanentSeriesLink:Input:v1"
          xsi:schemaLocation="urn:NNDS:CAB:SIMetadata:PermanentSeriesLink:Input:v1 PermanentSeriesInput.xsd">
    <permanentSeason ui_descr="b Season 1"
                     permanent_season_id="145693">
                     1 1 1
    </permanentSeason>
    <permanentSeason ui_descr="â, î or ô"
                     permanent_season_id="145693">
                     2 2 2
<![CDATA[[ <cdata1>]]>
<!--Comment 2-->
<![CDATA[[ 'cdata2']]>
<!--Comment 3-->
<![CDATA[[ "cdata 4 ]]> 3 3 3
    </permanentSeason>
</PSLinput>""")))

    #

    XML(u"""<bookEvent service_key   = "2002"
                       event_id      = "1"
                       nominal_start = "2016-05-11T10:00:00Z"
                       /><!-- Channel:101, Time: 2016-05-11T10:00:00Z (57519.4166667) -->""")

    u'xmlns = "urn:NNDS:CAB:SIMetadata:PermanentSeriesLink:Input:v1"'

    #

    print(XML(u"""<?xml version="1.0"?>
<PSLinput version="20160510211557"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns="urn:NNDS:CAB:SIMetadata:PermanentSeriesLink:Input:v1"
          xsi:schemaLocation="urn:NNDS:CAB:SIMetadata:PermanentSeriesLink:Input:v1 PermanentSeriesInput.xsd">
    <permanentSeason ui_descr="b Season 1"
                     permanent_season_id="145693">
        <currentSeason last_season="false" xmlns:test="test:of:namespace">
            <test:title lang="eng" use="show">b</test:title>
            <test:of:namespace:title lang="eng" use="season">b: b Season 1</test:of:namespace:title>
            <test:seriesChain  series_id="123"/>
            <seriesChain  series_id="432"/>
        </currentSeason>
        <bookEvent service_key="2002"
                   event_id="555"
                   nominal_start="2016-05-10T11:00:00Z"/>
        <!-- Channel:101, Time: 2016-05-10T11:00:00Z (57518.4583333) -->
        <bookEvent service_key="2002"
                   event_id="1356"
                   nominal_start="2016-05-10T10:00:00Z"/>
        <!-- Channel:101, Time: 2016-05-10T10:00:00Z (57518.4166667) -->
    </permanentSeason>
    <permanentSeason ui_descr="b Season 2"
                     permanent_season_id="145694">
        <currentSeason  last_season="false">
            <title  lang="eng" use="show">b</title>
            <title  lang="eng" use="season">b: b Season 2</title>
        </currentSeason>
    </permanentSeason>
</PSLinput>"""))

    #

    someXMLDeclaration = u"""<?xml version="1.0" encoding="UTF-8"?>
    <tns:MediaRequest xmlns:tns="http://rsi.com/mediarequest">
        <tns:MediaId>MediaId</tns:MediaId>
    </tns:MediaRequest>"""
    print(XML(someXMLDeclaration))
    pprint.pprint(XML(someXMLDeclaration).dictionary)

    someXMLDeclaration = u'<?xml version="1.0"         encoding="utf-8" ?> '
    print(XMLDeclaration(StringScanner(someXMLDeclaration)))

    someXMLDeclaration = StringScanner(u"""<?xml version="1.0" encoding="UTF-8"?>
    <tns:MediaRequest xmlns:tns="http://rsi.com/mediarequest">
        <tns:MediaId>MediaId</tns:MediaId>
    </tns:MediaRequest>""")
    print(XMLDeclaration(someXMLDeclaration))
