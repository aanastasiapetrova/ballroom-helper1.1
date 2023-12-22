from os.path import abspath

from fpdf import FPDF


def get_number(spacing, number, athlete, club, competition, group, gn):
    pdf = FPDF(orientation="landscape")
    pdf.add_font('Times', '', abspath('ballroom_helper/static/fonts/times.ttf'), uni=True)
    pdf.set_font('Times', size=20)
    pdf.add_page()
    pdf.image(abspath('ballroom_helper/static/icons/icon.png'), x=5, y=5, h=30, w=30)
    pdf.cell(pdf.w-20, 10, f'"{competition}"', border=0, align='C')
    pdf.ln(75)
    pdf.set_font('Times', size=300)
    pdf.cell(pdf.w-20, 10, f"{number}", border=0, align='C')
    pdf.ln(75)
    pdf.set_font('Times', size=18)
    pdf.cell(pdf.w-20, 10, f"{athlete}", border=0, align='C')
    pdf.ln(7)
    pdf.cell(pdf.w-20, 10, f"{group}", border=0, align='C')
    pdf.ln(7)
    pdf.cell(pdf.w-20, 10, f"{club}", border=0, align='C')

    pdf.output(abspath(f"ballroom_helper/docs/numbers/number_{gn}_{number}.pdf"))