# 🎮 Pacman-Agent 挑战
## 🐱‍👤 pacman-engine

欢迎来到 **Pacman-Agent 挑战**！🎉 这个引擎最初由加州大学伯克利分校的 **John DeNero**和 **Dan Klein**创建。📚

### 🚀 如何开始
要以键盘控制的方式运行游戏引擎，请使用以下命令：
```bash
python pacman.py
```

### 🛠️ 环境配置
- **Python 版本**：3.12.7 🐍

### 🕹️ 游戏挑战
以下是简单难度的两个游戏挑战。你需要实现 `ce811ManhattanGhostDodgerAgent` 和 `ce811ManhattanGhostDodgerHunterAgent` 来完成这些挑战。⚔️👻

**注意**：由于难度设置，以下命令可能会报错。你需要修复 `ce811ManhattanGhostDodgerAgent` 后再进行游戏。🔧

#### 挑战1：简单循环迷宫
```bash
python pacman.py -l simpleLoopMaze -p ce811ManhattanGhostDodgerAgent
```

#### 挑战2：带胶囊的简单循环迷宫
```bash
python pacman.py -l simpleLoopMazeCapsule -p ce811ManhattanGhostDodgerHunterAgent
```

### 📝 额外任务
以下命令需要你将 `part2` 文件夹中的相应 `.py` 文件内容复制到 `ce811Assignment2Agents.py` 中后再执行：

1. **一阶预测曼哈顿代理**
    ```bash
    python pacman.py -p ce811OneStepLookaheadManhattanAgent
    ```
    - 将 `part2/1.py` 内容复制到 `ce811Assignment2Agents.py`。

2. **一阶预测迪杰斯特拉代理**
    ```bash
    python pacman.py -p ce811OneStepLookaheadDijkstraAgent
    ```
    - 将 `part2/4.py` 内容复制到 `ce811Assignment2Agents.py`。

3. **迪杰斯特拉规则代理**
    ```bash
    python pacman.py -l simpleLoopMazeCapsule -p ce811DijkstraRuleAgent
    ```
    - 将 `part2/5.py` 内容复制到 `ce811Assignment2Agents.py`。

4. **迪杰斯特拉规则代理（无迷宫指定）**
    ```bash
    python pacman.py -p ce811DijkstraRuleAgent
    ```
    - 将 `part2/6.py` 内容复制到 `ce811Assignment2Agents.py`。

### ⚡ 快速获取游戏解决方案
如果你想快速获得游戏解决方案，可以在每个命令后添加 `-f -q -n 10` 参数。这将以无界面方式运行10次游戏，并为你提供平均分。📈
```bash
python pacman.py [你的命令] -f -q -n 10
```

### 🛡️ 实现代理
为了完成 **简单难度** 的两个游戏挑战，你需要实现以下代理：

- **ce811ManhattanGhostDodgerAgent** 🏃‍♂️👻
- **ce811ManhattanGhostDodgerHunterAgent** 🎯👻

确保在运行挑战时，这些代理已正确实现并放置在相应的文件中。🗂️

### ❓ 有问题？
如果在执行过程中遇到任何问题，请检查以下几点：

1. **Python 版本**是否正确（3.12.7）🐍。
2. **代理文件**是否已正确复制并命名为 `ce811Assignment2Agents.py` 📂。
3. **命令参数**是否正确无误 📝。

祝你游戏愉快，挑战成功！🎉🍀

---
python pacman.py -p ce811MyBestAgent
python pacman.py -p ce811MyBestAgent -f -q -n 10
如果你有任何疑问或需要进一步的帮助，请随时联系我，付费费咨询：QQ：284190056