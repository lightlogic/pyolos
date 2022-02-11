import json
class DlcmDeposit:
    def __init__(self, access_lvl, data_sensitivity, title, description, org_unit_id, pubdate) -> None:
        self.access = access_lvl
        self.dataSensitivity = data_sensitivity
        self.title = title
        self.description = description
        self.organizationalUnitId = org_unit_id
        self.publicationDate = pubdate
        ## json object with details according to
        ## https://sandbox.dlcm.ch/administration/docs/DLCM-APIs.html#preingest-deposits-details
        self.details = None

    def setDetails(self, creation_response):
        self.details = creation_response
        return 1
    
    def getDetails(self):
        return self.details
        
    # def getAccessLvl(self):
    #     return self.access
    
    # def getDataSensitivity(self):
    #     return self.dataSensitivity
    
    # def getTitle(self):
    #     return self.title
    
    # def getDescription(self):
    #     return self.description
    
    # def getOrgUnitId(self):
    #     return self.organizationalUnitId
    
    # def getPublicationDate(self):
    #     return self.publicationDate