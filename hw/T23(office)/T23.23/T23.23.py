#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import docx
from docx.shared import RGBColor



def main(filename_input, filename_output, c1=RGBColor(0, 0, 0), c2=RGBColor(255, 0, 0)):
    doc1 = docx.Document(filename_input)

    run_list = [[run] for par in doc1.paragraphs for run in par.runs]

    run_list_res = []

    for par in run_list:
        tmp = []
        for run in par:
            if c1  == run.font.color.rgb == c1:
                run.font.color.rgb = c2
            tmp.append(run)
        run_list_res.append(tmp)

    doc2 = docx.Document()

    for par in run_list_res:
        doc2.add_paragraph(' '.join([run.text for run in par]))

    doc2.save(filename_output)


if __name__ == '__main__':
    main('test.docx', 'res.docx')