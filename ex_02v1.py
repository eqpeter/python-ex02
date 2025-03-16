import csv
from os.path import isfile

class Income:
    """代表一筆資料 (年度銷貨收入紀錄)"""
    all = []

    def __init__(self, year, sales, profit):
        """初始化一筆(年度)資料，並附加入報表串列"""
        self.year = int(year)
        self.sales = int(sales)
        self.profit = int(profit)
        self.rate = self.profit / self.sales  # 計算獲利率
        self.rank = 0  # 初始化排名
        Income.all.append(self)

    def __repr__(self) -> str:
        """傳回描述每筆(列)資料的字串"""
        return f"Income({self.year}, {self.sales}, {self.profit})"

    def __str__(self):
        """傳回列印時每筆(列)資料的字串(已排版)"""
        return f"{self.year:>6d} {self.sales:>12,d} {self.profit:>12,d} {self.rate:>8.2%} {self.rank:>6d}"

    def __lt__(self, other):
        """以獲利率比較大小"""
        return self.rate < other.rate

    @classmethod
    def sort_rate(cls):
        """以獲利率排序報表並填入名次(欄位)"""
        sorted_list = sorted(cls.all, reverse=True)  # 由高到低排序
        for i, income in enumerate(sorted_list, 1):
            income.rank = i

    @classmethod
    def report(cls):
        """印出整份財務報表"""
        cls.sort_rate()  # 先計算排名
        print("\n   年度        營業額       利潤      獲利率     排名")
        print("="*56)
        for income in sorted(cls.all, key=lambda x: x.year):  # 依年度排序
            print(income)
        print("="*56)

def save_to_csv(CSV_FILENAME):
    """儲存報表至指定檔案名稱"""
    with open(CSV_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        for income in Income.all:
            writer.writerow([income.year, income.sales, income.profit])

def load_csv(CSV_FILENAME):
    """載入檔案，恢復報表資料"""
    Income.all.clear()  # 清空現有資料
    if isfile(CSV_FILENAME):
        with open(CSV_FILENAME, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                Income(row[0], row[1], row[2])

def entry(CSV_FILENAME):
    """要求輸入營業數據，以建立年度資料物件並存檔"""
    print("\n=== peter奶茶-財務報表輸入系統 ===")
    print("請依照以下格式輸入資料：")
    print("年度,營業額,利潤")
    print("範例: 110,2234000,122200")
    print("按下 'Q' 或 'q' 結束輸入\n")
    
    while True:
        try:
            data = input('請輸入資料: ').strip()
            if data.upper() == 'Q':
                print("\n資料輸入完成！")
                break
            
            year, sales, profit = data.split(',')
            # 驗證輸入的數值
            if not all(val.strip().isdigit() for val in [year, sales, profit]):
                print("錯誤：所有數值必須為正整數！")
                continue
                
            Income(year, sales, profit)
            print(f"已新增 {year} 年度資料")
            
        except ValueError:
            print("錯誤：請按照格式輸入三個數值，以逗號分隔！")
            continue
    
    save_to_csv(CSV_FILENAME)

if __name__ == '__main__':
    # 要求使用者輸入部門代碼作為檔案名稱
    filename = input('\n請輸入部門代碼: ') + '.csv'
    
    # 載入既有資料（如果檔案存在）
    load_csv(filename)
    
    # 顯示目前的報表
    print('\n=== 目前的報表 ===')
    Income.report()
    
    # 進入資料輸入模式
    entry(filename)
    
    # 顯示更新後的報表
    print('\n=== 更新後的報表 ===')
    Income.report()