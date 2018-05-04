""" coding: utf-8
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""
import pywintypes
from win32com.client.dynamic import Dispatch
import time

class PIServer:
    def __init__(self, server_name):
        self.server_name = server_name
        self.server = self.server_connection()

    def server_connection(self):
        """
        Allows the connection to the PIserver using PI SDK via pywin32.
        :param server_name: The name of the PIserver
        :return: server object
        """
        pl = Dispatch("PISDK.PISDK")
        # Find the wished server in the list of registered servers:
        registered_servers = list()
        for server in pl.Servers:
            if self.server_name == "default":
                if server.Name == pl.Servers.DefaultServer.Name:
                    # print("{0}\t:: Connected ::".format(server.Name))
                    return server
            else:
                if server.Name == self.server_name:
                    # print("{0}\t:: Connected ::".format(server.Name))
                    return server
            registered_servers.append(server.Name)
        print("No existe servidor registrado con el nombre: {0} \n"
              "Los servidores registrados son: {1}".format(self.server_name, registered_servers))
        return None

    def get_tag_object(self, tag_name):
        """
        if a tag_name exists in the server then returns a tag object
        otherwise None
        :param tag_name:     name of the PI Tag
        :return:             tag object
        """

        try:
            tag=self.server.PIPoints(tag_name)
            return tag
        except pywintypes.com_error:
            print("[get_tag_object] [{0}] does not exist".format(tag_name))
            return None

    def get_tag_snapshot(self, tag_name):

        tag = self.get_tag_object(tag_name)
        if tag is None: return Snapshot(0, -1)
        else:
            return Snapshot(
                tag.Data.Snapshot.TimeStamp.UTCseconds,
                tag.Data.Snapshot.Value
            )


class Snapshot():
    """
    This class represent a snapshot of a PI Tag
    """
    def __init__(self, timestamp, value):
        """
        Snapshot of a PI Tag
        :param timestamp:   timestamp in time.localtime (UTCseconds)
        :param value:       value of the tag
        """
        self.timestamp = time.localtime(timestamp)
        self.value = value