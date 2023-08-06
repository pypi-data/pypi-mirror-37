import os
import os.path
import shutil
import hashlib
import pymysql
import time
import psycopg2

md5_list={}
source = {}


##########
'''
Get the Database links
0. for local Mysql
1. for remote nas Mysql
2. for remote nas postgre
'''
########
def getDB(a):
    if a == 1:
        conn = pymysql.connect(host='home.njnuko.top', port=33066, user='root', passwd='admin',db='nas_files')
    elif a == 0:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='',db='nas_files')
    elif a == 2:
        conn = psycopg2.connect(host='127.0.0.1', port=5432, user='ko', passwd='231231',db='nas_files')
    return conn


##########
'''
Checking files, ignore the files starts with ’@‘ and  ‘.’
and will create a checking.log in tofd
'''
########
def check_files(fromfd,tofd,log):
    global md5_list
    a=open(log,'a')
    for i in os.listdir(fromfd):
        
        if os.path.isdir(os.path.join(fromfd,i)):
            print(str(os.path.join(fromfd,i))+ " is directory")
            if i[0] not in ['@','.']:
                print(str(os.path.join(fromfd,i)) + " is not dummy folder")
                check_files(os.path.join(fromfd,i),tofd,log)
        else:
            the_md5=hashlib.md5()
            hash = ''
            with open(os.path.join(fromfd,i), 'rb') as f:
                the_md5.update(f.read())
                hash = the_md5.hexdigest()
            print("========================")
            print(md5_list)
            print("-------------------------")
            print(hash)
            print("========================")
            if hash != '':
                if hash in md5_list.values() :
                    print(os.path.join(fromfd,i)+' has been moved' + 'with md5:' + hash)
                    a.write(os.path.join(fromfd,i)+' has been moved' + 'with md5:' + hash+'\n')
                    if not os.path.exists(os.path.join(tofd,i)):
                        shutil.move(os.path.join(fromfd,i),tofd)
                    else:
                        os.remove(os.path.join(fromfd,i))
                else:
                    print("the hash code:" + hash + " has been insert")
                    md5_list[os.path.join(fromfd,i)] = hash
                    print(os.path.join(fromfd,i))
    a.close()


#######
'''
get the global dict:dic
and insert it into the Database with TableName
'''
#####
def InsertData(TableName,dic,dblink):
    try:
        conn = getDB(dblink)
        cur=conn.cursor()

        ###create table
        sql1 = "create table " + TableName + " (url varchar(1000), md5 varchar(20));" 
        cur.execute(sql1)


        list = []
        for key in dic.keys():
            a = (key,dic[key])
            list.append(a)

        sql = "insert into " + TableName + " values(%s,%s)"

        sql = cur.executemany(sql,list)
        conn.commit()
        
        cur.close()
        conn.close()
    except Exception as e:
      print("Insert Data Error %d: %s" % (e.args[0], e.args[1]))


################
'''
get the dic data from database
'''
###############
def GetData(TableName,dblink):   
    try:
        conn = getDB(dblink)
        cur=conn.cursor()
        dic = {}
        for key in dic.keys():
            a = (key,dic[key])
            list.append(a)

        sql = "select * from " + TableName

        cur.execute(sql)
        results = cur.fetchall()
        for i in results:
            dic[i[0]] = i[1] 
        conn.commit()
        cur.close()
        conn.close()
        return dic
    except Exception as e:
        print("Get Data Error %d: %s" % (e.args[0], e.args[1]))


#####################
'''
Compare the folder files with the existing dic,
and update the dic
'''
#####################
def compare_files(fromfd,tofd,log):
    global source
    a=open(log,'a')
    for i in os.listdir(fromfd):
       #print(str(os.path.join(foldername,i)+ os.path.isdir(os.path.join(fromfd,i)))
        if os.path.isdir(os.path.join(fromfd,i)):
            if i[0] not in ['@','.']:
        #print(str(os.path.join(fromfd,i)))
                compare_files(os.path.join(fromfd,i),tofd,log)
        else:
            the_md5=hashlib.md5()
            f = open(os.path.join(fromfd,i), 'rb')
            the_md5.update(f.read())
            hash = the_md5.hexdigest()
            f.close()

            if hash in source.values():
                a.write(os.path.join(fromfd,i)+' has been moved' + 'with md5:' + hash+'\n')
                move_out(fromfd,i,hash,tofd)
            else:
                source[os.path.join(fromfd,i)] = hash
    a.close()


######
'''''
Move out duplicate files
'''''
######
def move_out(fromfd,i,hashf,dest):
    if not os.path.exists(os.path.join(dest,i)):
        shutil.move(os.path.join(fromfd,i),dest)
    else:
        the_md5=hashlib.md5()
        f = open(os.path.join(dest,i), 'rb')
        the_md5.update(f.read())
        hashd = the_md5.hexdigest()
        f.close()
        if hashf == hashd:
            os.remove(os.path.join(fromfd,i))
        else:
            a = time.time()
            b = str(int(a))
            shutil.move(os.path.join(fromfd,i),os.path.join(dest,i+b))         
            

def sorting(frm,dest,dblink):
    if os.path.exists(os.path.join(dest,'sorting.txt')):
        os.remove(os.path.join(dest,'sorting.txt'))
        open(os.path.join(dest,'sorting.txt'),'w')
    log = os.path.join(dest,'sorting.txt')
    check_files(frm,dest,log)
    print(md5_list)
    InsertData('path_md5',md5_list,dblink)

def comparing(frm,dest,dblink):
    global source
    if os.path.exists(os.path.join(dest,'comparing.txt')):
        os.remove(os.path.join(dest,'comparing.txt'))
        open(os.path.join(dest,'comparing.txt'),'w')
    log = os.path.join(dest,'comparing.txt')
    source = GetData('path_md5',dblink)
    compare_files(frm,dest,log)
    InsertData('path_md5_c',source,dblink)





def main():
    pass
if __name__ == '__main__':
    main()
