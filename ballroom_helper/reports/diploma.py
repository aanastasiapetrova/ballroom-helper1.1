from os.path import abspath

from fpdf import FPDF

def get_diploma(spacing=1, participant_name='', participant_id='', competition_name='', result=''):

    pdf = FPDF()
    pdf.add_font('Times', '', abspath('ballroom_helper/static/fonts/times.ttf'), uni=True)
    pdf.set_font('Times', size=25)
    pdf.add_page()
    pdf.ln(100)
    pdf.cell(pdf.w-20, 10, f'НАГРАЖДАЕТСЯ', border=0, align='C')
    pdf.ln(20)
    pdf.set_font('Times', size=20)
    pdf.cell(pdf.w-20, 10, f'{participant_name}', border=0, align='C')
    pdf.ln(2)
    pdf.cell(pdf.w-20, 10, f'__________________________________', border=0, align='C')
    pdf.ln(20)
    pdf.cell(pdf.w-20, 10, f'за участие в промежуточной аттестации', border=0, align='C')
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f'школы танцев "Олимп"', border=0, align='C')
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f'с результатом: {str(result)} балла', border=0, align='C')
    pdf.set_font('Times', style='', size=10)
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f'(максимальный балл: 3.0.)', border=0, align='C')
    pdf.ln(40)
    pdf.set_font('Times', style='', size=15)
    pdf.cell(pdf.w-20, 10, f'Руководитель школы танцев "Олимп"        ', border=0, align='R')
    pdf.ln(8)
    pdf.cell(pdf.w-20, 10, f'Меньщикова А.М. _________________        ', border=0, align='R')
    pdf.ln(30)
    pdf.cell(pdf.w-10, 10, f'Ульяновск', border=0, align='C')
    pdf.ln(8)
    pdf.cell(pdf.w-10, 10, f'24.12.2023', border=0, align='C')

    pdf.output(abspath(f"ballroom_helper/docs/diplomas/diploma_{participant_id}.pdf"))