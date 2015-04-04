#!usr/bin/env python
import time
import os

notes_basic = []
notes_reversible = []
notes_cloze = []
notes_residue = []

current_q_and_a = []

today = time.strftime("%Y-%m-%d")
file_name = raw_input("what should I open? ")
file_to_open = open(file_name, 'r')
strings = file_to_open.readlines()

modified_file_name = file_name.split("_")
modified_file_name.pop(0)
modified_file_name = "_".join(modified_file_name)

csv_basic_name = today + "_" + modified_file_name + "_notes_basic" + ".csv"
csv_reversible_name = today + "_" + modified_file_name + "_notes_reversible" + ".csv"
csv_cloze_name = today + "_" + modified_file_name + "_notes_cloze" + ".csv"
csv_residue_name = today + "_" + modified_file_name + "_notes_residue" + ".csv"

if os.path.isfile(csv_basic_name):
	os.remove(csv_basic_name)
if os.path.isfile(csv_reversible_name):
	os.remove(csv_reversible_name)
if os.path.isfile(csv_cloze_name):
	os.remove(csv_cloze_name)
if os.path.isfile(csv_residue_name):
	os.remove(csv_residue_name)

csv_basic = open(csv_basic_name, 'w')
csv_reversible = open(csv_reversible_name, 'w')
csv_cloze = open(csv_cloze_name, 'w')
csv_residue = open(csv_residue_name, 'w')

csv_basic.write("tags:" + strings[0])
csv_reversible.write("tags:" + strings[0])
csv_cloze.write("tags:" + strings[0])
csv_residue.write("tags:" + strings[0])

for line in strings[1:]:
	current_q_and_a = line.split('?')
	if len(current_q_and_a) != 2: 
		print current_q_and_a
		print "GG"
		os.remove(csv_basic_name)
		os.remove(csv_reversible_name)
		os.remove(csv_cloze_name)
		os.remove(csv_residue_name)
		break

	if line[0] == ">":
	#reversible
		current_q_and_a[0] = current_q_and_a[0][1:]
		current_q_and_a[0] = current_q_and_a[0].replace(",","")
		current_q_and_a[1] = current_q_and_a[1].replace(",","")
		csv_reversible.write(current_q_and_a[0] + "?," + current_q_and_a[1])

	elif line[0] == "<":
	#cloze 
		current_q_and_a[0] = current_q_and_a[0][1:]

		#cloze deletion needs special shiz
		clozers = current_q_and_a[1].split(',')
		clozers[-1] = clozers[-1].rstrip()
		for i in xrange (0,len(clozers)):
			x = i + 1
			clozers[i] = r"{{c" + str(x) + r"::" + clozers[i] + r"}}"
		lineup = current_q_and_a[0] + ": "
		for i in xrange (0,len(clozers)):
			lineup = lineup + clozers[i]
		lineup = lineup + "\n"
		csv_cloze.write(lineup)

	#elif line[0] == "/":
	#events
		#basic_questions = []
		#current_q_and_a[0] = current_q_and_a[0][1:]

		#cloze deletion needs special shiz
		#basics = current_q_and_a[1].split(',')
		#basics[-1] = basics[-1].rstrip()
		#for i in xrange (0,len(basics)):
			##rip the (X) for the event #X
			#num_start = basics[i].find("(")
			#num_end = basics[i].find(")")
			#event_number = basics[num_start:num_end+1]

			#if i == 0:
			##very first
				#basic_question = "what is event " + str(event_number) + " of " + str(current_q_and_a[0]) + " that happens before " + str(basics[1]) + "?"
			#elif i == len(basics) - 1:
			##very last
				#basic_question = "what is event " + str(event_number) + " of " + str(current_q_and_a[0]) + " that happens after " + str(basics[i - 1]) + "?"
			#else:
				#basic_question = "what is event " + str(event_number) + " of " + str(current_q_and_a[0]) + " that happens before " + str(basics[i + 1]) + " and after " + str(basics[i-1]) + "?"
			#basic_question += str(basics)
			#basic_question += str("\n")
			#csv_basic.write(basic_question)

	elif line[0] == "*" or line[0] == "/":
	#residue
		current_q_and_a[0] = current_q_and_a[0].replace(",","")
		current_q_and_a[1] = current_q_and_a[1].replace(",","")
		csv_residue.write(current_q_and_a[0] + "?," + current_q_and_a[1])

	else:
	#basic
		current_q_and_a[0] = current_q_and_a[0].replace(",","")
		current_q_and_a[1] = current_q_and_a[1].replace(",","")
		csv_basic.write(current_q_and_a[0] + "?," + current_q_and_a[1])
	
file_to_open.close()
csv_basic.close()
csv_reversible.close()
csv_cloze.close()
csv_residue.close()

print "done"
#first get file DONE
#for each line in file DONE
#separate according to question type (none, >, <) DONE
#separate each Q&A using the ? as separator DONE
#make CSV with those (3 separate for each question type) DONE
