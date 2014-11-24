import sys
import argparse
import csv

import parser # see parser.py in the same directory

# Execute the following command:
# python simple_pos_tagger.py -m sample_model_params.csv -e sample_eval_trgdata.csv -i sample.in -o sample.out -g sample_gold.out

class SimpleTagger:

	def __init__(self, emission_params, emission_counts, y_counts, input_file, output_file, gold_output):
		self.emission_params = list(emission_params)
		self.emission_counts = list(emission_counts)
		self.y_counts = list(y_counts)
		self.input = input_file
		self.output = output_file
		self.gold_output = gold_output

	def update_emission_parameters(self):
		"""
		Depending on whether x is a new word or has been seen in training,
		we update the emission parameters accordingly.
		This implies we actually don't require the OLD emission parameter values at all.
		"""
		input_file = open(self.input)
		self.emission_params = [] # reset the emission_param array

		for line in input_file: # input_file contains words that have not been tagged yet
			current_word = line.strip() 

			# skip blank words
			if current_word == "":
				continue
			
			seen = False
			for ec in self.emission_counts : # search emission_counts to find if current_word has been seen before
				if ec[0] == current_word:
					seen = True
					break
 	
			# update the emission params for all combinations of x,y
			if seen: 

				for ec in self.emission_counts:

					stored_word = ec[0] 	# x
					stored_label = ec[1]	# y
					count_y_to_x = ec[2]	# count(y->x)

					# match x value
					if stored_word == current_word:

						# match y value
						for y in self.y_counts:

							current_label = y[0]
							count_y = float(y[1])

							if stored_label == current_label:

								# compute emission param
								emission_param = float(count_y_to_x) / (count_y+1)

								# add it to child list
								new_emission_param_list = []
								new_emission_param_list.append(current_word)
								new_emission_param_list.append(current_label)
								new_emission_param_list.append(emission_param)

								# add it to parent list
								self.emission_params.append(new_emission_param_list)

								# at this point, we are done with the current x,y;
								# move onto next iteration
								break

			else: # not seen

				for y in self.y_counts: # for all y labels
					
					current_label = y[0]
					count_y = float(y[1])

					emission_param = 1.0 / (count_y + 1)

					new_emission_param_list = []
					new_emission_param_list.append(current_word)
					new_emission_param_list.append(current_label)
					new_emission_param_list.append(emission_param)

					self.emission_params.append(new_emission_param_list)

		input_file.close()

	def run_simple_tagger(self):
		input_file = open(self.input)
		output_file = open(self.output, 'w')
		gold_output_file = open(self.gold_output)

		# each element in output will be written on a single line 
		# in the output file eventually
		output = []

		correct = 0
		total = 0

		for line in input_file:
			current_word = line.strip()

			# skip blank words
			if current_word == '':
				output.append('\n')
				continue

			predicted_label = self.get_label_with_argmax(current_word)

			# compare with gold standard
			gold_row = gold_output_file.readline().strip().split('\t')
			if len(gold_row) == 2:
				if predicted_label == gold_row[1]:
					correct += 1
				total += 1

			# assemble output
			row = current_word + '\t' + predicted_label

			output.append(row)

		# assemble final output to be written to output file
		final_output = ''
		for row in output:
			final_output += row + '\n'

		output_file.write(final_output)
		sys.stdout.write('Written output file\n')

		percentage_accuracy = float(correct) / total
		sys.stdout.write('Accuracy compared to gold standard output: %.2f\n' % percentage_accuracy)

	def get_label_with_argmax(self, word):
		
		argmax = 0
		corresponding_label = ""

		for em in self.emission_params:
			if em[0] == word:
				if argmax < em[2]:
					argmax = em[2]
					corresponding_label = em[1]

		return corresponding_label

# End of Class SimpleTagger
		


###################################################
###################################################		

def get_data_from_csv(data, flag):
	emission = []
	transmission = []
	y_counts = []

	with open(data, 'rb') as f:
		csv_file_contents = csv.reader(f)
		for row in csv_file_contents:
			if row[0] == 'e':
				emission.append(row[1:])
			elif row[0] == 'q':
				transmission.append(row[1:])
			else:
				st = []
				st.append(row[1])
				st.append(row[3])
				y_counts.append(st)

	if flag == 'm':
		return emission, transmission

	else:
		return emission, transmission, y_counts

if __name__=="__main__":
	sys.stdout.write("\n----- Beginning Simple POS Tagger -----\n\n")
	
	parser = argparse.ArgumentParser()

	parser.add_argument('-m', dest = 'm', help = 'file containing model parameters')
	parser.add_argument('-e', dest = 'e', help = 'file containing evaluated training data')
	parser.add_argument('-i', dest = 'i', help = 'file containing test data to be tagged')
	parser.add_argument('-o', dest = 'o', help = 'output file to contain predicted tags')
	parser.add_argument('-g', dest = 'g', help = 'file containing gold-standard outputs')

	args = parser.parse_args()

	sys.stdout.write("Specified File for Model Parameters: %s\n" % args.m)
	sys.stdout.write("Specified File for Evaluated Training Data: %s\n" % args.e)
	sys.stdout.write("Specified File to be Tagged: %s\n" % args.i)
	sys.stdout.write("Specified File with Predicted Tags: %s\n" % args.o)
	sys.stdout.write("Specified File Containing Gold-Standard Outputs: %s\n" % args.g)

	emission_params, transmission_params = get_data_from_csv(args.m, 'm')
	# print emission_params
	# print transmission_params

	emission_counts, transmission_counts, y_counts = get_data_from_csv(args.e, 'e')
	# print emission_counts
	# print transmission_counts
	# print y_counts

	tagger = SimpleTagger(emission_params, emission_counts, y_counts, args.i, args.o, args.g)
	tagger.update_emission_parameters()
	tagger.run_simple_tagger()