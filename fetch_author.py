def fetch():
	author_file = open("author_input.txt")
        authors = author_file.read().split('\n')
	author_file.close()
	try:
		done_authors = open("authors_output.txt", 'r')
		authored = done_authors.read().split('\n')
		done_authors.close()
	except:
		authored = []	
	for author in authors:
		author_item = author.split(',')[0]
		if author_item in authored:
			continue
		else:
			return author_item


def record_author(author):
	file = open("author_output.txt", 'a')
	file.write(author + '\n')
	file.close()



def test():
	item = fetch()
	print(item)
	record_author(item)
	item = fetch()
	print(item)
	record_author(item)

#test() 
