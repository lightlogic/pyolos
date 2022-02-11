from jinja2 import Template

class Endpoint:
    def __init__(self, prot, rootCont, apiModule, apiResource, resID=None) -> None:
        self.prot = prot
        self.root = rootCont
        self.apiModule = apiModule
        self.apiResource = apiResource
        self.resID = resID if resID is not None else ""

        endpointURL_template = Template("{{ edp.getProt() }}://{{ edp.getRoot() }}/{{ edp.getModule() }}/{{ edp.getResource() }}/{{ edp.getResID() }}")
        self.endpointURL = endpointURL_template.render(edp=self)


    def getProt(self):
        return self.prot

    def getRoot(self):
        return self.root
    
    def getModule(self):
        return self.apiModule
    
    def getResource(self):
        return self.apiResource
    
    def getResID(self):
        return self.resID

    def getRessourceURL(self):
        return self.endpointURL

