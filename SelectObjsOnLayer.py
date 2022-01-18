import rhinoscriptsyntax as rs


def SelectObjsOnLayer():

    try:

        obj = rs.GetObject(message="Select obj to select all on layer", filter=0,
                           preselect=True, select=False, custom_filter=None, subobjects=False)
        rs.EnableRedraw(False)
        layer = rs.ObjectLayer(obj)
        objs = rs.ObjectsByLayer(layer, select=True)
        rs.EnableRedraw(True)

    except:
        rs.EnableRedraw(True)
        print("Failed to execute")
        return


if __name__ == "__main__":
    SelectObjsOnLayer()
