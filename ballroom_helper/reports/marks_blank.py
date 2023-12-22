from os.path import abspath

from fpdf import FPDF

def get_marks_list(spacing=1, numbers_list=[], dances_list=[], competition_name='', group='', judge=[], gn=0):
    numbers_list_copy = numbers_list.copy()
    data = [["№ участника"]]
    for dance in dances_list:
        data[0].append(dance)
    for i in range(len(numbers_list_copy)):
        numbers_list_copy[i] = [numbers_list_copy[i]]
        for _ in range(len(data[0])-1):
            numbers_list_copy[i].append('')
    data.extend(numbers_list_copy)
    columns_amount = len(data[0])

    pdf = FPDF(orientation="landscape")
    pdf.add_font('Times', '', abspath('ballroom_helper/static/fonts/times.ttf'), uni=True)
    pdf.set_font('Times', size=15)
    pdf.add_page()
    pdf.image(abspath('ballroom_helper/static/icons/icon.png'), x=5, y=5, h=30, w=30)
    pdf.cell(pdf.w-20, 10, "BALLROOM-HELPER v.1.1", border=0, align='C', fill=0)
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, competition_name, border=0, align='C', fill=0)
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f'БЛАНК ДЛЯ ВЫСТАВЛЕНИЯ ОЦЕНОК СУДЬИ: "{judge[0]}"', border=0, align='C')
    pdf.ln(20)
    pdf.cell(pdf.w-20, 10, f'Группа: {group}', border=0, align='L')
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f'Идентификатор: {judge[1]}', border=0, align='L')
    pdf.ln(20)

    col_width = (pdf.w - 20) / columns_amount
    row_height = pdf.font_size*2
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing, border=1, txt=str(item), align='C')
        pdf.ln(row_height*spacing)
    
    pdf.output(abspath(f"ballroom_helper/docs/marks_blanks/{gn}/{judge[1]}.pdf"))