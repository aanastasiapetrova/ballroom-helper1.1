from fpdf import FPDF
from os.path import abspath

def get_group_registration_list(spacing=1, participants_list=[], competition_name='', group='', gn=0):
    copy_list = participants_list.copy()
    data = [["№ п/п", "№ участника", "Имя", "Клуб"]]
    data.extend(copy_list)
    columns_amount = 4

    pdf = FPDF()
    pdf.add_font('Times', '', abspath('ballroom_helper/static/fonts/times.ttf'), uni=True)
    pdf.set_font('Times', size=10)
    pdf.add_page()
    pdf.image(abspath('ballroom_helper/static/icons/icon.png'), x=5, y=5, h=30, w=30)
    pdf.cell(pdf.w-20, 10, "BALLROOM-HELPER v.1.1", border=0, align='C', fill=0)
    pdf.ln(4)
    pdf.cell(pdf.w-20, 10, competition_name, border=0, align='C', fill=0)
    pdf.ln(4)
    pdf.cell(pdf.w-20, 10, f'СПИСОК РЕГИСТРАЦИИ ГРУППЫ "{group}"', border=0, align='C')
    pdf.ln(15)
    pdf.cell(pdf.w-20, 10, f'Количество участников: {len(participants_list)}', border=0, align='L')
    pdf.ln(15)

    col_width = (pdf.w - 20) / columns_amount
    row_height = pdf.font_size*2
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing, border=1, txt=str(item), align='C')
        pdf.ln(row_height*spacing)
    
    pdf.output(abspath(f"ballroom_helper/docs/group_registration_lists/reg_list_{gn}.pdf"))