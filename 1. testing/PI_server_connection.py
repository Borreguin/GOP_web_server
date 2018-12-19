from win32com.client.dynamic import Dispatch
import win32com.client
import time


""" Access to PI SDK via pywin32 """
def connect_to_PIserver_by_SDK():
    PL = Dispatch("PISDK.PISDK")
    print("PISDK Version:", PL.PISDKVersion)
    print("Known Server List")
    print("-----------------")

    for server in PL.Servers:
        if server.Name == PL.Servers.DefaultServer.Name:
            print("{0}\t:: DEFAULT::".format(server.Name))
        else:
            print(server.Name)
        tag = server.PIPoints("sinusoid")
        # or tag = server.PIPoints.Item("sinusoid")
        print("\t", tag.PointAttributes("tag").Value)
        print("\t", tag.Data.Snapshot.Value)
        timestamp = time.localtime(tag.Data.Snapshot.TimeStamp.UTCseconds)
        print("\t", time.asctime(timestamp))


""" Using the COM extension for CPython, we can also use PI OLEDB (COM technology) """
def connect_PIserver_by_OLEDB():
    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = "Provider=PIOLEDB.1;Data Source=UIOSEDE-COMBAP;Integrated Security=SSPI;Persist Security Info=False"
    conn.Open(DSN)

    recordset = win32com.client.Dispatch(r'ADODB.Recordset')
    recordset.Cursorlocation = 3
    recordset.Open("select tag, value from pisnapshot", conn)

    if recordset.RecordCount > 0:
        print("You have a total of {0} tags, and these are their values\n".format(recordset.RecordCount))
        print("Tag, Snapshot Value")
        print("---------------------\n")
        while not recordset.EOF:
            source = {field.Name: field.value for field in recordset.Fields}
            print("{tag}, {value}".format(**source))
            recordset.MoveNext()
    else:
        print("There are no tags")
    conn.Close()


connect_to_PIserver_by_SDK()
# connect_PIserver_by_OLEDB()
