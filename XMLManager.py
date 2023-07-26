import xml.etree.ElementTree as ET

class XMLTool():
    def __init__(self, xml_path: str = "example.xml"):
        self.xml_path = xml_path
        
        try:
            with open(xml_path) as f :
                self.tree = ET.parse(f)
                self.root = self.tree.getroot()
        except FileNotFoundError:
            self.__create_xml(xml_path)

    #xml 파일 저장
    def __create_xml(self, xml_path = "example.xml"):
        print("Create XML File")
        self.root = ET.Element("root")
        self.tree = ET.ElementTree(self.root)
        self.xml_path = xml_path
        
        self.save_file()

    #xml 출력 정리
    def __pretty_print(self, current, parent=None, index=-1, depth=0):

        for i, node in enumerate(current):
            self.__pretty_print(current= node, parent=current,index= i, depth= depth + 1)
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('\t' * depth)
            else:
                parent[index - 1].tail = '\n' + ('\t' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('\t' * (depth - 1))

    #xml 파일 저장         
    def save_file(self):
        self.__pretty_print(self.root)
        with open(self.xml_path, "wb") as file:
            self.tree.write(file, encoding='utf-8', xml_declaration=True)

    
    #요소들 변경
    def modify_elements(self, before_element : str, after_element : str, parent :str = "."): 
        for child in self.tree.findall(parent + "/" + before_element):
            child.tag = after_element

        self.save_file()
    
    #요소 변경
    def modify_element(self, before_element : str, after_element : str, parent :str = ".", index: int = 0): 
        i = 0
        for child in self.tree.findall(parent + "/" + before_element):
            if index == i:
                child.tag = after_element
            i += 1

        self.save_file()

    #속성들 변경
    def modify_attribs(self, element: str, before_attribs : str, after_attribs : str, parent :str = "."): 
        for child in self.tree.findall(parent + "/" + element):
            value = child.attrib[before_attribs]
            child.attrib.pop(before_attribs, None)
            child.set(after_attribs, value)
        
        self.save_file()

    #속성 변경
    def modify_attrib(self, element: str, before_attribs : str, after_attribs : str, parent :str = "." , index = 0): 
        i = 0
        for child in self.tree.findall(parent + "/" + element):
            if before_attribs in child.attrib.keys():
                if index == i:
                    value = child.attrib[before_attribs]
                    child.attrib.pop(before_attribs, None)
                    child.set(after_attribs, value)
                    break
                i += 1
        self.save_file()
    
    #요소들 추가
    def add_elements(self, element, parent :str = None):
        if parent:
            parent_tag = parent.split("/")[-1]
            path = parent.replace(parent_tag, '')
            for chlid in self.tree.findall(path):
                if parent_tag == chlid.tag:
                    ET.SubElement(chlid, element)
        else:
            self.root.append(ET.Element(element))

        self.save_file()
    
    #요소 추가
    def add_element(self, element, parent :str = None, index: int = 0):        
        if parent:
            i = 0
            parent_tag = parent.split("/")[-1]
            path = parent.replace(parent_tag, '')
            for chlid in self.tree.findall(path):
                if parent_tag == chlid.tag:
                    if index == i:
                        ET.SubElement(chlid, element)
                        break
                    i += 1
        else:
            self.root.append(ET.Element(element))

        self.save_file()

    #속성들 추가
    def add_attribs(self, element, attrib, value, parent :str = "."):
        for child in self.tree.findall(parent + "/" + element):
            
            child.set(attrib, value)

        self.save_file()

    #속성 추가
    def add_attrib(self, element, attrib, value, parent :str = ".", index: int = 0):
        i = 0
        for child in self.tree.findall(parent + "/" + element):
            print(child)
            if attrib not in child.attrib.keys():
                if index == i:
                    child.set(attrib, value)
                    break
                i += 1   

        self.save_file()

    #요소들 삭제
    def remove_elements(self, element, parent :str = "."):
        for child in self.tree.findall(parent + "/" + element):
            self.root.remove(child)
        
        self.save_file()
    
    #요소 삭제
    def remove_element(self, element, parent :str = ".", index: int = 0):
        i = 0
        parent_et = self.tree.find(parent)
        for child in self.tree.findall(parent + "/"+ element):
            
            if child.tag == element:
                if index == i:
                    parent_et.remove(child)
                    break
                i += 1   
        self.save_file()

    #속성들 삭제
    def remove_attribs(self, element, attrib, parent :str = "."):
        for child in self.tree.findall(parent + "/" + element):
            child.attrib.pop(attrib , None)
    
        self.save_file()

    #속성 삭제
    def remove_attrib(self, element, attrib, parent :str = ".", index : int = 0):
        i=0
        for child in self.tree.findall(parent + "/" + element):
            
            if attrib in child.attrib.keys():
                
                if index == i:
                    child.attrib.pop(attrib, None)
                    break
                i += 1

        self.save_file()

if __name__ == "__main__":
    xml_tool = XMLTool("test.xml")
    #xml_tool.add_elements("node", "library/book")
    #xml_tool.add_element("node", "library/book")
    #xml_tool.add_attribs("book", "tr", "1000.0")
    #xml_tool.add_attrib("book", "tr", "1000.0", "library", 2)
    #xml_tool.remove_elements("node")
    #xml_tool.remove_element("node", "library/book", 1)
    #xml_tool.remove_attribs("book", "author", "library")
    #xml_tool.remove_attrib("book", "author", "library", 1)
    #xml_tool.modify_element("node", "ndn", parent="library/book",index=1)
    #xml_tool.modify_elements("ndn", "node", parent="library/book")
    #xml_tool.modify_attribs("node", "price", "pp")
    #xml_tool.modify_attrib("node", "price", "pp", "library/book", index= 2)