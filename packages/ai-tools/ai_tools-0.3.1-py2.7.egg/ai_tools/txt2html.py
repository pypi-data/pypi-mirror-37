# coding:utf-8
import sys


def txt2html(res_file,title_list_str,attach_info):

    TABLE = '<table>'
    TR = "<tr>"
    TD = "<td>"
    C_TABLE = "</table>"
    C_TR = "</tr>"
    C_TD = "</td>"
    title_list=title_list_str.split(",") 
    title_length=len(title_list)

    tableContent = '<table border="1"; style="border-collapse:collapse;text-align:left;">'
    tableContent += '<tr bgcolor="#CCCCCC">'
    for title in title_list:
        tableContent += '<td>%s</td>'%(title)
    tableContent += '</tr>'

    with open(res_file) as f:
        for line in f:
            items = line.strip().split(" ")
            tableContent += TR
            for item in items:
                tableContent += TD + str(item) + C_TD 
            tableContent += C_TR

    tableContent += C_TABLE

    mailContent = "<html>"
    mailContent += "<div style=\"text-align:center;\"><h3> 数据报告 </h3></div>"
    mailContent += "<p></p>"
    #mailContent += "<p>注：情感分取值[0,1], 值越大情感越正向。下表为每日情感分低于0.5的评论</p>"
    mailContent += "<p>%s</p>"%(attach_info)
    mailContent += tableContent
    mailContent += '</br>'
    mailContent += '</html>'

    #return tableContent
    print(mailContent)
    return mailContent


if __name__=="__main__":
    
    #txt2html("res.txt","t1,t2,t3.t4","import info")
    txt2html(sys.argv[1],sys.argv[2],sys.argv[3])
