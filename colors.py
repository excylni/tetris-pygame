import pathlib

class Colors:
    @staticmethod
    def get_cell_colors():
        color_codes = [
            (36, 41, 60),    # 0 - dark grey
            (47, 230, 23),   # 1 - green
            (232, 18, 18),   # 2 - red
            (226, 116, 17),  # 3 - orange
            (237, 234, 4),   # 4 - yellow
            (166, 0, 247),   # 5 - purple
            (21, 204, 209),  # 6 - cyan
            (13, 64, 216)    # 7 - blue
            ]
        return {i: color_codes[i] for i in range(len(color_codes))}