# -*- coding: utf-8 -*-
import re
import socket
import ssl
from random import shuffle
from contextlib import closing

class DatabaseAbstract:
    _buffer = None
    __ip4RangePattern = re.compile(r'^(\d+\.\d+\.\d+)\.(\d+)\.\.(\d+)')


    def __init__(self, connectionString, user, password, autocommit = False):
        self._buffer = [] #initialize buffer, don't forget in your inherited method!
        raise NotImplementedError()


    def ipFromConnectionString(self, connectionString):
        """chooses an usable IP address from the connection string
            
            Note:
                This method chooses an IP address from the connection string and checks if 
                the port on the given address is open. If the port is closed the next address
                will be checked.

            Args:
                connectionString:   an Exasol database connection string

            Returns:
                Tuple (ip, port) with valid address or None if no ip is usable

        """
        connectionSplit = connectionString.split(':')
        ipString = connectionSplit[0]
        port = int(connectionSplit[1])

        ipItems = []
        for ipRange in ipString.split(','):
            if not '..' in ipRange: #not a range, just an single IP
                ipItems.append(ipRange)
            else:
                match = self.__ip4RangePattern.match(ipRange)
                for i in range(int(match.group(2)), int(match.group(3)) + 1):
                    ipItems.append('%s.%i' % (match.group(1), i))
        shuffle(ipItems)
        for ip in ipItems:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                if s.connect_ex((ip, port)) == 0:
                    return (ip, port)
        return None


    def escapeIdent(self, text):
        """Escapes SQL identfiers

            Args:
                text:       SQL identifier that needs to be escaped

            Returns:
                The provided identifier, escaped
        """
        return '"' + text.replace('"', '""') + '"'


    def escapeString(self, text):
        """Escapes SQL strings

            Args:
                text:       SQL string that needs to be escaped

            Returns:
                The provided string, escaped
        """
        return "'" + text.replace("'", "''") + "'"


    def getBuffer(self):
        """Creates a string containing the current SQL buffer
            
            Args:
                None

            Returns:
                A string containing all SQL commands on the SQL buffer
        """
        return '\n'.join(self._buffer)


    def cleanBuffer(self):
        """Purges the SQL buffer content
            
            Args:
                None

            Returns:
                None
        """
        self._buffer = [] 


    def addToBuffer(self, sqlText):
        """Appends a SQL statement to the internal SQL buffer

            Args:
                sqlText:    The statement which will be appended

            Returns:
                None
        """
        self._buffer.append(sqlText.strip())


    def close(self):
        raise NotImplementedError()

    def execute(self, sqlText, *args):
        raise NotImplementedError()

    def executeBuffer(self):
        raise NotImplementedError()
