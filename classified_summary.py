import xlrd
import xlsxwriter
import os


def write_distribute(result,filename):
    # year = "2020"
    # if "2019" in filename:
    #     year = "2019"
    # sheetname = filename.split(year)[1]+filename.split(year)[2].split(".xls")[0]
    sheetname = "Sheet1"
    keylist = sorted(result.keys())
    xls2 = xlsxwriter.Workbook(filename)
    sht1 = xls2.add_worksheet(sheetname)
    sht1.write(0, 9, "分段")
    sht1.write(0, 10, "数量")
    for i in range(len(result)):
        sht1.write(i+1, 9, keylist[i])
        sht1.write(i+1, 10, result[keylist[i]])
    xls2.close()


# def write(result,filename):
#     from openpyxl import load_workbook
#     wb = load_workbook(filename)  # 生成一个已存在的wookbook对象
#     wb1 = wb.active  # 激活sheet
#     wb1.cell(1, 1, "分段")
#     wb1.cell(1, 2, "数量")
#     for i in range(len(result)):
#         wb1.cell(i+2, 1, result[i][0])
#         wb1.cell(i+2, 2, result[i][1])
#     wb.save("xxx.xlsx")  # 保存


def read_excel(filename):
    result = {}
    year = "2020"
    # if "2019" in filename:
    #     year = "2019"
    # sheetname = filename.split(year)[1]+filename.split(year)[2].split(".xls")[0]
    sheetname = "Sheet1"
    wb = xlrd.open_workbook(filename=filename)#打开文件
    sheet1 = wb.sheet_by_name(sheetname)#通过名字获取表格
    total = sheet1.cell_value(2, 1)
    interval = 100

    for i in range(int(total)):
        floor = sheet1.cell_value(7+i, 6) - sheet1.cell_value(7+i, 6) % interval
        if floor in result:
            result[floor] += 1
        else:
            result[floor] = 1
    # count = 0
    # for i in range(int(total)):
        # temp = sheet1.cell_value(i+7, 6)
        # if temp >= floor:
        #     count += 1
        # else:
        #     if count != 0:
        #         result.append([floor, count])
        #     floor = temp - temp % interval
        #     count = 1
    # result.append([floor, count])
    return result


def get_files(path, suffix):
    return [os.path.join(file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]

if __name__ =="__main__":
    root = "./weibo_data/"
    filename_list =get_files(root, ".xlsx")
    for filename in filename_list:
        result = read_excel(root + filename)
        write_distribute(result, root + filename)
