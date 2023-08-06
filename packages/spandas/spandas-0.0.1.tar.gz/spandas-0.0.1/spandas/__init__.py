
from pandas import *


def CreateExcel(file_name, copy=""):
	writer = ExcelWriter(file_name, engine="openpyxl")
	if (len(copy) > 0 ):
		import openpyxl as op
		book = op.load_workbook(copy)
		writer.book = book
	return writer
Create_Excel = CreateExcel
create_excel = CreateExcel
createexcel = CreateExcel
create_Excel = CreateExcel
createExcel = CreateExcel


def apply_style(self,DF_style):
	a = self.style.apply(lambda f: DF_style, axis=None)
	return a
DataFrame.apply_style = apply_style
Series.apply_style = apply_style


def clone(self, what=None):
	new_DF = self.copy()
	if what is not None:
		new_DF[:] = what
	return new_DF
DataFrame.clone = clone
Series.clone = clone


def apply_filter(self,mask,what,addto=False):

    prop = self.shape
    nb_column = prop[1]
    import numpy as np
    import operator as op
    
    if(isinstance(mask, (np.ndarray, np.generic))):
        mask = DataFrame(mask)
        
    if(isinstance(mask, list)):
        for col in range(nb_column):
            if addto:
                self.iloc[mask,col] = self.iloc[mask,col] + what
            else:
                self.iloc[mask,col] = what
    else:
        ss = mask.shape
        if(len(ss)==1):
            ss = ss + (0,)
        if(ss[1]>0):
            for col in range(nb_column):
                if addto:
                    self.iloc[mask.iloc[:,col].tolist(),col] = self.iloc[mask.iloc[:,col].tolist(),col] + what
                else:
                    self.iloc[mask.iloc[:,col].tolist(),col] = what 
        else:
            for col in range(nb_column):
                if addto:
                    self.iloc[mask.tolist(),col] =  (np.array(self.iloc[mask.tolist(),col].tolist()) + np.array([what]*np.sum(np.array(mask.tolist())) )).tolist()
                else:
                    self.iloc[mask.tolist(),col] = what
DataFrame.apply_filter = apply_filter
Series.apply_filter = apply_filter


try:
    DataFrame.rename2
except:    
    DataFrame.rename2 = DataFrame.rename
    def rename(self,columns={},index={}):
    	a = self.rename2(columns=columns,index=index)
    	self.columns = a.columns
    	self.index = a.index
    DataFrame.rename = rename


def add_row(self,contents):
    import numpy as np
    contents = np.array(contents)
    dimensions = contents.shape
    if (len(dimensions)==1):
        contents = np.array([ list(contents) ])
    allindex = np.array(list(self.index))
    ci = len(allindex)
    count = 0
    for j in range(len(self),len(self)+len(contents)):
        self.loc['new_row'] = list(contents[count,:])
        self.rename(index={'new_row':ci})
        count += 1
        ci += 1
DataFrame.add_row = add_row
DataFrame.add_rows = add_row


def add_column(self,contents=None,name=None):
    
    if contents is not None:
        import numpy as np
        contents = np.array(contents)
        dimensions = contents.shape
        if(len(dimensions)>0):
            if (len(dimensions)>1):
                if (dimensions[0]>1):
                    contents = contents.T
                contents = contents[0]
           
    allcolumns = self.columns   
    self.loc[:,'new_column'] = contents
    
    if name is not None:
        self.rename(columns={'new_column':name})
    else:
        self.rename(columns={'new_column':len(allcolumns)})
DataFrame.add_column = add_column

        