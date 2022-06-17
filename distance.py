import methods as methods

class Distances:
    def __init__(self, src, bd):
        self.src = src
        self.bd = bd
        self.index = []
        self.direction = []
        self.angle = []
        self.centroid = []   
        self.vector = []


    def minRec(self, box):
        sum_x = 0
        sum_y = 0
        for (x,y) in box: 
            sum_x += x
            sum_y += y
        x = int(sum_x/4)
        y = int(sum_y/4)
        self.xy.append((x,y))
        

    def grab(self):
        distance_x = self.xy[-1][0] - self.bd[0]
        distance_y = self.xy[-1][1] - self.bd[1]
        self.distance.append((int(distance_x), int(distance_y)))
        

    def draw(self):
        if self.xy:
            x = self.xy[-1][0]
            y = self.xy[-1][1]
            text_direction = str(self.direction[-1])
            methods.draw_text(self.src,'direction:' + text_direction,(x - 20, y - 10))
            text_index = str(self.index[-1])
            methods.draw_text(self.src,'Indexes:' + text_index,(x - 20, y + 10))
            '''
            if self.index[-1] == "O" or self.index[-1] == 0 or self.index[-1] == "I" or self.index[-1] == 4:
                line_length = 60
                angle = self.angle[-1] * np.pi / 180
                (x2,y2) = (x + line_length*np.cos(angle), y + line_length*np.sin(angle))
                cv.arrowedLine(self.src, (x, y), (int(x2), int(y2)),(75,175,125), 3)
            '''