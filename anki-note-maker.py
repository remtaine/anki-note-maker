#!venv/bin python2.7
import time
import os
import sys

ANSWER_SPLITTER = ','

notes_basic = []
notes_reversible = []
notes_cloze = []
notes_events = []
notes_residue = []

question_parts = []

args = sys.argv

today = time.strftime("%Y-%m-%d")
#only opens one file at a time for now
#TODO support multiple file conversion
if len(args) == 2:
	file_name = args[1];
else:
	file_name = raw_input("What should be opened? ")

file_to_open = open(file_name, 'r')

text_lines = file_to_open.readlines()

file_name_mod = file_name.split("_")
file_name_mod.pop(0)
file_name_mod = "_".join(file_name_mod)
if "." in file_name_mod:
	#removes the extension
	file_name_mod = file_name_mod[:file_name_mod.index(".")]

csv_basic_name = today + "_" + file_name_mod + "_notes_basic" + ".csv"
csv_reversible_name = today + "_" + file_name_mod + "_notes_reversible" + ".csv"
csv_cloze_name = today + "_" + file_name_mod + "_notes_cloze" + ".csv"
csv_events_name = today + "_" + file_name_mod + "_notes_events" + ".csv"
csv_residue_name = today + "_" + file_name_mod + "_notes_residue" + ".csv"

if os.path.isfile(csv_basic_name):
	os.remove(csv_basic_name)
if os.path.isfile(csv_reversible_name):
	os.remove(csv_reversible_name)
if os.path.isfile(csv_cloze_name):
	os.remove(csv_cloze_name)
if os.path.isfile(csv_events_name):
	os.remove(csv_events_name)
if os.path.isfile(csv_residue_name):
	os.remove(csv_residue_name)

csv_basic = open(csv_basic_name, 'w')
csv_reversible = open(csv_reversible_name, 'w')
csv_cloze = open(csv_cloze_name, 'w')
csv_events = open(csv_events_name, 'w')
csv_residue = open(csv_residue_name, 'w')

csv_basic.write("tags:" + text_lines[0])
csv_reversible.write("tags:" + text_lines[0])
csv_cloze.write("tags:" + text_lines[0])
csv_events.write("tags:" + text_lines[0])
csv_residue.write("tags:" + text_lines[0])

for line in text_lines[1:]:
	if line[0:2] == "//" or line[0] == "\n": #comment or break
		continue
	elif line[0] == "$":
	#residue
	# shift + 4
		#question_parts[0] = question_parts[0].replace(",","")
		#question_parts[1] = question_parts[1].replace(",","")
		#csv_residue.write(question_parts[0] + "?, " + question_parts[1])
		csv_residue.write(line)
		continue

	question_parts = line.split('?')
	if len(question_parts) != 2:
		print "ERROR: no '?' to signal question and answer. Aborting conversion."
		print "Error-containing question: " + str(question_parts)
		os.remove(csv_basic_name)
		os.remove(csv_reversible_name)
		os.remove(csv_cloze_name)
		os.remove(csv_events_name)
		os.remove(csv_residue_name)
		break

	if line[0] == "!":
	#reversible
	#shift + 1
		question_parts[0] = question_parts[0][1:]
		question_parts[0] = question_parts[0].replace(",","")
		question_parts[1] = question_parts[1].replace(",","")
		csv_reversible.write(question_parts[0] + "?," + question_parts[1])

	elif line[0] == "@":
	#cloze
	#shift + 2
	#TODO add a space between question and answers
		if line[-2:] == "@@":
			#TODO support multiline question
			#keep adding cloze answers one line at a time
			# until the next @@
			pass
		else:
			question_parts[0] = question_parts[0][1:]

			#cloze deletion needs special shiz
			cloze_answers = question_parts[1].split(ANSWER_SPLITTER)
			cloze_answers[-1] = cloze_answers[-1].rstrip()
			for i in xrange (0,len(cloze_answers)):
				x = i + 1
				cloze_answers[i] = r"{{c" + str(x) + r"::" + cloze_answers[i] + r"}}"
			lineup = question_parts[0] + "; " #will be Text
			for i in xrange (0,len(cloze_answers)):
				lineup = lineup + cloze_answers[i]
			lineup = lineup + "\n"
			csv_cloze.write(lineup)

	elif line[0] == "#":
	#step-by-step event
	#shift + 3
		if line[-2:] == "##":
			#TODO support multiline question
			#keep adding event answers one line at a time
			# until the next ##
			pass
		else:
			question_parts[0] = question_parts[0][1:]
			question_parts[1] = question_parts[1].split(ANSWER_SPLITTER)
			question_parts[1][0] = question_parts[1][0].rstrip("\n")
			question_parts[1][-1] = question_parts[1][-1].rstrip("\n")
			first_answer = question_parts[1][0]
			last_answer = question_parts[1][-1]

			#for first answer
			if "(" in first_answer and ")" in first_answer:
				parenthesis_num = first_answer[first_answer.index("(") + 1:first_answer.index(")")]
				csv_events.write("what is the #" + parenthesis_num + " " + question_parts[0] + " that comes before " + question_parts[1][1] + "?, " + first_answer + "\n")
			else:
				csv_events.write("what is the first " + question_parts[0] + " that comes before " + question_parts[1][1] + "?, " + first_answer + "\n")

			#for last answer
			if "(" in last_answer and ")" in last_answer:
				parenthesis_num = last_answer[last_answer.index("(") + 1:last_answer.index(")")]
				csv_events.write("what is the #" + parenthesis_num + " " + question_parts[0] + " that comes after " + question_parts[1][-2] + "?, " + last_answer + "\n")
			else:
				csv_events.write("what is the last " + question_parts[0] + " that comes after " + question_parts[1][-2] + "?, " + last_answer + "\n")

			# for middle answers
			for i in range(1, len(question_parts[1]) - 1):
				answer = question_parts[1][i].rstrip("\n")
				if "(" in answer and ")" in answer:
					parenthesis_num = answer[answer.index("(") + 1:answer.index(")")]
					csv_events.write("what is the #" + parenthesis_num + " " + question_parts[0] + " that comes after " + question_parts[1][i-1] + " and before " + question_parts[1][i+1] + "?, " + answer + "\n")
				else:
					csv_events.write("what is the #" + i + " " + question_parts[0] + " that comes after " + question_parts[1][i-1] + " and before " + question_parts[1][i+1] + "?, " + answer + "\n")
	else:
	#basic
		question_parts[0] = question_parts[0].replace(",","")
		question_parts[1] = question_parts[1].replace(",","")
		csv_basic.write(question_parts[0] + "?, " + question_parts[1])

file_to_open.close()
csv_basic.close()
csv_reversible.close()
csv_cloze.close()
csv_events.close()
csv_residue.close()

print "Note-making complete. This program may now be closed."
