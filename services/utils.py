import os
from django.core.exceptions import ValidationError
from docx import Document
from datetime import datetime
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt
import subprocess


def validate_file_type_and_size(value):
    """
    Validates the file type and size of uploaded files.

    Allowed types: PDF, Word, Excel
    Maximum size: 5MB
    """
    allowed_extensions = ['.pdf', '.mp4', '.mov', '.avi', '.mkv', '.flv', '.ppt', '.pptx']
    max_file_size = 50 * 1024 * 1024  # 50 MB

    # Get file extension
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed types are: {', '.join(allowed_extensions)}")

    # Check file size
    if value.size > max_file_size:
        raise ValidationError(f"The file size exceeds the 50MB limit.")


def center_cell_text(cell, left_indent=4.0, right_indent=4.0):
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        paragraph.paragraph_format.left_indent = Pt(left_indent)
        paragraph.paragraph_format.right_indent = Pt(right_indent)

    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    vAlign = OxmlElement('w:vAlign')
    vAlign.set(qn('w:val'), 'center')
    tcPr.append(vAlign)


def center_left_paragraph(paragraph, left_indent=4.0, right_indent=4.0):
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    paragraph.paragraph_format.left_indent = Pt(left_indent)
    paragraph.paragraph_format.right_indent = Pt(right_indent)


def file_one_create(serialized_data):
    file_path = "/home/otabek/Desktop/1-variant uchun shakl.docx"
    document = Document(file_path)

    paragraph1 = document.paragraphs[0]
    paragraph2 = document.paragraphs[1]

    paragraph1.text = f'{serialized_data.get('organization_director_position')} {serialized_data.get('organization_director_full_name')}гa'
    paragraph2.text = f'{serialized_data.get('employee_position')} {serialized_data.get('employee_full_name')}дан\n'

    run1 = paragraph1.runs[0]
    run2 = paragraph2.runs[0]

    run1.font.size = Pt(14)
    run2.font.size = Pt(14)

    center_left_paragraph(paragraph=paragraph1, left_indent=300, right_indent=2)
    center_left_paragraph(paragraph=paragraph2, left_indent=300, right_indent=2)

    table1 = document.tables[0]
    table2 = document.tables[1]
    table3 = document.tables[2]
    table4 = document.tables[3]
    table5 = document.tables[4]

    table1.cell(0, 2).text = (serialized_data.get('employee_passport_series') or ''
                              + '\n' + serialized_data.get('employee_passport_taken_date'))
    table1.cell(1, 2).text = serialized_data.get('employee_passport_number') or ''
    table2.cell(1, 2).text = serialized_data.get('related_persons_full_name') or ''
    table2.cell(2, 2).text = (serialized_data.get('related_persons_passport_series') or ''
                              + '\n' + serialized_data.get('related_persons_passport_taken_date') or '')
    table2.cell(5, 2).text = serialized_data.get('employee_legal_entity_name') or ''
    table2.cell(3, 2).text = serialized_data.get('related_persons_passport_number') or ''
    table2.cell(6, 2).text = serialized_data.get('employee_stir_number') or ''
    table2.cell(8, 2).text = serialized_data.get('related_persons_legal_entity_name') or ''
    table2.cell(9, 2).text = serialized_data.get('related_persons_stir_number') or ''
    table3.cell(0, 2).text = serialized_data.get('description') or ''
    table4.cell(0, 0).text = serialized_data.get('employee_position') or ''
    table4.cell(0, 1).text = f"________________________\n Шахсий имзо ёки электрон рақамли имзоси"
    table4.cell(0,
                2).text = f"{serialized_data.get('employee_full_name') or ''} \n {serialized_data.get('filled_date') or ''}"
    table5.cell(0, 0).text = serialized_data.get('organization_director_position') or ''
    table5.cell(0, 1).text = f"\n_______________________\n Шахсий имзо ёки электрон рақамли имзоси"
    table5.cell(0, 2).text = (f"{serialized_data.get('organization_director_full_name') or ''}"
                              f" \n \n _____________________\nТўлдирилган сана")

    center_cell_text(table1.cell(0, 2))
    center_cell_text(table1.cell(1, 2))
    center_cell_text(table2.cell(1, 2))
    center_cell_text(table2.cell(2, 2))
    center_cell_text(table2.cell(3, 2))
    center_cell_text(table2.cell(5, 2))
    center_cell_text(table2.cell(6, 2))
    center_cell_text(table2.cell(8, 2))
    center_cell_text(table2.cell(9, 2))
    center_cell_text(table3.cell(0, 2))
    center_cell_text(table4.cell(0, 0))
    center_cell_text(table4.cell(0, 1))
    center_cell_text(table4.cell(0, 2))
    center_cell_text(table5.cell(0, 0))
    center_cell_text(table5.cell(0, 1))
    center_cell_text(table5.cell(0, 2))

    docx_output_path = f"/home/otabek/Desktop/file1_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.docx"
    document.save(docx_output_path)
    pdf_output_path = docx_output_path.replace('.docx', '.pdf')
    output_dir = '/'.join(pdf_output_path.split('/')[:-1])
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, docx_output_path],
                   check=True)
    return serialized_data


