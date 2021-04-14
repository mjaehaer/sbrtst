from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch , landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas

def simple_table(tables_1,tables_2,fk):
    print(fk)
    canv = canvas.Canvas("phello.pdf", pagesize=landscape(A4))    
    coords = ([50, 450], [200, 450], [50, 300], [200, 300], [50, 150], [200, 150], [350, 450], [500, 450],[350, 300], [500, 300],[350, 150], [500, 150])

    def drawTable(table, cX, cY, targetcell):
        data = [[str(table[0]) + "/" + str(table[1])]]
        y = 2
        for x in table[2:]:
            try:
                data.append([table[y]])
                y+=1
            except(IndexError):
                break
        print(targetcell)
        # print(data)
        idx = data.index([targetcell])
        print(data)
        print(idx)
        
             
        t=Table(data,int(len(data[0]))*[1.3*inch], 13)
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),colors.gray),
            # ('BACKGROUND',(0,0),(1,idx),colors.yellow),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
        
        t.wrap(0, 0)
        t.drawOn(canv, cX, cY)

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
    z = 0

    # print(toDraw)

    for x in toDraw:
        drawTable(x, coords[z][0], coords[z][1], fk[x][2]) 
        z+=1

    canv.save()
    