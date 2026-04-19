class Classes:
    def __init__(self,id,name,teacherid):
        if id is None:
            self.id = 0
        else:
            self.id = id
        self.name = name
        self.teacherid = teacherid 
    
    @staticmethod
    def CreateClasses(obj):
        list=[]
        for i in obj:
            list.append(Classes(i[0],i[1],i[2]))
        return list
        
