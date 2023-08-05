#
#  BEGIN LICENSE
#  Copyright (c) Blue Mind SAS, 2012-2016
# 
#  This file is part of BlueMind. BlueMind is a messaging and collaborative
#  solution.
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of either the GNU Affero General Public License as
#  published by the Free Software Foundation (version 3 of the License).
# 
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# 
#  See LICENSE.txt
#  END LICENSE
#
import requests
from netbluemind.python import serder

class BaseDirEntryQuery :
    def __init__( self):
        self.kindsFilter = None
        self.accountTypeFilter = None
        self.nameFilter = None
        self.systemFilter = None
        self.archiveFilter = None
        self.from_ = None
        self.size = None
        self.entryUidFilter = None
        pass

class __BaseDirEntryQuerySerDer__:
    def __init__( self ):
        pass

    def parse(self, value):
        if(value == None):
            return None
        instance = BaseDirEntryQuery()

        self.parseInternal(value, instance)
        return instance

    def parseInternal(self, value, instance):
        from netbluemind.directory.api.BaseDirEntryKind import BaseDirEntryKind
        from netbluemind.directory.api.BaseDirEntryKind import __BaseDirEntryKindSerDer__
        kindsFilterValue = value['kindsFilter']
        instance.kindsFilter = serder.ListSerDer(__BaseDirEntryKindSerDer__()).parse(kindsFilterValue)
        from netbluemind.directory.api.BaseDirEntryAccountType import BaseDirEntryAccountType
        from netbluemind.directory.api.BaseDirEntryAccountType import __BaseDirEntryAccountTypeSerDer__
        accountTypeFilterValue = value['accountTypeFilter']
        instance.accountTypeFilter = __BaseDirEntryAccountTypeSerDer__().parse(accountTypeFilterValue)
        nameFilterValue = value['nameFilter']
        instance.nameFilter = serder.STRING.parse(nameFilterValue)
        systemFilterValue = value['systemFilter']
        instance.systemFilter = serder.BOOLEAN.parse(systemFilterValue)
        archiveFilterValue = value['archiveFilter']
        instance.archiveFilter = serder.BOOLEAN.parse(archiveFilterValue)
        from_Value = value['from']
        instance.from_ = serder.INT.parse(from_Value)
        sizeValue = value['size']
        instance.size = serder.INT.parse(sizeValue)
        entryUidFilterValue = value['entryUidFilter']
        instance.entryUidFilter = serder.ListSerDer(serder.STRING).parse(entryUidFilterValue)
        return instance

    def encode(self, value):
        if(value == None):
            return None
        instance = dict()
        self.encodeInternal(value,instance)
        return instance

    def encodeInternal(self, value, instance):

        from netbluemind.directory.api.BaseDirEntryKind import BaseDirEntryKind
        from netbluemind.directory.api.BaseDirEntryKind import __BaseDirEntryKindSerDer__
        kindsFilterValue = value.kindsFilter
        instance["kindsFilter"] = serder.ListSerDer(__BaseDirEntryKindSerDer__()).encode(kindsFilterValue)
        from netbluemind.directory.api.BaseDirEntryAccountType import BaseDirEntryAccountType
        from netbluemind.directory.api.BaseDirEntryAccountType import __BaseDirEntryAccountTypeSerDer__
        accountTypeFilterValue = value.accountTypeFilter
        instance["accountTypeFilter"] = __BaseDirEntryAccountTypeSerDer__().encode(accountTypeFilterValue)
        nameFilterValue = value.nameFilter
        instance["nameFilter"] = serder.STRING.encode(nameFilterValue)
        systemFilterValue = value.systemFilter
        instance["systemFilter"] = serder.BOOLEAN.encode(systemFilterValue)
        archiveFilterValue = value.archiveFilter
        instance["archiveFilter"] = serder.BOOLEAN.encode(archiveFilterValue)
        from_Value = value.from_
        instance["from"] = serder.INT.encode(from_Value)
        sizeValue = value.size
        instance["size"] = serder.INT.encode(sizeValue)
        entryUidFilterValue = value.entryUidFilter
        instance["entryUidFilter"] = serder.ListSerDer(serder.STRING).encode(entryUidFilterValue)
        return instance

