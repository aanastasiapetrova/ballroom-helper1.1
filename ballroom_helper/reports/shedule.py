from os.path import abspath

from fpdf import FPDF


def get_shedule(spacing=1, shedule_list=[], competition_name='', competition_id=0, part_id=0):
    copy_list = shedule_list.copy()
    data = [["№ п/п", "Группа", "Танцы", "Участников", "Заходов", "Длит-ть"]]
    data.extend(copy_list)
    columns_amount = 5

    pdf = FPDF(orientation="landscape")
    pdf.add_font('Times', '', abspath('ballroom_helper/static/fonts/times.ttf'), uni=True)
    pdf.set_font('Times', size=15)
    pdf.add_page()
    pdf.image(abspath('ballroom_helper/static/icons/icon.png'), x=5, y=5, h=30, w=30)
    pdf.cell(pdf.w-20, 10, "BALLROOM-HELPER v.1.1", border=0, align='C', fill=0)
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, competition_name, border=0, align='C', fill=0)
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f"РАСПИСАНИЕ ОТДЕЛЕНИЯ № {part_id}", border=0, align='C')
    pdf.ln(15)

    #col_width = (pdf.w - 20) / columns_amount
    col_width1 = (pdf.w - 20) * 0.4
    col_width2 = (pdf.w - 20) * 0.1
    col_width3 = (pdf.w - 20) * 0.2
    row_height = pdf.font_size*2
    counter = 0
    for row in data:
        counter = 0
        for item in row:
            if counter == 1:
                pdf.cell(col_width1, row_height*spacing, border=1, txt=str(item), align='C')
            elif counter == 2:
                pdf.cell(col_width3, row_height*spacing, border=1, txt=str(item), align='C')
            else:
                pdf.cell(col_width2, row_height*spacing, border=1, txt=str(item), align='C')
            counter += 1
        pdf.ln(row_height*spacing)
    
    pdf.output(abspath(f"ballroom_helper/docs/shedules/shedule_{part_id}.pdf"))