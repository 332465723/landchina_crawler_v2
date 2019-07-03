# -*- coding: utf-8 -*-

from fontTools.ttLib import TTFont


class FontDecoder(object):
    def __init__(self, obj_font_file_path, std_font_file_path='./microsoft_yahei_simpli.woff'):
        self.obj_font = TTFont(obj_font_file_path)
        self.std_font = TTFont(std_font_file_path)
        self.word_map = {}
        self.missing_code_map = []
        self.glyph_map = []


    def obj_unicode_list(self):
        return self.obj_font.getGlyphOrder()


    def std_unicode_list(self):
        return self.std_font.getGlyphOrder()


    def generate_word_map(self):
        for obj_code in self.obj_unicode_list():
            hit_flag = False
            try:
                obj_char_coordinates = self.obj_font['glyf'][obj_code].coordinates
            except Exception as e:
                self.missing_code_map.append(obj_code)
                continue

            for std_code in self.std_unicode_list()[1252:8017]: # the range covers almost all Chinese charactors in unicode
                try:
                    std_char_coordinates = self.std_font['glyf'][std_code].coordinates
                except Exception as e:
                    continue

                # There might be many other ways to match Chinese charactors
                if self.is_same_char1(obj_char_coordinates, std_char_coordinates):
                    obj_unicode = eval("u'\u" + obj_code[3:] + "'")
                    std_unicode = eval("u'\u" + std_code[3:] + "'")
                    self.word_map[obj_unicode] = std_unicode
                    # TODO identify Chinese charactor by coordinates of each glyph
                    self.glyph_map.append((list(obj_char_coordinates), std_unicode))
                    hit_flag = True
                    break

            if not hit_flag:
                self.missing_code_map.append(obj_code)

        return self.word_map

    # some future work TODO
    def generate_glyph_map(self, glyph_map_file):
        with open(glyph_map_file, 'w') as fp:
            for obj in self.glyph_map:
                try:
                    glyph_str = obj[0].__repr__()
                    char_str = obj[1].encode('utf-8')
                except:
                    continue
                fp.write('%s\n' % glyph_str)
                fp.write('%s\n' % char_str)

    def is_same_char1(self, coor1, coor2):
        arr1 = [x[0] for x in coor1]
        arr2 = [x[0] for x in coor2]

        if abs(len(arr1) - len(arr2)) > 2:
            return False

        idx1 = 0
        idx2 = 0
        while (idx1 < len(arr1) and idx2 < len(arr2)):
            if abs(arr1[idx1] - arr2[idx2]) > 5:
                if len(arr1) > len(arr2):
                    idx1 += 1
                elif len(arr1) < len(arr2):
                    idx2 += 1
                else:
                    return False
            else:
                idx1 += 1
                idx2 += 1

        if abs(idx1 - idx2) > 2:
            return False
        else:
            return True


    def is_same_char2(self, coor1, coor2):
        arr1 = [x[0] for x in coor1]
        arr2 = [x[0] for x in coor2]

        if abs(len(arr1) - len(arr2)) > 2:
            return False

        for i in range(0, 10):
            if abs(arr1[i] - arr2[i]) > 5:
                return False

        for i in range(-1, -11, -1):
            if abs(arr1[i] - arr2[i]) > 5:
                return False

        return True

if __name__ == '__main__':
    fd1 = FontDecoder(obj_font_file_path='./fonts/test1.woff', std_font_file_path='fonts/microsoft_yahei_simpli.woff')
    word_map1 = fd1.generate_word_map()

    fd2 = FontDecoder(obj_font_file_path='./fonts/test2.woff', std_font_file_path='fonts/microsoft_yahei_simpli.woff')
    word_map2 = fd2.generate_word_map()

    fd3 = FontDecoder(obj_font_file_path='./fonts/test3.woff', std_font_file_path='fonts/microsoft_yahei_simpli.woff')
    word_map3 = fd3.generate_word_map()

    def unicode2str(code):
        import re
        if not type(code) == unicode:
            return None
        code_str = code.__repr__()
        match = re.search(ur'u(\w+)', code_str)
        if match:
            return 'uni' + match.group(1).upper()
        else:
            return None

    for k1, v1 in word_map1.items():
        k11 = unicode2str(k1)
        v11 = unicode2str(v1)
        print fd1.obj_font['glyf'][k11].coordinates.__repr__()

        for k2, v2 in word_map2.items():
            k22 = unicode2str(k2)
            v22 = unicode2str(v2)
            if v22 == v11:
                print fd2.obj_font['glyf'][k22].coordinates.__repr__()
                break

        for k3, v3 in word_map3.items():
            k33 = unicode2str(k3)
            v33 = unicode2str(v3)
            if v33 == v11:
                print fd3.obj_font['glyf'][k33].coordinates.__repr__()
                break

        print('================================================================\n\n')
