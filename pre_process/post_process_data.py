from bin.tokenizer import TweetTokenizer
def post_process_data(original_file,tagged_file,output_file_name):
    original = TweetTokenizer(original_file)
    tagged = TweetTokenizer(tagged_file)
    original.tokenize()
    tagged.tokenize()
    output_file=open(output_file_name,'w')
    output_string=""
    #print output_file_name
    ##print 'I am in here.'
    for i in range(len(original.sentence_list)):
        for j in range(len(original.sentence_list[i])):
            output_string+=original.sentence_list[i][j][0]+'\t'
            output_string+=tagged.sentence_list[i][j][1]+'\n'
            #print output_string
        output_string+='\n'
    output_file.write(output_string)
    output_file.close()
    