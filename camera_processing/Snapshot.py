# Handle snapshot and get the data for the website


from ImageProcessing import ImageProcessing
class Snapshot:
    currentSnapshot = None 
    def __init__(self):
        self.objectInfo = {} 

    def detectObject(self):
        self.objectInfo = {}
        if(Snapshot.currentSnapshot is not None):
            self.objectInfo = ImageProcessing.getObjectInfo(Snapshot.currentSnapshot) 
    
    def getPosition(self,selectedObject,selectedContainer):
        data = [] 
        if  selectedObject in self.objectInfo:
            for value in self.objectInfo[selectedObject]:
                data.append(value)
            data.append(selectedContainer)
        return data

    def listObject(self):
        if (bool(self.objectInfo)):
            objectName = []
            for key in self.objectInfo:
                objectName.append(key) 
            return objectName
        return []
    