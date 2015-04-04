#!usr/bin/env python
import time
import os
import sys

notes_basic = []
notes_reversible = []
notes_cloze = []
notes_residue = []

current_q_and_a = []

args = str(sys.argv)

today = time.strftime("%Y-%m-%d")
#only opens one file at a time for now
#TODO support multiple file conversion
if args.length == 2:
	file_name = args[1];	
else:
	file_name = raw_input("what should I open? ")
	file_to_open = open(file_name, 'r')

text_lines = file_to_open.readlines()

file_name_mod = file_name.split("_")
file_name_mod.pop(0)
file_name_mod = "_".join(file_name_mod)
if file_name_mod.index(".") != -1:
	#remove the extension
	file_name_mod = file_name_mod[:file_name_mod.index(".")]

csv_basic_name = today + "_" + file_name_mod + "_notes_basic" + ".csv"
csv_reversible_name = today + "_" + file_name_mod + "_notes_reversible" + ".csv"
csv_cloze_name = today + "_" + file_name_mod + "_notes_cloze" + ".csv"
csv_residue_name = today + "_" + file_name_mod + "_notes_residue" + ".csv"

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

csv_basic.write("tags:" + text_lines[0])
csv_reversible.write("tags:" + text_lines[0])
csv_cloze.write("tags:" + text_lines[0])
csv_residue.write("tags:" + text_lines[0])

for line in text_lines[1:]:
	current_q_and_a = line.split('?')
	if len(current_q_and_a) != 2: 
		print "ERROR: no '?' to signal question and answer. Aborting conversion."
		print "Error-containing question: " + str(current_q_and_a)
		os.remove(csv_basic_name)
		os.remove(csv_reversible_name)
		os.remove(csv_cloze_name)
		os.remove(csv_residue_name)
		break

	if line[0] == "!":
	#reversible
	#shift + 1
		current_q_and_a[0] = current_q_and_a[0][1:]
		current_q_and_a[0] = current_q_and_a[0].replace(",","")
		current_q_and_a[1] = current_q_and_a[1].replace(",","")
		csv_reversible.write(current_q_and_a[0] + "?," + current_q_and_a[1])

	elif line[0] == "@":
	#cloze 
	#shift + 2
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

	elif line[0] == "#":
	#step-by-step event
	#shift + 3
	#TODO: actually implement
		pass
	elif line[0] == "$":
	#residue
	# shift + 4
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
