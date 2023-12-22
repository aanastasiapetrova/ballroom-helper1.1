from os.path import abspath

from fpdf import FPDF


def get_convert(spacing, number, athlete, club, competition, group, gn):
    pdf = FPDF(orientation="landscape")
    pdf.add_font('Times', '', abspath('ballroom_helper/static/fonts/times.ttf'), uni=True)
    pdf.set_font('Times', size=20)
    pdf.add_page()
    pdf.image(abspath('ballroom_helper/static/icons/icon.png'), x=45, y=-10, h=180, w=200)
    pdf.ln(150)
    pdf.cell(pdf.w-20, 10, f'"{competition}"', border=0, align='C')
    pdf.ln(10)
    pdf.set_font('Times', size=18)
    pdf.cell(pdf.w-20, 10, f"{athlete}", border=0, align='C')
    pdf.ln(7)
    pdf.cell(pdf.w-20, 10, f"{club}", border=0, align='C')

    pdf.output(abspath(f"ballroom_helper/docs/converts/convert_{gn}_{number}.pdf"))