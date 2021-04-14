from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch , landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas

def simple_table(tables_1,tables_2,fk, tblViews):
    # print(fk)
    canv = canvas.Canvas("phello.pdf", pagesize=landscape(A4))    
    coords = ([50, 450], [200, 450], [50, 300], [200, 300], [50, 150], [200, 150], [350, 450], [500, 450],[350, 300], [500, 300],[350, 150], [500, 150])

    def drawTable(table, cX, cY, targetcell, tblViews):
        data = [[str(table[0]) + "/" + str(table[1])]]
        y = 2
        for x in table[2:]:
            try:
                data.append([table[y]])
                y+=1
            except(IndexError):
                break
        # print(data)
        idx = data.index([targetcell])             
        t=Table(data,int(len(data[0]))*[1.3*inch], 13)
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),colors.gray),
            ('BACKGROUND',(0,idx),(0,idx),colors.yellow),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,idx),(0,idx),colors.yellow)
            ]))
        t.wrap(0, 0)
        t.drawOn(canv, cX, cY)
        canv.setFont("Helvetica", 8)
        for x in tblViews:
            if table[0] == x[2] and table[1] == x[3]:
                canv.drawString(cX , cY - 15, "Used in view " + str(x[0]) + "/" + str(x[1]))

    def getTable(arg1,arg2):
        for x in tables_1:
            if arg1 == x[0] and arg2 == x[1]:
                return x
    def getTable2(arg1,arg2):
        for x in tables_2:
            if arg1 == x[0] and arg2 == x[1]:
                return x

    toDraw = []       
    for i in fk:
        toDraw.append(getTable(i[0],i[1]))
        toDraw.append(getTable2(i[3],i[4]))
    
    print(tblViews)
    targetCells = []
    g = 0
    for x in fk:
        targetCells.append(fk[g][2])
        targetCells.append(fk[g][5]) 
        g+=1
        
    # print(targetCells)
    z = 0 
    for x in toDraw:
        print(x)
        drawTable(x, coords[z][0], coords[z][1], targetCells[z], tblViews) 
        z+=1

    canv.save()
    