## 项目架构

目前架构包含三个主要应用集合：

1. 第一个应用集合是原始数据层，该集合中的应用主要负责**原始**数据的输入、存储与显示。目前仅包含 finance_report 应用，用于历史原始财务数据，和最基本的股票数据（仅包含股票编码、股票名称和市值等）。未来可添加更多原始数据，例如股票历史价格数据等。

2. 第二个应用集合是选股模型数据层，该层应用依赖于原始数据层。该集合中的应用主要负责各选股模型所需的关键数据的计算、存储与显示。目前仅包含 magic_formula 应用，用于神奇公式关键数据。注意该层不仅计算与存储历史关键数据，还会存储与显示最新关键数据快照。未来可添加多种选股模型与数据。

3. 第三个应用集合是数据应用显示层，该层应用依赖于原始数据层与选股模型数据层。该集合中的应用主要负责应用选股模型数据层的计算结果进行选股并显示。目前仅包含 eval\_utility 应用。eval\_utility 应用不含有图形用户界面，在 matplotlib 与 python 命令行交互界面中显示选股结果供参考。
   
   目前 eval\_utility 中的 china\_magic\_formula.py 脚本显示神奇公式的选股结果，而 china\_import.py 脚本负责导入与生成 finance\_report 与 magic\_formula 中的数据（其实 china\_import.py 的功能应该分开至 finance\_report 和 magic\_formula 应用层中去实现。目前为简单先放在 eval\_utility 应用层中）。
   
## 项目运行

在项目 evalstock 根目录下运行以下所有脚本：

1. 运行 `python manage.py makemigrations`

2. 运行 `python manage.py migrate`

3. 运行 `python manage.py createsuperuser`

4. 运行 `python manage.py runserver`

至此可以访问 <http://127.0.0.1:8000/admin/> 查看管理界面。但数据是空的，需要导入。

## 导入数据

1. 从 <https://www.dropbox.com/s/tvzo3grv691n4oz/raw_data.zip?dl=0> 下载全部历史财务数据与最新市场数据并解压至 eval_utility 目录下

2. 从 <https://www.dropbox.com/s/f13iao1g8yeavx0/STHeiti_Medium_1.ttf?dl=0> 下载 matplotlib 所需的中文字体并保存至 eval\_utility 目录下

3. 运行 `python manage.py shell`（注意仍然是从项目 evalstock 根目录下运行）

4. 在 python 命令行交互界面运行 `import eval_utility.china_import` 导入原始数据

5. 在 python 命令行交互界面运行 `import eval_utility.china_magic_formula` 执行神奇公式选股。除了 matplotlib 散点图，该脚本还会将初选结果保存中 eval\_utility 目录下的 china\_magic\_formula\_results.csv。

   有关神奇公式的简单介绍，参阅：<https://github.com/prstcsnpr/qmagicformula>。注意该结果仅供参考，更多历史数据需要收集与参考。
