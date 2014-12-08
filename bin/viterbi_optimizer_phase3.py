from tokenizer import TweetTokenizer
class ViterbiOptimizerP3:
    def __init__(self,q_params,e_params,file_in,file_out,file_gold,states):
        print '\n \n'
        print '----- Initializing Viterbi Optimizer -----'
        self.q_params=q_params
        self.e_params=e_params
        self.file_in=file_in
        self.file_out=file_out
        self.file_gold=file_gold
        self.states=states
        self.states.remove('*')
        self.states.remove('STOP')
        for i in self.states:
            for j in self.states:
                if (i,j) not in self.q_params:
                    self.q_params[(i,j)]=0
        
    def tokenize_input(self):
        input_tokenizer=TweetTokenizer(self.file_in)
        print '----- Tokenizing Input File -----'
        input_tokenizer.tokenize()
        self.input_sentence=input_tokenizer.sentence_list

    def tokenize_gold(self):
        input_tokenizer=TweetTokenizer(self.file_gold)
        print '----- Tokenizing Gold Output File -----'
        input_tokenizer.tokenize()
        self.gold_sentence=input_tokenizer.sentence_list
        
    def run(self):
        print '----- Begin Calculations -----'
        self.start_params={}
        self.output_tokens=[]
        for i in self.q_params:
            if i[1]=='*':
                self.start_params[i[0]]=self.q_params[i]
        for i in self.states:
            if i not in self.start_params:
                self.start_params[i]=0
        print '----- Begin Tagging -----'
        for sentence in self.input_sentence:
            V=[{}]
            path={}
            for y in self.states:
                if (sentence[0][0],y) in self.e_params:
                    V[0][y]=self.start_params[y]*self.e_params[(sentence[0][0],y)]
                else:
                    V[0][y]=0
                path[y]=[y]
            
            for t in range(1,len(sentence)):
                V.append({})
                newpath={}
                
                for y in self.states:
                    if (sentence[t][0],y) not in self.e_params:
                        (prob,state) = max((V[t-1][y0] * self.q_params[(y,y0)] * 0, y0) for y0 in self.states)
                    else:
                        (prob, state) = max((V[t-1][y0] * self.q_params[(y,y0)] * self.e_params[(sentence[t][0],y)], y0) for y0 in self.states)
                    V[t][y]=prob
                    newpath[y]=path[state]+[y]
                path = newpath
            n=0
            if len(sentence)!=1:
                n=t
            #print_dptable(V)
            (prob,state) = max((V[n][y], y) for y in self.states)
            newsentence=[]
            for i in range(len(path[state])):
                if sentence[i][0][0]=='#':
                    tag='#'    
                elif sentence[i][0][0]=='@' and len(sentence[i][0])!=1:
                    tag='@'
                elif sentence[i][0][0:4]=='http':
                    tag='U'
                else:
                    tag=path[state][i]
                newsentence.append((sentence[i][0],tag))
            self.output_tokens.append(newsentence)

        output_file = open(self.file_out, 'w')
        final_output = ""
        for row in self.output_tokens:
            for word in row:
                for token in word:
                    final_output += token + '\t'
                final_output+= '\n'
            final_output+= '\n'
        output_file.write(final_output)
        output_file.close()
        print '----- Tagging Complete. Saved to '+self.file_out+' -----'
    
    def compare_accuracy(self):
        totaltags=0
        totalcorrect=0
        for i in range(len(self.gold_sentence)):
            for j in range(len(self.gold_sentence[i])):
                if self.gold_sentence[i][j][1]==self.output_tokens[i][j][1]:
                    totalcorrect=totalcorrect+1
                totaltags=totaltags+1
        percentage_accuracy = totalcorrect/float(totaltags)*100
        print "Accuracy: %.2f%%" % percentage_accuracy
                