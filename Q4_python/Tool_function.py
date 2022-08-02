# %% ==========================================================================
#                                  Tool functions 
# =============================================================================
import os     
import sys



# ------------------------------------------------------------------------------
#                              intersection function  
# ------------------------------------------------------------------------------
def intersection(input, overlay, ouput):
    """
    realize an intersection between two file 
    """
    # parameters 
    params = {
     'INPUT': input,
     'OVERLAY': overlay,
     'OUTPUT': ouput}
     
    # outputdict : {'OUPUT': file path'}     
    outputdict = processing.run('qgis:intersection', params)
    return(outputdict['OUTPUT'])
    
    
# ------------------------------------------------------------------------------
#                              centroids  function  
# ------------------------------------------------------------------------------
def centroids(input, all_part, output):
    """
    calculate the centroids
    """
    # parameters 
    params ={'INPUT':input ,
             'ALL_PARTS':all_part,
             'OUTPUT': output}
    
    # calculate the centroids 
    outputdict = processing.run("native:centroids",params )
    
    return(outputdict['OUTPUT'])
    

# ------------------------------------------------------------------------------
#                      function to add new field in a vector 
# ------------------------------------------------------------------------------
def add_field(layer, name_field, expression) :
    """
    add a field in the attribut table based on a math expression 
    
    Parameters :
    ---------------
    layer : string
        name of the mlayer in which you made the computation
        
    name_field : string
        name of the column in the attribut table
        
    expression: string     
        math epression you want to calculate 
    """
    # test if the area is already a field
    field_names = [field.name() for field in layer.fields()]

    if name_field not in field_names : 
        pv = layer.dataProvider()
        # add a new field in the vector 
        pv.addAttributes([QgsField(name_field, QVariant.Double)])
        # update the layer 
        layer.updateFields()

    # expression desired in the new field
    expression = QgsExpression(expression)

    # specified the layer where to put the expression
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

    # perform the calculation 
    with edit(layer):
        for f in layer.getFeatures():
            context.setFeature(f)
            f[name_field] = expression.evaluate(context)
            layer.updateFeature(f)

    # update the layer 
    layer.updateFields()
    

# ------------------------------------------------------------------------------
#              function to test if a polygone isn't exceed a certain value
# ------------------------------------------------------------------------------
def is_area_valid(layer, max_area) :
    """

    measur the area of a layer and checked if the value isn't exceed max_area
    
    Parameters :
    ---------------
    layer : string
        name of the layer for which you want the test
        
    max_area : number
        the area that the layer cannot exceed

    """
    
    for f in layer.getFeatures():
        geom = f.geometry()
        area = geom.area()/10000
        consortia = f.attribute(0)
        
        if area > max_area :
            print('===============================')
            print('the area of the consortia : ' + consortia )
            raise(ValueError( 'exceed the authorized area : ' + str(max_area)   + '. Please reduce its area before relaunching the programm'))

 
       
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    