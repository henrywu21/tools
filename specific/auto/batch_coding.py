#! /usr/bin/env python3

import os
import re

kst_home = None

spaces = '    '

def insert_surround_code_in_block(_brand: str, _file_name: str,
                                  _line_pattern_begin: str, _line_pattern_end: str,
                                  _code_to_insert_begin: str, _code_to_insert_end: str):
    _kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand) + _file_name
    code = ''
    spaces = '    '
    begin = False
    with open(_kst_code_path) as fp_kst:
        for line in fp_kst.readlines():
            if begin:
                if re.search(_line_pattern_end, line):
                    code = code.rstrip('\n') + "\n" + spaces + _code_to_insert_end + "\n\n"
                    begin = False

                code = code + line
            elif re.search(_line_pattern_begin, line):
                code = code + "\n" + line
                code = code + spaces + _code_to_insert_begin + "\n"
                begin = True
            else:
                code = code + line

    new_file = _brand + "/" + _file_name
    with open(new_file, 'w') as new_fp:
        new_fp.write(code)


def rep_insert_surround_code_in_block(_brand: str, _file_name: str,
                                      _code_to_insert_begin: str, _code_to_insert_end: str):
    _kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand) + _file_name
    code = ''
    spaces = '    '
    begin = False
    with open(_kst_code_path) as fp_kst:
        for line in fp_kst.readlines():
            if begin:
                if re.search('smoke_assert_code_ok', line):
                    code = code + spaces + _code_to_insert_begin + "\n"
                elif re.search('^done <.*.txt', line):
                    code = code + spaces + _code_to_insert_end + "\n\n"
                    code = code + line
                    begin = False
                elif line != '\n':
                    code = code + line
            elif re.search('smoke_url \\$url', line):  # bypass
                code = code + spaces + 'smoke_url_ok $url\n'
                begin = True
            else:
                code = code + line

    new_file = _brand + "/" + _file_name
    with open(new_file, 'w') as new_fp:
        new_fp.write("{0}{1}".format(code.rstrip("\n"), "\n"))


def rep_with_template_adv(_brand: str, _file_name: str):
    _kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand) + _file_name

    is_target = False
    code = '{0}elif [[ "$script_name" == \'{1}\' ]]; then\n'.format(spaces, _file_name)
    begin = False
    idx = 0
    is_in_if = False

    with open(_kst_code_path) as fp_kst:
        for line in fp_kst.readlines():
            if begin:
                if re.search('^done <.*.txt', line):
                    code = code.rstrip().rstrip("fi")  # remove last line of 'fi'
                    break
                elif re.search('^smoke_assert_', line.strip()):
                    if is_in_if:
                        code = code + spaces

                    line = line.strip()
                    re_comment = re.search('(.*)#(.*)', line)
                    if not re_comment:
                        code += '{2}{2}asserts_array[{0}]="{1}"\n'.format(idx, line.replace('\"', '\\"'), spaces)
                    else:  # has comments
                        code += '{3}{3}asserts_array[{0}]="{1}"  # {2}\n'.format(idx,
                                                                           re_comment[1].replace('\"', '\\"').strip(),
                                                                           re_comment[2].strip(), spaces)
                    idx = idx + 1
                else:
                    code = code + line

                    re_if = re.search('^(if|elif|else)', line.strip())
                    re_fi = re.search('^fi', line.strip())
                    if re_if:
                        is_in_if = True
                    elif re_fi:
                        is_in_if = False

            elif re.search('smoke_assert_code_msg\\) == "success"', line):  # bypass
                is_target = True
                begin = True

    if is_target:
        new_file = _brand + "/adv/" + _file_name
        with open(new_file, 'w') as new_fp:
            new_fp.write(code)


def rep_with_template(_brand: str, _file_name: str) -> bool:
    _kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand) + _file_name

    spaces = '    '
    is_target_script = False
    is_assert_section = False
    asserts = []
    pagetype = None
    with open(_kst_code_path) as fp_kst:
        for line in fp_kst.readlines():
            line = line.strip()
            if line == '' or re.search('^#', line):
                continue

            if re.search('^(?:smoke_url_ok|smoke_url) \\$url', line):
                is_assert_section = True
                is_target_script = True
                continue

            if is_assert_section:
                re_url_file = re.search('^done < \\$urlspath/(.*.txt)', line)
                if re_url_file:
                    url_file = re_url_file[1]
                    break

                re_assert = re.search('^smoke_assert_', line)
                re_assert_code = re.search('^smoke_assert_code', line)
                if re_assert and not re_assert_code:
                    asserts.append(line.strip())
                    continue
                else:
                    re_if_404 = re.search("smoke_assert_code '404'", line)
                    re_if_success = re.search('if \\[ \\$\\(smoke_assert_code_msg\\) == "success" \\]; then', line)
                    re_if_valid_url = re.search('if \\$\\(is_valid_url \\$url\\); then', line)
                    re_fi = re.search('^fi$', line)
                    if not (re_if_404 or re_if_success or re_if_valid_url or re_fi):
                        is_target_script = False
                        break

            re_pagetype = re.search('^pagetype="(.*)"', line)
            if pagetype is None and re_pagetype:
                pagetype = re_pagetype[1]
                continue

    if is_target_script:
        new_file = _brand + "/" + _file_name
        code = "#!/bin/bash\n\n. _chk_keywords_helper\n\n"
        code += 'ORIG_FS=$IFS\nIFS=";"\n'
        code += 'declare -a asserts_array\n\n'

        code += 'pagetype="{0}"\n'.format(pagetype)
        code += 'urls_file="{0}"\n\n'.format(url_file)

        code += 'asserts_array=$(cat<<SmokeAssertContainer\n'
        for _assert in asserts:
            code += spaces + _assert + "\n"

        code += 'SmokeAssertContainer\n)\n'
        code += '\nsmoke_assert $pagetype $urls_file "${asserts_array[*]}"\n'
        code += '\nIFS=$ORIG_FS\n\n'

        with open(new_file, 'w') as new_fp:
            new_fp.write(code.rstrip() + "\n")

        return True
    else:
        return False


