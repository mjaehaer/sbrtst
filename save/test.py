from fpdf import FPDF
 
def simple_table(tables,columns,fk,tblViews,spacing=1):
    
 
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
 
    col_width = pdf.w / 5
    row_height = pdf.font_size
    for row in tables:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)

    for row in columns:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)
    for row in fk:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)
    for row in tblViews:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)
 
    pdf.output('simple_table.pdf')
 
if __name__ == '__main__':
    simple_table()