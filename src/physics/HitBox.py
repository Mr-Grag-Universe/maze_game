class HitBox:
    def __init__(self, map : str):
        rows = map.split('\n')
        self.map = rows

    def mask(self):
        map_mask = []
        for row in self.map:
            line = []
            for s in row:
                line.append(s != ' ')
            map_mask.append(line)
        return map_mask