def heredoc_style(_brand: str, _file_name: str):
    _kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand) + _file_name
    code = ''
    begin = False
    with open(_kst_code_path) as fp_kst:
        for line in fp_kst.readlines():
            if re.search('ORIG_FS=\\$IFS; IFS=#', line):
                code += 'ORIG_FS=$IFS\nIFS=\";"\n'
                continue

            re_asserts = re.search('^asserts_array\\[\d+\\]="(.*)"(.*)', line)
            if begin:
                if re.search('^smoke_assert', line):
                    code = code.rstrip() + "\n\nSmokeAssertContainer\n)\n\n"
                    code += line + '\nIFS=$ORIG_FS\n\n'
                    break
                elif re_asserts:
                    code += "\n" + spaces + re_asserts[1].replace('\\"', '"') + re_asserts[2]
                else:
                    code += line
            elif re_asserts:
                begin = True
                code += 'asserts_array=$(cat<<SmokeAssertContainer\n'
                code += spaces + re_asserts[1].replace('\\"', '"') + re_asserts[2]
            else:
                code += line

    new_file = _brand + "/" + _file_name
    with open(new_file, 'w') as new_fp:
        new_fp.write(code.rstrip() + "\n")


if __name__ == "__main__":
    try:
        kst_home = str(os.environ['KST_HOME']).rstrip('/')
    except KeyError:
        print('\n\t>hint: set environment variable "KST_HOME" to show failed KST code')
        exit(-1)

    # for brand in ['tvg', 'chowhound', 'download', 'metacritic', 'techrepublic', 'zdnet']:
    #     print('===> Working on brand: {0}...'.format(brand))
    #     os.makedirs(brand, exist_ok=True)
    #     kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand)
    #
    #     for fn in os.listdir(kst_code_path):
    #         if re.search('^chk_keywords_', fn):
    #             heredoc_style(brand, fn)

    for brand in ['cnet']:
        print('===> Working on brand: {0}...'.format(brand))
        os.makedirs(brand, exist_ok=True)
        os.makedirs(brand + "/adv/", exist_ok=True)
        kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand)
        cnt = 0
        adv_cnt = 0
        for fn in os.listdir(kst_code_path):
            if re.search('^chk_keywords_', fn):
                if rep_with_template(brand, fn):
                    cnt = cnt + 1
                else:
                    rep_with_template_adv(brand, fn)
                    adv_cnt = adv_cnt + 1

        print('Summary: brand: {0}: count: {1}; adv_cnt: {2}'.format(brand, cnt, adv_cnt))

    # code_to_insert_begin = 'if [ $(smoke_assert_code_msg) == "success" ]; then'
    # code_to_insert_end = 'fi'
    #
    # for brand in ['chowhound', 'tvg', 'metacritic', 'download']:
    #     print('brand: ' + brand)
    #     os.makedirs(brand, exist_ok=True)
    #     kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand)
    #     for fn in os.listdir(kst_code_path):
    #         if re.search('^chk_keywords_', fn) and not re.search('404', fn):
    #             print(kst_code_path + fn)
    #             rep_insert_surround_code_in_block(brand, fn, code_to_insert_begin, code_to_insert_end)

    # line_pattern_begin = 'smoke_url_ok \\$url'
    # line_pattern_end = '^done <.*.txt'
    # for brand in ['cnet', 'techrepublic', 'zdnet']:
    #     print('brand: ' + brand)
    #     os.makedirs(brand, exist_ok=True)
    #     kst_code_path = '{0}/{1}/bin/'.format(kst_home, brand)
    #     for fn in os.listdir(kst_code_path):
    #         if re.search('^chk_keywords_', fn) and not re.search('404', fn):
    #             print(kst_code_path + fn)
    #             insert_surround_code_in_block(brand, fn, line_pattern_begin, line_pattern_end, code_to_insert_begin,
    #                                           code_to_insert_end)
