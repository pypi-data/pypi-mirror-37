如何在样本文件中添加行号到行首
awk '{print FNR","$0}' iris.csv > iris.proc.csv
