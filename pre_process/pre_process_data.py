import argparse
import re 

# pre-process (edit words) on both test and training data to get better results
# python pre_process_data.py -i train --type train
# python pre_process_data.py -i dev.in --type test

def pre_process_data(input_file, output_file,data_type):
	output = []

	with open(input_file, 'r') as f:
		for line in f:
			if contains_url(line):
				replace_url(line, output,data_type)

			elif contains_user(line):
				replace_user(line, output,data_type)

			elif contains_haha(line):
				replace_haha(line, output,data_type)

			elif contains_num(line):
				replace_num(line, output,data_type)

			elif contains_hashtag(line):
				replace_hashtag(line, output,data_type)

			else:
				write(line, output)
	
	with open(output_file, 'w') as output_f:
		for o in output:
			output_f.write(o)

	#print "pre-processed data file written to " + output_file

def write(line, output):
	output.append(line)


###########################
## find and replace urls ##
###########################

url = "http"
url_pattern = re.compile(url)

def contains_url(line):
	if url_pattern.match(line):
		return True
	else:
		return False

def replace_url(line, output,data_type):
	if data_type == "train":
		tag = line.split()[1]
		edited_line = url + '\t' + tag + '\n'
		output.append(edited_line)
	else:
		output.append(url + '\n')

###########################
## find and replace user ##
###########################

user = "@USER"
user_pattern = re.compile(user)

def contains_user(line):
	if user_pattern.match(line):
		return True
	else:
		return False

def replace_user(line, output,data_type):
	if data_type == "train":
		tag = line.split()[1]
		edited_line = user + '\t' + tag + '\n'
		output.append(edited_line)
	else:
		output.append(user + '\n')

###########################
## find and replace haha ##
###########################

haha = ".*haha.*"
haha_pattern = re.compile(haha)

def contains_haha(line):
	line = line.lower() # lowercase
	if haha_pattern.match(line):
		return True
	else:
		return False

def replace_haha(line, output,data_type):
	replacement = "haha"
	if data_type == "train":
		tag = line.split()[1]
		edited_line = replacement + '\t' + tag + '\n'
		output.append(edited_line)
	else:
		output.append(replacement + '\n')


##############################
## find and replace numbers ##
##############################

num = "[0-9]+"
num_pattern = re.compile(num)

def contains_num(line):
	if num_pattern.match(line):
		return True
	else:
		return False

def replace_num(line, output,data_type):
	replacement = "1000"
	if data_type == "train":
		tag = line.split()[1]
		edited_line = replacement + '\t' + tag + '\n'
		output.append(edited_line)
	else:
		output.append(replacement + '\n')


###############################
## find and replace hashtags ##
###############################

hashtag_pattern = re.compile("#")

def contains_hashtag(line):
	if hashtag_pattern.match(line):
		return True
	else:
		return False

def replace_hashtag(line, output,data_type):
	replacement = "#hashtag"
	if data_type == "train":
		tag = line.split()[1]
		edited_line = replacement + '\t' + tag + '\n'
		output.append(edited_line)
	else:
		output.append(replacement + '\n')



#parser = argparse.ArgumentParser()
#parser.add_argument('-i', dest='i')
#parser.add_argument('--type', dest='type', help='indicate train or test data')
#args = parser.parse_args()

#pre_process_data()
