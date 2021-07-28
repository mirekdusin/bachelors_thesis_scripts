#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
from concurrent.futures.thread import ThreadPoolExecutor

all_keyword = []


def parse_row(row):
    if row:
        transformed_row = [0] * 39
        transformed_row.insert(0, re.sub('\s+', ' ', row[0]))

        parts = row[1].split("|")
        for part in parts:
            part = part.rstrip("\n")
            re.sub('\s+', ' ', part)
            if part == 'Zdravotnictví':
                transformed_row.insert(1, 1)
            elif part == 'Lidé bez domova':
                transformed_row.insert(2, 1)
            elif part == 'Senioři':
                transformed_row.insert(3, 1)
            elif part == 'Životní prostředí':
                transformed_row.insert(4, 1)
            elif part == 'Kultura':
                transformed_row.insert(5, 1)
            elif part == 'Benefiční akce':
                transformed_row.insert(6, 1)
            elif part == 'Foreign volunteer':
                transformed_row.insert(7, 1)
            elif part == 'Práce se zvířaty':
                transformed_row.insert(8, 1)
            elif part == 'Sport':
                transformed_row.insert(9, 1)
            elif part == 'Mimořádné události':
                transformed_row.insert(10, 1)
            elif part == 'Děti a mládež':
                transformed_row.insert(11, 1)
            elif part == 'Lidé s hendikepem':
                transformed_row.insert(12, 1)
            elif part == 'Lidská práva':
                transformed_row.insert(13, 1)
            elif part == 'Lidé s autismem':
                transformed_row.insert(14, 1)

        parts = row[2].split("|")
        for part in parts:
            part = part.rstrip("\n")
            re.sub('\s+', ' ', part)
            if part == 'Produkce audio/video':
                transformed_row.insert(15, 1)
            elif part == 'Grafika a design':
                transformed_row.insert(16, 1)
            elif part == 'Administrativa':
                transformed_row.insert(17, 1)
            elif part == 'jiné':
                transformed_row.insert(18, 1)
            elif part == 'Fundraising':
                transformed_row.insert(19, 1)
            elif part == 'Management':
                transformed_row.insert(20, 1)
            elif part == 'Umělecká tvorba':
                transformed_row.insert(21, 1)
            elif part == 'Daně a účetnictví':
                transformed_row.insert(22, 1)
            elif part == 'Vzdělávání, studijní nebo diskusní zaměření':
                transformed_row.insert(23, 1)
            elif part == 'Technologie a online':
                transformed_row.insert(24, 1)
            elif part == 'Marketing':
                transformed_row.insert(25, 1)
            elif part == 'Personalistika':
                transformed_row.insert(26, 1)
            elif part == 'Doprovázení':
                transformed_row.insert(27, 1)
            elif part == 'Volnočasové aktivity':
                transformed_row.insert(28, 1)
            elif part == 'Psaní a překlady':
                transformed_row.insert(29, 1)
            elif part == 'Manuální práce':
                transformed_row.insert(30, 1)

        transformed_row.insert(31, re.sub('\s+', ' ', row[3]))
        transformed_row.insert(32, re.sub('\s+', ' ', row[4]))
        transformed_row.insert(33, re.sub('\s+', ' ', row[5]))
        transformed_row.insert(34, re.sub('\s+', ' ', row[6]))
        transformed_row.insert(35, re.sub('\s+', ' ', row[7]))
        transformed_row.insert(36, re.sub('\s+', ' ', row[8]))
        transformed_row.insert(37, re.sub('\s+', ' ', row[9]))
        transformed_row.insert(38, re.sub('\s+', ' ', row[10]))

        return transformed_row


executor = ThreadPoolExecutor(8)
futures = []
csv_header = ["Název pomoci", "Zdravotnictví", "Lidé bez domova", "Senioři", "Životní prostředí",
              "Kultura", "Benefiční akce", "Foreign volunteer","Práce se zvířaty", "Sport",
              "Mimořádné události", "Děti a mládež", "Lidé s hendikepem", "Lidská práva",
              "Lidé s autismem", "Produkce audio/video", "Grafika a design", "Administrativa",
              "jiné", "Fundraising", "Management", "Umělecká tvorba",
              "Daně a účetnictví", "Vzdělávání, studijní nebo diskusní zaměření",
              "Technologie a online", "Marketing", "Personalistika", "Doprovázení", "Volnočasové aktivity",
              "Psaní a překlady", "Manuální práce", "Trvání", "Věk dobrovolníka", "Účast",
              "Datum od", "Datum do", "Datum publikování", "Publikoval", "Naplněnost"]

with open('output_parsed.csv', mode='w', newline='') as output:
    output_writer = csv.writer(output,
                               delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_ALL)
    output_writer.writerow(csv_header)
    with open('output.csv', 'r') as read_obj:
        reader = csv.reader(read_obj, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) != 0:
                if row:
                    future = executor.submit(parse_row, row)
                    futures.append(future)

        for future in futures:
            result = future.result()
            if len(result) != 0:
                print(result)
                output_writer.writerow(result)
