#!/bin/sh
echo "" > extra_log.txt
echo "" > extra_brief_results.txt
#for dir in ../PA1_final_tests/*; do
#for dir in ../PA1_input_output_samples/*; do
for dir in ../PA1_extra_samples/*; do
    cp "${dir}/input.txt" ./input.txt
    python3 ../../compiler.py
    
	cp ./tokens.txt $(printf "${dir}/your_tokens.txt" $i)
	cp ./lexical_errors.txt $(printf "${dir}/your_lexical_errors.txt" $i)
	cp ./symbol_table.txt $(printf "${dir}/your_symbol_table.txt" $i)
    
    printf "\n\n\n\n=====================================>>>>> Running Test ${dir}...\n" >> extra_log.txt
    printf "\n\n=====================================>>>>> Running Test ${dir}...\n" >> extra_brief_results.txt
    printf "\n\n              *** tokens.txt diffrences ***\n" >> extra_log.txt
    diff -y -B -W 250 -w  --suppress-common-lines ./tokens.txt "${dir}/tokens.txt" >> extra_log.txt
    diff -y -B -W 250 -w -q ./tokens.txt "${dir}/tokens.txt" >> extra_brief_results.txt
    printf "\n\n              *** lexical_errors.txt diffrences ***\n" >> extra_log.txt
    diff -y -B -W 250 -w  --suppress-common-lines ./lexical_errors.txt "${dir}/lexical_errors.txt" >> extra_log.txt
    diff -y -B -W 250 -w -q ./lexical_errors.txt "${dir}/lexical_errors.txt" >> extra_brief_results.txt
    printf "\n\n              *** symbol_table.txt diffrences ***\n" >> extra_log.txt
    diff -y -B -W 250 -w  --suppress-common-lines ./symbol_table.txt "${dir}/symbol_table.txt" >> extra_log.txt
    diff -y -B -W 250 -w -q ./symbol_table.txt "${dir}/symbol_table.txt" >> extra_brief_results.txt
    
    echo "test $dir finished";
done


