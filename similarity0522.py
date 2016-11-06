#coding:utf-8 
import jieba
file=open('d:\simi.csv','r+')
lines=file.readlines()
out=open('d:\simi_kekka.csv','w')
out.write('a,b,same,similarity\n')

fre=['客栈','旅馆','宾馆','酒店','旅舍','（','）','(',')','-','市','县']
dic=['楼','阁','预付','东翼','西翼','店']
spe=['（','）','(',')','-']

def freq(str):
	for f in fre:
		f=f.decode('utf8')
		str=str.replace(f,'')
	return str
	
def phra(x):
	return list(jieba.cut(x))

for line in lines:
	line=line.decode('GBk')
	line2=freq(line)
	list2=line2.split(',')
	phra_a=phra(list2[0].strip())   #第一列的字符串分词结果
	phra_b=phra(list2[1].strip())
	print '/'.join(phra_a)
	
	match=[i for i in phra_a if i in phra_b]
	all=list(set(phra_a).union(set(phra_b)))
	
	
	
	simi=len(match)*100/len(all)
	num=len(match)
	each=line.encode('mbcs').strip()+','+str(num)+','+str(simi)+','+'/'.join(phra_a).encode('mbcs')+','+'/'.join(phra_b).encode('mbcs')+','+'/'.join(match).encode('gbk')+','+'/'.join(all).encode('mbcs') 
	out.write(each)
	for i in dic:
		i=i.decode('utf-8')
		if i in line:
			for spec in spe:
				spec=spec.decode('utf-8')
				if spec in line:
					each2=','+'careful'
					out.write(each2)
	out.write('\n')		
	# for i in list[0]:
		# if i.lower() in list[1].lower():
			# num+=1
	# for i in list[1]:
		# if i.lower() in list[0].lower():
			# num+=1
	# simi=num*100/(len(list[0].strip())+len(list[1].strip()))
	
	# each=line.encode('mbcs').strip()+','+str(num)+','+str(simi)+'%\n'
	# out.write(each)

print 'solved\t'+str(len(lines))
print 'done'

