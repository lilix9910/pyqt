from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class MyTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(MyTableWidget, self).__init__(*args, **kwargs)

    def insert_df(self, df):
        """
        清空QTableWidget, 导入df
        :param df: DataFrame
        :return: None
        """
        self.clear()
        column_list = df.columns.tolist()
        self.setColumnCount(len(column_list))
        self.setRowCount(0)
        self.setHorizontalHeaderLabels([str(_) for _ in column_list])

        for row, row_lst in df.iterrows():
            self.setRowCount(self.rowCount()+1)
            for i in range(len(row_lst)):
                self.setItem(self.rowCount()-1, i, QTableWidgetItem(row_lst[i]))
