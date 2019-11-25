from game.war import PlaneWar


def main():
    """游戏入口函数"""

    # 开始游戏初始化
    war = PlaneWar()
    # 创建六架敌方小型飞机
    war.create_small_enemy_planes(6)
    # 运行游戏
    war.run_game()


if __name__ == "__main__":
    main()