def file_two_create(serialized_data):
    file_path = '/home/otabek/Desktop/2-variant uchun shakl.docx'
    document = Document(file_path)

    paragraph0 = document.paragraphs[0]
    paragraph1 = document.paragraphs[1]
    paragraph2 = document.paragraphs[2]

    paragraph0.text = "Ходимнинг эҳтимолий манфаатлар тўқнашуви тўғрисидаги"
    run0 = paragraph0.runs[0]
    run0.font.size = Pt(14)
    paragraph0.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph0.runs[0].bold = True

    paragraph1.text = "ДЕКЛАРАЦИЯ"
    run1 = paragraph1.runs[0]
    run1.font.size = Pt(14)
    paragraph1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph1.runs[0].bold = True

    paragraph2.text = f"Мен, {serialized_data.get('employee_full_name')} ушбу тўлдираётган декларацияда ўзим ва менга алоқадор шахсларнинг эҳтимолий манфаатлар тўқнашувига оид қуйидаги маълумотларни ошкор қиламан:"
    run2 = paragraph2.runs[0]
    run2.font.size = Pt(12)

    table1 = document.tables[0]
    table2 = document.tables[1]
    table3 = document.tables[2]

    table1.cell(0, 2).text = (serialized_data.get('employee_passport_series') or '' +
                              '\n' + serialized_data.get('employee_passport_taken_date') or '')
    table1.cell(1, 2).text = serialized_data.get('employee_passport_number') or ''
    table2.cell(1, 2).text = serialized_data.get('related_persons_full_name') or ''
    table2.cell(2, 2).text = (serialized_data.get('related_persons_passport_series') or '' +
                              '\n' + serialized_data.get('related_persons_passport_taken_date') or '')
    table2.cell(3, 2).text = serialized_data.get('related_persons_passport_number') or ''
    table2.cell(5, 2).text = serialized_data.get('employee_legal_entity_name') or ''
    table2.cell(6, 2).text = serialized_data.get('employee_stir_number') or ''
    table2.cell(8, 2).text = serialized_data.get('related_persons_legal_entity_name') or ''
    table2.cell(9, 2).text = serialized_data.get('related_persons_stir_number') or ''
    table3.cell(0, 0).text = serialized_data.get('employee_position') or ''
    table3.cell(0, 1).text = f"________________________\n Шахсий имзо ёки электрон рақамли имзоси"
    table3.cell(0,
                2).text = f"{serialized_data.get('employee_full_name') or ''} \n {serialized_data.get('filled_date') or ''}"

    center_cell_text(table1.cell(0, 2))
    center_cell_text(table1.cell(1, 2))
    center_cell_text(table2.cell(1, 2))
    center_cell_text(table2.cell(2, 2))
    center_cell_text(table2.cell(3, 2))
    center_cell_text(table2.cell(5, 2))
    center_cell_text(table2.cell(6, 2))
    center_cell_text(table2.cell(8, 2))
    center_cell_text(table2.cell(9, 2))
    center_cell_text(table3.cell(0, 0))
    center_cell_text(table3.cell(0, 1))
    center_cell_text(table3.cell(0, 2))

    docx_output_path = f"/home/otabek/Desktop/file2_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.docx"
    document.save(docx_output_path)
    pdf_output_path = docx_output_path.replace('.docx', '.pdf')
    output_dir = '/'.join(pdf_output_path.split('/')[:-1])
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, docx_output_path],
                   check=True)
    return serialized_data


def file_three_create(serialized_data):
    file_path = '/home/otabek/Desktop/3-variant uchun shakl.docx'
    document = Document(file_path)

    paragraph0 = document.paragraphs[0]
    paragraph1 = document.paragraphs[1]
    paragraph2 = document.paragraphs[2]

    paragraph0.text = "Алоқадор шахсларнинг эҳтимолий манфаатлар тўқнашуви тўғрисидаги"
    paragraph0.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph0.runs[0].bold = True

    paragraph1.text = "ДЕКЛАРАЦИЯ"
    paragraph1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph1.runs[0].bold = True

    paragraph2.text = f"Мен {serialized_data.get("related_persons_full_name") or ''}, ушбу декларацияда алоқадор шахс сифатида ўзим ва ходим (ишга кираётган номзоднинг) эҳтимолий манфаатлар тўқнашувига оид қуйидаги маълумотларни маълум қиламан:\n"
    paragraph2.runs[0].bold = False

    table1 = document.tables[0]
    table2 = document.tables[1]

    table1.cell(0, 2).text = serialized_data.get('related_persons_passport_number') or ''
    table1.cell(1, 2).text = serialized_data.get('employee_legal_entity_name') or ''
    table1.cell(2, 2).text = serialized_data.get('employee_stir_number') or ''
    table1.cell(3, 2).text = (serialized_data.get('employee_full_name') or ''
                              + serialized_data.get('employee_position') or '')
    table1.cell(4, 2).text = serialized_data.get('related_persons_kinship_data') or ''
    table1.cell(5, 2).text = serialized_data.get('employee_legal_entity_data') or ''

    table2.cell(0, 1).text = f"________________________\n Шахсий имзо ёки электрон рақамли имзоси"
    table2.cell(0, 2).text = (f"{serialized_data.get('related_persons_full_name') or ''}"
                              f" \n {serialized_data.get('filled_date') or ''}")

    center_cell_text(table1.cell(0, 2))
    center_cell_text(table1.cell(1, 2))
    center_cell_text(table1.cell(2, 2))
    center_cell_text(table1.cell(3, 2))
    center_cell_text(table1.cell(4, 2))
    center_cell_text(table1.cell(5, 2))
    center_cell_text(table2.cell(0, 1))
    center_cell_text(table2.cell(0, 2))

    docx_output_path = f"/home/otabek/Desktop/file3_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.docx"
    document.save(docx_output_path)
    pdf_output_path = docx_output_path.replace('.docx', '.pdf')
    output_dir = '/'.join(pdf_output_path.split('/')[:-1])
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, docx_output_path],
                   check=True)
    return serialized_data
