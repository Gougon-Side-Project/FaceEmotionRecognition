class Rect():
    def __init__(self, top, bottom, left, right):
        self.start = [left, top]
        self.end = [right, bottom]

    @property
    def Top(self):
        return self.start[1]

    @Top.setter
    def Top(self, value):
        self.start[1] = value

    @property
    def Left(self):
        return self.start[0]

    @Left.setter
    def Left(self, value):
        self.start[0] = value

    @property
    def Bottom(self):
        return self.end[1]

    @Bottom.setter
    def Bottom(self, value):
        self.end[1] = value

    @property
    def Right(self):
        return self.end[0]

    @Right.setter
    def Right(self, value):
        self.end[0] = value

    def FitFaceToHeadSize(self):
        length = self.Bottom - self.Top
        transformDiff = int(length * 0.3)
        self.Top = self.Top - transformDiff
        self.Left = self.Left - int(transformDiff / 2)
        self.Right = self.Right + transformDiff - int(transformDiff / 2)