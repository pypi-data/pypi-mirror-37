import sys, Ice
import Demo
import DBM

PER_FILE_DATA_LENGTH = 10 * 1024 * 1024
# Modules:

class Client:
    def __init__(self, ice_config, db_config):
        communicator = Ice.initialize(sys.argv)
        base = communicator.stringToProxy(db_config)
        dfs = communicator.stringToProxy(ice_config)
        self.dbm = DBM.DatabaseManagerPrx.checkedCast(base)
        self.FDFS = Demo.FDFSPrx.checkedCast(dfs)

        if not self.dbm:
            raise RuntimeError("dbm Invalid proxy")

        if not self.FDFS:
            raise RuntimeError("fdfs Invalid proxy")

    def upload(self, fullname, filename):
        if self.FDFS == None:
            return None

        fid = ""

        try:
            with open(fullname) as f:
                data = f.read()

                if len(bytes(data.encode("utf8"))) <= PER_FILE_DATA_LENGTH:
                    fid = self.FDFS.upload(bytes(data.encode("utf8")), len(bytes(data.encode("utf8"))), filename.replace(" ", ""))
                    return fid

                else:
                    index = 0
                    datastr = data[index:index + PER_FILE_DATA_LENGTH]
                    fid = self.FDFS.upload(bytes(datastr.encode("utf8")), len(bytes(datastr.encode("utf8"))), filename.replace(" ", ""))
                    index = index + PER_FILE_DATA_LENGTH

                    while index < len(data):
                        datastr = data[index: index + PER_FILE_DATA_LENGTH]
                        self.FDFS.append(fid, bytes(datastr.encode("utf8")), len(bytes(datastr.encode("utf8"))))
                        index = index + PER_FILE_DATA_LENGTH

                    return fid
                

        except Exception as e:
            print(repr(e))
            return None



    def download(self, fid):
        if self.FDFS == None or type(fid) is not str:
            return None

        try:
            size = self.FDFS.size(fid)

            leftSize = size
            bufferSize = PER_FILE_DATA_LENGTH
            offset = 0
            data = ""
            while leftSize > 0:
                if PER_FILE_DATA_LENGTH > leftSize:
                    bufferSize = leftSize

                res = self.FDFS.download(fid, offset, bufferSize)
                res = str(res, "utf-8")
                data = data + res
                offset = offset + PER_FILE_DATA_LENGTH
                leftSize = leftSize - bufferSize

            return data

        except Exception as e:
            print(repr(e))
            return None

    def delete(self, fid):
        if self.FDFS == None or type(fid) is not str:
            return None

        try:
            self.FDFS.delete(fid)
            return True
        except Exception as e:
            print(repr(e))
            return None
        

    def size(self, fid):
        if self.FDFS == None or type(fid) is not str:
            return None

        try:
            res = self.FDFS.size(fid)
            return res
        except Exception as e:
            print(repr(e))
            return None
            

    def saveFid(self, exchange, symbol, contractType, dataType, fid, dateTime):
        if self.dbm == None:
            return None

        try:
            res = self.dbm.saveFid(exchange, symbol, contractType, dataType, fid, dateTime, None);
            return res;
        except Exception as e:
            print(repr(e))
            return None
    
    def queryFid(self, exchange, symbol, contractType, dataType, startDate, endDate):
        if self.dbm == None:
            return None

        try:
            res = self.dbm.queryFid(exchange, symbol, contractType, dataType, startDate, endDate);
            return res;
        except Exception as e:
            print(repr(e))
            return None

