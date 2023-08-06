import tempfile
import os
import socket
from smb.SMBConnection import SMBConnection

def copyLocally(settings, networkPath):

        #escaping special characters
        networkPath = networkPath.replace("\a","\\a").replace("\b","\\b").replace("\f","\\f").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t")

        print("Accessing: " + networkPath)
        conn = SMBConnection(settings["networkDrive"]["userID"],
                                 settings["networkDrive"]["password"],
                                 socket.gethostname(),
                                 "sharedServer",
                                 use_ntlm_v2=True,
                                 is_direct_tcp=True)


        ip = settings["networkDrive"][networkPath[:1].upper() + "_drive_ip"]
        share = settings["networkDrive"][networkPath[:1].upper() + "_drive_share"]
        location = networkPath.replace(networkPath[:3],"")
        local = settings["networkDrive"]["localPath"]

        print("retriving from ip: \\\\" + ip +  "\\" + share + "\\" + location + " to: " + local)

        conn.connect(ip, 445)
        file_obj = tempfile.NamedTemporaryFile(prefix="temp-notebook-", dir= os.getcwd())
        conn.retrieveFile(share, location, file_obj)

        if file_obj is not None:
            print("temp file created")
        file_obj.seek(0)

        filename = os.path.basename(networkPath.replace('\\',os.sep))
        print("filename: " + filename)
       
        filepath = os.path.join(os.getcwd(),local, filename)
        print("writing to " + filepath)
        file1 = open(filepath,"wb") 
        try:
            for line in file_obj:
                file1.write(line)
        finally:
            file1.close()

        localP = os.path.join(local, filename)
        print("returning local path: " + localP)
        return localP


def isSharedLocation(path):
    return path[0:2].upper() in ["S:"]