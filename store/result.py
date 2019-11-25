import constants


class PlaneResult(object):
    """飞机游戏结果"""
    # 得分
    __score = 0
    # 生命数量
    __life = 3
    # 生命值
    __blood = 1000

    @property
    def score(self):
        """以属性方式获取分数"""
        return self.__score

    @score.setter
    def score(self, value):
        """分数设值"""
        if value < 0:
            print("分数不能为负数")
        else:
            self.__score = value

    def record_highest_score(self):
        """记录最高分"""
        history_score = self.get_history_score()
        if history_score < self.score:
            with open(constants.HISTORY_SCORE_FILE, 'w') as score_file:
                score_file.write(str(self.score))

    def get_history_score(self):
        """获取历史最高分"""
        history_score = 0
        with open(constants.HISTORY_SCORE_FILE, 'r') as score_file:
            temp = score_file.read()
            if temp:
                history_score = int(temp)
        return history_score
